"""Feature transforms shared by all decoders. Matches the FALCON reference Wiener filter."""
from __future__ import annotations

import numpy as np
from scipy.signal import lfilter

NEURAL_TAU_MS = 240.0
BIN_MS = 20


def exp_kernel(tau_ms: float = NEURAL_TAU_MS, bin_ms: int = BIN_MS, extent: int = 1) -> np.ndarray:
    t = np.arange(0, extent * tau_ms, bin_ms)
    k = np.exp(-t / tau_ms)
    return k / k.sum()


def smooth(X: np.ndarray, tau_ms: float = NEURAL_TAU_MS) -> np.ndarray:
    """Causal FIR exponential smoothing, identical to falcon-challenge `apply_exponential_filter`."""
    return lfilter(exp_kernel(tau_ms), [1.0], X.astype(np.float64), axis=0)


def lagged(X: np.ndarray, history: int) -> np.ndarray:
    """Stack X[t], X[t-1], ..., X[t-history] (zero-padded at the start), keeping length T."""
    if history == 0:
        return X
    T, C = X.shape
    out = np.zeros((T, C * (history + 1)), dtype=X.dtype)
    for i in range(history + 1):
        out[i:, i * C:(i + 1) * C] = X[: T - i]
    return out


def zscore_stats(X: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    m, s = X.mean(0), X.std(0)
    s = np.where(s == 0, 1.0, s)
    return m, s
