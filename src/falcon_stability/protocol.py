"""Local evaluation protocol.

FALCON's held-out *evaluation* data is private (scored on EvalAI). Locally we only have each
held-out day's calibration files, so we split every such file in time:

    first `adapt_frac` of bins  -> adaptation block (unlabelled for label-free methods,
                                   labelled for few-shot methods)
    remaining bins             -> evaluation block, scored with FALCON's eval_mask

`test`: train on all held-in days, evaluate on held-out days.
`dev`:  train on held-in days except the last `n_dev_days`, evaluate on those (files cropped to the
        median held-out file length so the adaptation budget matches). Hyperparameters are chosen on
        `dev` only; `test` numbers are never used for selection.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .data import Session, group_by_day, load_split
from .metrics import r2_vw
from .methods import REGISTRY


@dataclass
class EvalDay:
    day: str
    days_since: int          # days since the last reference (training) day
    files: list[Session]


def make_split(task: str, which: str, n_dev_days: int = 2):
    held_in = load_split(task, "held_in_calib")
    if which == "test":
        held_out = load_split(task, "held_out_calib")
        ref, tgt = held_in, held_out
    elif which == "dev":
        days = group_by_day(held_in)
        keys = list(days)
        ref = [s for k in keys[:-n_dev_days] for s in days[k]]
        crop = int(np.median([len(s.X) for s in load_split(task, "held_out_calib")]))
        tgt = []
        for k in keys[-n_dev_days:]:
            for s in days[k]:
                tgt.append(Session(s.task, s.split, s.name, s.date, s.X[:crop], s.Y[:crop], s.mask[:crop],
                                   s.trial_change[:crop]))
    else:
        raise ValueError(which)
    last = max(s.date for s in ref)
    eval_days = [EvalDay(k, (v[0].date - last).days, v) for k, v in group_by_day(tgt).items()]
    return ref, eval_days


def run_method(name: str, ref, eval_days, adapt_frac: float = 0.5, drop_still: bool = False, seed: int = 0,
               **kw) -> list[dict]:
    cls = REGISTRY[name]
    m = cls(drop_still=drop_still, seed=seed, **kw)
    m.fit_reference([(s.X, s.Y, s.mask) for s in ref])
    rows = []
    for ed in eval_days:
        cut = [int(adapt_frac * len(s.X)) for s in ed.files]
        bx = [s.X[:c] for s, c in zip(ed.files, cut)]
        by = [s.Y[:c] for s, c in zip(ed.files, cut)] if cls.needs_labels else None
        bm = [s.mask[:c] for s, c in zip(ed.files, cut)] if cls.needs_labels else None
        m.adapt(bx, by, bm)
        for s, c in zip(ed.files, cut):
            pred = m.predict(s.X)
            ev = np.zeros(len(s.X), bool)
            ev[c:] = True
            ev &= s.mask
            rows.append(dict(method=name, seed=seed, session=s.name, day=ed.day, days_since=ed.days_since,
                             r2=r2_vw(s.Y[ev], pred[ev]), n_eval=int(ev.sum())))
    return rows
