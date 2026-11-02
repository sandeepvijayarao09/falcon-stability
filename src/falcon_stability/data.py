"""Load FALCON sessions (via the official falcon_challenge loader) and cache them as .npz."""
from __future__ import annotations

import datetime as dt
import pathlib
import re
from dataclasses import dataclass

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
SPLITS = ("held_in_calib", "minival", "held_out_calib")


@dataclass
class Session:
    task: str
    split: str
    name: str            # file stem
    date: dt.date
    X: np.ndarray        # (T, C) binned spike counts, 20 ms bins
    Y: np.ndarray        # (T, D) decoding targets
    mask: np.ndarray     # (T,) FALCON eval_mask
    trial_change: np.ndarray

    @property
    def day_key(self) -> str:
        return self.date.isoformat()


def parse_date(stem: str) -> dt.date:
    m = re.search(r"ses-(\d{4})-?(\d{2})-?(\d{2})", stem)
    if not m:
        raise ValueError(f"no session date in {stem}")
    return dt.date(*map(int, m.groups()))


def _load_nwb(path: pathlib.Path, task: str):
    from falcon_challenge.config import FalconTask
    from falcon_challenge.dataloaders import load_nwb
    X, Y, tc, mask = load_nwb(path, dataset=getattr(FalconTask, task))
    return np.asarray(X), np.asarray(Y, dtype=np.float32), np.asarray(tc, bool), np.asarray(mask, bool)


def load_split(task: str, split: str, data_dir: pathlib.Path = DATA) -> list[Session]:
    files = sorted((data_dir / task / split).glob("*.nwb"))
    if not files:
        raise FileNotFoundError(f"no NWB files in {data_dir / task / split}; run scripts/get_data.py {task}")
    cache = data_dir / "cache" / task / split
    cache.mkdir(parents=True, exist_ok=True)
    out = []
    for f in files:
        c = cache / (f.stem + ".npz")
        if not c.exists():
            X, Y, tc, mask = _load_nwb(f, task)
            np.savez_compressed(c, X=X, Y=Y, tc=tc, mask=mask)
        z = np.load(c)
        out.append(Session(task, split, f.stem, parse_date(f.stem), z["X"], z["Y"], z["mask"], z["tc"]))
    out.sort(key=lambda s: (s.date, s.name))
    return out


def group_by_day(sessions: list[Session]) -> dict[str, list[Session]]:
    days: dict[str, list[Session]] = {}
    for s in sessions:
        days.setdefault(s.day_key, []).append(s)
    return dict(sorted(days.items()))
