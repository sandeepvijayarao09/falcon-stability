"""Local evaluation protocols. Scores are FALCON's metric, computed per *day*: for each day, eval
bins of all that day's files are concatenated and variance-weighted R^2 is computed. This matches
falcon_challenge's `compute_metrics_regression`, which groups H1 `S6_set_1`/`S6_set_2` under one
session key (`reduce_key`). M1 has one file per day.

FALCON's held-out *evaluation* data is private (scored on EvalAI), so locally:

`test`    reference = all held-in days. For each held-out day, each calibration file is split in time:
          first `adapt_frac` -> adaptation block (unlabelled, or labelled for few-shot methods);
          remainder -> scored. Weakness: on H1 that leaves ~24 s per file, and the two halves cover
          different movements (scripts/diagnose_behaviour.py), so H1 `test` is uninformative.
`minival` for each held-in day d after the first: reference = held-in days before d; adaptation =
          the first N bins of d's calibration files (N = median held-out calibration file length,
          the budget FALCON gives few-shot methods); scored = d's minival files (later trials of the
          same session). Longer, behaviourally richer eval windows than `test`, but only 1-12 days
          of drift and the same days that `dev` uses for selection (see README).
`dev`     reference = held-in days except the last `n_dev_days`; those days are cropped to N bins
          and split like `test`. Used for all hyperparameter selection.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from .data import Session, group_by_day, load_split
from .metrics import r2_vw
from .methods import REGISTRY


@dataclass
class EvalDay:
    day: str
    days_since: int                       # days since the last reference (training) day
    adapt: list[np.ndarray]               # adaptation blocks: raw counts
    adapt_Y: list[np.ndarray]
    adapt_m: list[np.ndarray]
    score: list[tuple[Session, int]]      # (session, first scored bin); predict on the whole session


@dataclass
class Episode:
    ref: list[Session]
    days: list[EvalDay] = field(default_factory=list)


def _crop(s: Session, n: int) -> Session:
    return Session(s.task, s.split, s.name, s.date, s.X[:n], s.Y[:n], s.mask[:n], s.trial_change[:n])


def calib_budget(task: str) -> int:
    return int(np.median([len(s.X) for s in load_split(task, "held_out_calib")]))


def _split_days(files_by_day: dict, last_ref, adapt_frac: float) -> list[EvalDay]:
    out = []
    for day, files in files_by_day.items():
        cut = [int(adapt_frac * len(s.X)) for s in files]
        out.append(EvalDay(day, (files[0].date - last_ref).days,
                           [s.X[:c] for s, c in zip(files, cut)], [s.Y[:c] for s, c in zip(files, cut)],
                           [s.mask[:c] for s, c in zip(files, cut)], list(zip(files, cut))))
    return out


def make_episodes(task: str, which: str, adapt_frac: float = 0.5, n_dev_days: int = 2) -> list[Episode]:
    held_in = load_split(task, "held_in_calib")
    if which == "test":
        ref = held_in
        days = _split_days(group_by_day(load_split(task, "held_out_calib")), max(s.date for s in ref), adapt_frac)
        return [Episode(ref, days)]
    by_day = group_by_day(held_in)
    keys = list(by_day)
    n = calib_budget(task)
    if which == "dev":
        ref = [s for k in keys[:-n_dev_days] for s in by_day[k]]
        tgt = {k: [_crop(s, n) for s in by_day[k]] for k in keys[-n_dev_days:]}
        return [Episode(ref, _split_days(tgt, max(s.date for s in ref), adapt_frac))]
    if which == "minival":
        mv = group_by_day(load_split(task, "minival"))
        eps = []
        for i, k in enumerate(keys[1:], start=1):
            ref = [s for kk in keys[:i] for s in by_day[kk]]
            cal = [_crop(s, n) for s in by_day[k]]
            d = EvalDay(k, (by_day[k][0].date - max(s.date for s in ref)).days,
                        [s.X for s in cal], [s.Y for s in cal], [s.mask for s in cal], [(s, 0) for s in mv[k]])
            eps.append(Episode(ref, [d]))
        return eps
    raise ValueError(which)


def run_method(name: str, episodes: list[Episode], drop_still: bool = False, seed: int = 0, **kw) -> list[dict]:
    cls = REGISTRY[name]
    rows = []
    for ep in episodes:
        m = cls(drop_still=drop_still, seed=seed, **kw)
        m.fit_reference([(s.X, s.Y, s.mask) for s in ep.ref])
        for d in ep.days:
            labelled = cls.needs_labels
            m.diag = {}
            m.adapt(d.adapt, d.adapt_Y if labelled else None, d.adapt_m if labelled else None)
            ys, ps = [], []
            for s, start in d.score:
                pred = m.predict(s.X)
                ev = np.zeros(len(s.X), bool)
                ev[start:] = True
                ev &= s.mask
                ys.append(s.Y[ev])
                ps.append(pred[ev])
            y, p = np.concatenate(ys), np.concatenate(ps)
            rows.append(dict(method=name, seed=seed, day=d.day, days_since=d.days_since, r2=r2_vw(y, p),
                             finite=bool(np.isfinite(p).all()), n_eval=len(y), n_files=len(d.score),
                             n_adapt=int(sum(len(x) for x in d.adapt)), **m.diag))
    return rows
