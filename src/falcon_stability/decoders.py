"""Linear Wiener-filter decoder (FALCON reference baseline) on smoothed, z-scored spikes."""
from __future__ import annotations

import numpy as np
from sklearn.linear_model import Ridge
from sklearn.model_selection import GridSearchCV

from .features import lagged

ALPHAS = np.logspace(-5, 5, 20)


def train_mask(Y: np.ndarray, mask: np.ndarray, drop_still: bool) -> np.ndarray:
    m = mask & ~np.isnan(Y).any(1)
    if drop_still:  # reference masks timepoints with no movement (H1)
        m &= ~np.all(np.abs(Y) < 1e-3, axis=1)
    return m


class WienerFilter:
    def __init__(self, history: int = 0, alpha: float | None = None):
        self.history, self.alpha = history, alpha

    def fit(self, Z: np.ndarray, Y: np.ndarray, m: np.ndarray) -> "WienerFilter":
        """Z: z-scored smoothed rates (T, C). m: boolean train mask."""
        F = lagged(Z, self.history)[m]
        if self.alpha is None:
            gs = GridSearchCV(Ridge(), {"alpha": ALPHAS}).fit(F, Y[m])
            self.alpha = float(gs.best_params_["alpha"])
        self.model = Ridge(alpha=self.alpha).fit(F, Y[m])
        return self

    def predict(self, Z: np.ndarray) -> np.ndarray:
        return self.model.predict(lagged(Z, self.history))
