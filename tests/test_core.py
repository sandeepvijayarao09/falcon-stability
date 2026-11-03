"""Fast tests on synthetic data; no FALCON download needed (CI-safe)."""
import numpy as np
import pytest
from sklearn.metrics import r2_score

from falcon_stability.data import parse_date
from falcon_stability.features import exp_kernel, lagged, smooth
from falcon_stability.methods import REGISTRY, behaviour_weights, fit_tlma_map, lagged_covs
from falcon_stability.metrics import bootstrap_ci, r2_vw


def test_r2_matches_sklearn_variance_weighted():
    rng = np.random.default_rng(0)
    y = rng.normal(size=(500, 3)) * [1, 5, 0.1]
    yhat = y + rng.normal(size=y.shape)
    assert r2_vw(y, yhat) == pytest.approx(r2_score(y, yhat, multioutput="variance_weighted"))


def test_smoothing_is_causal_and_matches_reference_kernel():
    k = exp_kernel()
    assert len(k) == 12 and k.sum() == pytest.approx(1)  # tau 240 ms, 20 ms bins, extent 1
    x = np.zeros((50, 1)); x[20] = 1
    s = smooth(x)
    assert np.all(s[:20] == 0)  # nothing before the impulse
    assert s[20:32, 0] == pytest.approx(k)


def test_lagged_shapes_and_alignment():
    X = np.arange(10, dtype=float)[:, None]
    L = lagged(X, 2)
    assert L.shape == (10, 3)
    assert list(L[5]) == [5, 4, 3]


def test_bootstrap_ci_contains_mean():
    m, lo, hi = bootstrap_ci([0.1, 0.2, 0.3, 0.4])
    assert lo <= m <= hi and m == pytest.approx(0.25)


def test_parse_date_both_formats():
    assert str(parse_date("sub-HumanPitt-held-out-calib_ses-19250126T113454")) == "1925-01-26"
    assert str(parse_date("sub-MonkeyL-held-in-calib_ses-20120924_behavior+ecephys")) == "2012-09-24"


def _ar_latents(T, k, rng):
    """Latents with distinct temporal autocorrelations (identifiable from lagged moments)."""
    rho = np.linspace(0.5, 0.98, k)
    L = np.zeros((T, k))
    for t in range(1, T):
        L[t] = rho * L[t - 1] + rng.normal(size=k) * np.sqrt(1 - rho ** 2)
    return L


def test_tlma_recovers_a_mixing_that_covariance_alone_cannot():
    rng = np.random.default_rng(1)
    k, lags = 4, (0, 1, 2, 4, 8)
    L0 = _ar_latents(20000, k, rng)
    Q, _ = np.linalg.qr(rng.normal(size=(k, k)))
    R = Q @ np.diag([1.0, 1.0, 1.0, 1.0])  # an orthogonal drift: invisible to lag-0 covariance
    small = 0.3 * (R - np.eye(k)) + np.eye(k)
    Ld = _ar_latents(20000, k, rng) @ np.linalg.inv(small).T  # new day = drifted latents
    A = fit_tlma_map(lagged_covs(L0, lags), lagged_covs(Ld, lags), lam=1e-4)
    err_tlma = np.linalg.norm(A - small) / np.linalg.norm(small)
    A0 = fit_tlma_map(lagged_covs(L0, (0,)), lagged_covs(Ld, (0,)), lam=1e-4)
    err_cov = np.linalg.norm(A0 - small) / np.linalg.norm(small)
    assert err_tlma < 0.1
    assert err_tlma < err_cov


def test_behaviour_weights_are_scale_free():
    """Regression test: H1 velocities have SD ~1e-3; weights must not collapse to uniform."""
    rng = np.random.default_rng(2)
    ref = rng.normal(size=(4000, 3)) * 1e-3
    day = (rng.normal(size=(1000, 3)) + [1.5, 0, 0]) * 1e-3
    w = behaviour_weights(ref, day)
    assert w.mean() == pytest.approx(1)
    assert np.corrcoef(w, ref[:, 0])[0, 1] > 0.3  # upweights reference bins that look like today


@pytest.mark.parametrize("name", ["frozen_day_zscore", "fewshot_pooled", "fa_procrustes", "tlma", "br_tlma"])
def test_methods_run_end_to_end_on_synthetic_drift(name):
    rng = np.random.default_rng(3)
    C, T, D = 24, 3000, 2
    W = rng.normal(size=(D, 4))
    loadings = rng.normal(size=(4, C))

    def session(gain):
        lat = _ar_latents(T, 4, rng)
        Y = lat @ W.T
        rates = np.exp(0.3 * lat @ loadings - 1) * gain
        return rng.poisson(rates).astype(np.uint8), Y.astype(np.float32), np.ones(T, bool)
    ref = [session(np.ones(C)) for _ in range(2)]
    X, Y, m = session(rng.uniform(0.5, 1.5, C))
    meth = REGISTRY[name](k=4, lam=1.0, alpha=1.0)
    meth.fit_reference(ref)
    meth.adapt([X[:1500]], [Y[:1500]], [m[:1500]])
    pred = meth.predict(X)
    assert pred.shape == Y.shape and np.isfinite(pred).all()


def test_behaviour_weights_fall_back_to_uniform_when_degenerate():
    """Regression test for the M1 seed-4 failure: an outlier-dominated ratio must not return NaN."""
    rng = np.random.default_rng(4)
    ref = rng.standard_t(1.5, size=(5000, 4))
    day = rng.normal(size=(500, 4)) * 0.05
    w = behaviour_weights(ref, day)
    assert np.isfinite(w).all() and w.mean() == pytest.approx(1)
