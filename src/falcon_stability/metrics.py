"""FALCON metric (variance-weighted R^2 per session) plus resampling CIs."""
from __future__ import annotations

import numpy as np


def r2_vw(y: np.ndarray, yhat: np.ndarray) -> float:
    """Variance-weighted R^2, same as sklearn r2_score(multioutput='variance_weighted')."""
    y, yhat = np.asarray(y, float), np.asarray(yhat, float)
    ss_res = ((y - yhat) ** 2).sum()
    ss_tot = ((y - y.mean(0)) ** 2).sum()
    return float(1.0 - ss_res / ss_tot)


def bootstrap_ci(values, n_boot: int = 10000, alpha: float = 0.05, seed: int = 0) -> tuple[float, float, float]:
    """Mean and percentile bootstrap CI over independent units (sessions)."""
    v = np.asarray(values, float)
    rng = np.random.default_rng(seed)
    boots = v[rng.integers(0, len(v), (n_boot, len(v)))].mean(1)
    lo, hi = np.quantile(boots, [alpha / 2, 1 - alpha / 2])
    return float(v.mean()), float(lo), float(hi)


def paired_bootstrap_ci(a, b, **kw) -> tuple[float, float, float]:
    """CI on mean(a - b) for per-session paired scores."""
    return bootstrap_ci(np.asarray(a) - np.asarray(b), **kw)
