"""Decoding pipelines evaluated under one protocol.

Every method is fitted once on reference (held-in) sessions, then for each new day it may `adapt`
on that day's adaptation block (unlabelled, unless `needs_labels`), and `predict` on full files.
All features are causal, so predicting the whole file and scoring only the evaluation block is
equivalent to running online after adaptation.
"""
from __future__ import annotations

import numpy as np
from scipy.linalg import orthogonal_procrustes
from sklearn.decomposition import PCA, FactorAnalysis

from .decoders import WienerFilter, train_mask
from .features import smooth, zscore_stats


def _zs_per_file(blocks: list[np.ndarray]) -> list[np.ndarray]:
    out = []
    for X in blocks:
        S = smooth(X)
        mu, sd = zscore_stats(S)
        out.append((S - mu) / sd)
    return out


class Method:
    name = "base"
    needs_labels = False

    def __init__(self, history: int = 0, drop_still: bool = False, seed: int = 0, **kw):
        self.history, self.drop_still, self.seed = history, drop_still, seed
        self.kw = kw

    # ref: list of (X, Y, mask) for held-in training files
    def fit_reference(self, ref):
        raise NotImplementedError

    def adapt(self, blocks_X: list[np.ndarray], blocks_Y: list[np.ndarray] | None = None, blocks_m=None):
        pass

    def predict(self, X: np.ndarray) -> np.ndarray:
        raise NotImplementedError


# ----------------------------------------------------------------------------- channel-space WF
class FrozenHeldInNorm(Method):
    """Strict zero-shot: one z-score computed on all held-in data, decoder frozen, no new-day info."""
    name = "frozen_heldin_norm"

    def fit_reference(self, ref):
        S = np.concatenate([smooth(X) for X, _, _ in ref])
        self.mu, self.sd = zscore_stats(S)
        Y = np.concatenate([y for _, y, _ in ref])
        m = train_mask(Y, np.concatenate([mm for _, _, mm in ref]), self.drop_still)
        self.wf = WienerFilter(self.history, self.kw.get("alpha")).fit((S - self.mu) / self.sd, Y, m)

    def predict(self, X):
        return self.wf.predict((smooth(X) - self.mu) / self.sd)


class FrozenDayZscore(Method):
    """FALCON reference zero-shot WF: frozen weights, inputs z-scored with each day's own stats
    (estimated from the unlabelled adaptation block)."""
    name = "frozen_day_zscore"

    def fit_reference(self, ref):
        Z = np.concatenate(_zs_per_file([X for X, _, _ in ref]))
        Y = np.concatenate([y for _, y, _ in ref])
        m = train_mask(Y, np.concatenate([mm for _, _, mm in ref]), self.drop_still)
        self.wf = WienerFilter(self.history, self.kw.get("alpha")).fit(Z, Y, m)
        self.Ztrain, self.Ytrain, self.mtrain = Z, Y, m

    def adapt(self, blocks_X, blocks_Y=None, blocks_m=None):
        self.mu, self.sd = zscore_stats(np.concatenate([smooth(X) for X in blocks_X]))

    def predict(self, X):
        return self.wf.predict((smooth(X) - self.mu) / self.sd)


class FewShotPooled(FrozenDayZscore):
    """Labelled recalibration: refit the WF on held-in data pooled with today's labelled block."""
    name = "fewshot_pooled"
    needs_labels = True

    def adapt(self, blocks_X, blocks_Y=None, blocks_m=None):
        super().adapt(blocks_X)
        Zd = np.concatenate([(smooth(X) - self.mu) / self.sd for X in blocks_X])
        Yd = np.concatenate(blocks_Y)
        md = train_mask(Yd, np.concatenate(blocks_m), self.drop_still)
        w = self.kw.get("day_weight", 1)
        Z = np.concatenate([self.Ztrain] + [Zd] * w)
        Y = np.concatenate([self.Ytrain] + [Yd] * w)
        m = np.concatenate([self.mtrain] + [md] * w)
        self.wf = WienerFilter(self.history, self.kw.get("alpha")).fit(Z, Y, m)


class FewShotDayOnly(FrozenDayZscore):
    """Labelled recalibration from today's block only (new decoder, alpha chosen by CV)."""
    name = "fewshot_day_only"
    needs_labels = True

    def adapt(self, blocks_X, blocks_Y=None, blocks_m=None):
        super().adapt(blocks_X)
        Zd = np.concatenate([(smooth(X) - self.mu) / self.sd for X in blocks_X])
        Yd = np.concatenate(blocks_Y)
        md = train_mask(Yd, np.concatenate(blocks_m), self.drop_still)
        self.wf = WienerFilter(self.history, None).fit(Zd, Yd, md)


