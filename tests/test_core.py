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


def _ar_latents(T, k, rng, rho=None):
    """Unit-variance AR(1) latents; distinct `rho` per latent makes them identifiable from lagged moments."""
    rho = np.linspace(0.5, 0.98, k) if rho is None else np.asarray(rho, float)
    L = np.zeros((T, k))
    for t in range(1, T):
        L[t] = rho * L[t - 1] + rng.normal(size=k) * np.sqrt(1 - rho ** 2)
    return L


def _rotation(k, rng, angle=0.3):
    from scipy.linalg import expm
    S = rng.normal(size=(k, k))
    S = (S - S.T) / 2
    return expm(angle * S / np.linalg.norm(S, 2))  # orthogonal, ~angle radians from identity


def _recovery_errors(rho, seed):
    rng = np.random.default_rng(seed)
    k, lags = len(rho), (0, 1, 2, 4, 8)
    L0 = _ar_latents(20000, k, rng, rho)
    R = _rotation(k, rng)
    # new day: z_d = R^T z, so the aligning map is A = R. Unit-variance latents => C_d(0) = C_0(0) = I,
    # i.e. the drift is invisible to lag-0 covariance matching.
    Ld = _ar_latents(20000, k, rng, rho) @ R
    A = fit_tlma_map(lagged_covs(L0, lags), lagged_covs(Ld, lags), lam=1e-6)
    A0 = fit_tlma_map(lagged_covs(L0, (0,)), lagged_covs(Ld, (0,)), lam=1e-6)
    rel = lambda M: np.linalg.norm(M - R) / np.linalg.norm(R - np.eye(k))  # 1.0 = no better than identity
    return rel(A), rel(A0)


def test_tlma_recovers_rotation_that_covariance_alone_cannot():
    # Only partial recovery: relative error 0.19-0.49 over seeds 0-2 with 20k bins (1.0 = identity).
    for seed in (0, 1, 2):
        err_tlma, err_cov = _recovery_errors(np.linspace(0.5, 0.98, 4), seed=seed)
        assert err_tlma < 0.6      # lagged moments recover a substantial part of the rotation
        assert err_cov > 0.9       # lag-0 covariance leaves A at the identity


def test_tlma_cannot_identify_rotation_when_autocorrelations_are_equal():
    """Known limit: with equal autocorrelation every lagged covariance is proportional to I, so any
    rotation fits equally well (the same failure as AMUSE/SOBI); with a tiny ridge the solution is
    arbitrary (relative error 4-7 over seeds 0-2), which is why a pull toward the identity is needed."""
    err_tlma, _ = _recovery_errors([0.9, 0.9, 0.9, 0.9], seed=1)
    assert err_tlma > 0.9


def test_lagged_covs_do_not_straddle_file_boundaries():
    a = np.tile([[1.0], [-1.0]], (50, 1))   # alternating: lag-1 autocovariance -1
    b = a.copy()
    joined = lagged_covs(np.concatenate([a, b[1:]]), (1,))[0]  # boundary pair (+1 then +1) would add +1
    split = lagged_covs([a, b[1:]], (1,))[0]
    assert split[0, 0] == pytest.approx(-1.0, abs=1e-3)
    assert joined[0, 0] > split[0, 0]


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


@pytest.mark.parametrize("method", ["wf", "gru"])
def test_online_submission_decoder_matches_offline_pipeline(tmp_path, method):
    """The EvalAI decoder (one bin at a time) must reproduce the offline pipeline exactly."""
    import pathlib
    import torch
    from falcon_challenge.config import FalconConfig, FalconTask
    from falcon_stability.features import smooth, zscore_stats
    from falcon_stability.submission import StabilityDecoder
    rng = np.random.default_rng(5)
    C, T, D = 64, 400, 16   # M1 shapes
    ref = [(rng.poisson(1.0, (1500, C)).astype(np.uint8), rng.normal(size=(1500, D)).astype(np.float32),
            np.ones(1500, bool)) for _ in range(2)]
    name = {"wf": "frozen_day_zscore", "gru": "gru_frozen"}[method]
    m = REGISTRY[name](seed=0, steps=20)
    m.fit_reference(ref)
    X = rng.poisson(1.2, (T, C)).astype(np.uint8)
    m.adapt([X])
    offline = m.predict(X)
    mu, sd = zscore_stats(smooth(X))
    tag = "sub-MonkeyL-held-out-calib_ses-20121004_behavior+ecephys"
    payload = {"method": method, "stats": {"20121004": (mu.astype(np.float32), sd.astype(np.float32))},
               "coef": m.wf.model.coef_.astype(np.float32), "intercept": m.wf.model.intercept_.astype(np.float32)}
    if method == "gru":
        payload.update(gru_state=m.net0.state_dict(), hidden=m.net0.gru.hidden_size)
    torch.save(payload, tmp_path / "p.pt")
    dec = StabilityDecoder(FalconConfig(task=FalconTask.m1), str(tmp_path / "p.pt"), batch_size=1)
    dec.reset([pathlib.Path(tag + ".nwb")])
    online = np.concatenate([dec.predict(X[t:t + 1]) for t in range(T)])
    assert np.allclose(online, offline, atol=2e-3, rtol=1e-3)