# ----------------------------------------------------------------------------- latent-space pipelines
class LatentBase(Method):
    """Shared reference latent space: z-scored smoothed rates -> k latents -> ridge to kinematics."""
    name = "latent_frozen"

    def _project_ref(self, Zs):
        raise NotImplementedError

    def fit_reference(self, ref):
        self.k = self.kw.get("k", 20)
        Zs = _zs_per_file([X for X, _, _ in ref])
        self.Zref = np.concatenate(Zs)
        L = self._fit_latent(self.Zref)
        Y = np.concatenate([y for _, y, _ in ref])
        m = train_mask(Y, np.concatenate([mm for _, _, mm in ref]), self.drop_still)
        self.ref_latents = L
        self.wf = WienerFilter(self.history, self.kw.get("alpha")).fit(L, Y, m)

    def _fit_latent(self, Z):
        self.pca = PCA(self.k, random_state=self.seed).fit(Z)
        return self.pca.transform(Z)

    def _latent(self, Z):
        return self.pca.transform(Z)

    def adapt(self, blocks_X, blocks_Y=None, blocks_m=None):
        self.mu, self.sd = zscore_stats(np.concatenate([smooth(X) for X in blocks_X]))

    def _day_latent(self, Z):
        return self._latent(Z)

    def predict(self, X):
        return self.wf.predict(self._day_latent((smooth(X) - self.mu) / self.sd))


class FAProcrustes(LatentBase):
    """Degenhart et al. 2020 (Nat. BME) style stabilizer: per-day factor analysis, iteratively find
    channels whose loadings agree with the reference, Procrustes-rotate the new latents onto the
    reference latents using only those stable channels. Label-free."""
    name = "fa_procrustes"

    def _fit_latent(self, Z):
        self.fa_ref = FactorAnalysis(self.k, random_state=self.seed).fit(Z)
        return self.fa_ref.transform(Z)

    def _latent(self, Z):
        return self.fa_ref.transform(Z)

    def adapt(self, blocks_X, blocks_Y=None, blocks_m=None):
        super().adapt(blocks_X)
        Zd = np.concatenate([(smooth(X) - self.mu) / self.sd for X in blocks_X])
        self.fa_day = FactorAnalysis(self.k, random_state=self.seed).fit(Zd)
        L0, Ld = self.fa_ref.components_.T, self.fa_day.components_.T  # (C, k)
        C = L0.shape[0]
        keep = np.arange(C)
        n_stable = max(self.k + 1, int(self.kw.get("stable_frac", 0.6) * C))
        while True:
            O, _ = orthogonal_procrustes(Ld[keep], L0[keep])
            err = np.linalg.norm(Ld @ O - L0, axis=1)
            if len(keep) <= n_stable:
                break
            n_drop = max(1, min(len(keep) - n_stable, int(0.05 * C)))
            worst = keep[np.argsort(err[keep])[-n_drop:]]
            keep = np.setdiff1d(keep, worst)
        self.O, self.stable = O, keep

    def _day_latent(self, Z):
        return self.fa_day.transform(Z) @ self.O


def lagged_covs(L: np.ndarray, lags, w: np.ndarray | None = None) -> list[np.ndarray]:
    """Symmetrised lagged covariances. Optional per-bin weights w (pair (t, t+tau) gets w[t])."""
    L = np.asarray(L, np.float64)
    T = len(L)
    w = np.ones(T) if w is None else np.asarray(w, np.float64)
    L = L - (w[:, None] * L).sum(0) / w.sum()
    out = []
    for t in lags:
        A, B, ww = L[: T - t], L[t:], w[: T - t]
        Ct = (ww[:, None] * A).T @ B / ww.sum()
        out.append(0.5 * (Ct + Ct.T))
    return out


def behaviour_weights(yhat_ref: np.ndarray, yhat_day: np.ndarray, clip_q: float = 0.99) -> np.ndarray:
    """Importance weights on reference bins so the frozen decoder's outputs on the reference match
    the distribution of its outputs on the new day (Gaussian density ratio, clipped, mean 1).
    Both sides pass through the same frozen decoder, so decoder shrinkage cancels. Label-free."""
    from scipy.stats import multivariate_normal as mvn
    D = yhat_ref.shape[1]
    mu, sd = yhat_ref.mean(0), yhat_ref.std(0) + 1e-12  # scale-free (H1 velocities have SD ~1e-3)
    yhat_ref, yhat_day = (yhat_ref - mu) / sd, (yhat_day - mu) / sd
    eps = 1e-3 * np.eye(D)
    lr = (mvn(yhat_day.mean(0), np.cov(yhat_day.T) + eps, allow_singular=True).logpdf(yhat_ref)
          - mvn(yhat_ref.mean(0), np.cov(yhat_ref.T) + eps, allow_singular=True).logpdf(yhat_ref))
    lr -= lr.max()
    w = np.exp(lr)
    w = np.minimum(w, np.quantile(w, clip_q))
    return w / w.mean()


def ess(w: np.ndarray) -> float:
    return float(w.sum() ** 2 / (w ** 2).sum() / len(w))


def fit_tlma_map(C0: list[np.ndarray], Cd: list[np.ndarray], lam: float, seed: int = 0) -> np.ndarray:
    """argmin_A  sum_tau ||A Cd(tau) A^T - C0(tau)||^2 / ||C0(tau)||^2  +  lam ||A - I||^2 / k."""
    import torch
    k = C0[0].shape[0]
    torch.manual_seed(seed)
    A = torch.eye(k, dtype=torch.float64, requires_grad=True)
    I = torch.eye(k, dtype=torch.float64)
    c0s = [torch.tensor(np.asarray(c, np.float64)) for c in C0]
    cds = [torch.tensor(np.asarray(c, np.float64)) for c in Cd]
    norms = [float((c ** 2).sum()) for c in C0]
    opt = torch.optim.LBFGS([A], max_iter=500, line_search_fn="strong_wolfe")

    def closure():
        opt.zero_grad()
        loss = sum(((A @ c @ A.T - c0) ** 2).sum() / n for c, c0, n in zip(cds, c0s, norms))
        loss = loss + lam * ((A - I) ** 2).sum() / k
        loss.backward()
        return loss

    opt.step(closure)
    return A.detach().numpy()


class TLMA(LatentBase):
    """Time-Lagged Moment Alignment (this repo). Project new-day activity into the reference PCA
    space, then learn a k x k map A so the new day's lagged covariances C_d(tau) match the
    reference's C_0(tau) for several lags, with a ridge pull toward the identity.

    Covariance at lag 0 alone only fixes A up to a rotation; adding lagged (dynamical) moments breaks
    that ambiguity, the same identifiability argument as AMUSE/SOBI blind source separation.
    """
    name = "tlma"

    def fit_reference(self, ref):
        super().fit_reference(ref)
        self.lags = self.kw.get("lags", (0, 1, 2, 4, 8, 16))
        self.C0 = lagged_covs(self.ref_latents, self.lags)

    def adapt(self, blocks_X, blocks_Y=None, blocks_m=None):
        super().adapt(blocks_X)
        Ld = np.concatenate([self._latent((smooth(X) - self.mu) / self.sd) for X in blocks_X])
        self.A = fit_tlma_map(self.C0, lagged_covs(Ld, self.lags), self.kw.get("lam", 1.0), self.seed)

    def _day_latent(self, Z):
        return self._latent(Z) @ self.A.T


class BRTLMA(TLMA):
    """Behaviour-reweighted TLMA (this repo): like TLMA, but the reference moments are recomputed
    with weights that make the reference's decoded-behaviour distribution match today's, so a short
    block that covers only some movements is not forced onto moments of all movements."""
    name = "br_tlma"

    def adapt(self, blocks_X, blocks_Y=None, blocks_m=None):
        LatentBase.adapt(self, blocks_X)
        Ld = np.concatenate([self._latent((smooth(X) - self.mu) / self.sd) for X in blocks_X])
        w = behaviour_weights(self.wf.predict(self.ref_latents), self.wf.predict(Ld), self.kw.get("clip_q", 0.99))
        self.ess = ess(w)
        C0w = lagged_covs(self.ref_latents, self.lags, w)
        self.A = fit_tlma_map(C0w, lagged_covs(Ld, self.lags), self.kw.get("lam", 1.0), self.seed)


class CovAlign(TLMA):
    """Ablation of TLMA with lag 0 only (second-moment matching, CORAL-like)."""
    name = "cov_align"

    def fit_reference(self, ref):
        self.kw["lags"] = (0,)
        super().fit_reference(ref)


REGISTRY = {c.name: c for c in [FrozenHeldInNorm, FrozenDayZscore, FewShotPooled, FewShotDayOnly,
                               LatentBase, FAProcrustes, TLMA, BRTLMA, CovAlign]}


def _register_optional():
    from .nomad import GRUAug, GRUBRTLMA, GRUFewShot, GRUFrozen, GRUTLMA, NoMADStyle
    for c in (NoMADStyle, GRUFrozen, GRUFewShot, GRUAug, GRUTLMA, GRUBRTLMA):
        REGISTRY[c.name] = c


_register_optional()
