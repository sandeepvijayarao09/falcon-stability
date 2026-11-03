"""NoMAD-style unsupervised alignment (Karpowicz et al. 2022, bioRxiv), scaled down for a laptop.

Reference day: a causal GRU dynamics model reads z-scored smoothed rates through an input
alignment layer (identity on held-in) and predicts next-bin spike counts with a Poisson readout.
A ridge decoder maps GRU states to behaviour. New day: freeze the GRU and decoder, and train only
the affine input alignment and the Poisson readout on unlabelled data, minimising
  Poisson NLL + beta * KL( N(mu_d, S_d) || N(mu_0, S_0) )   over GRU states,
with an L2 pull toward the reference parameters.

Simplifications vs the paper: GRU instead of LFADS (no inferred inputs / initial-condition encoder),
smoothed-rate inputs, Gaussian KL on hidden states instead of on factors.
"""
from __future__ import annotations

import copy

import numpy as np
import torch
import torch.nn as nn

from .decoders import WienerFilter, train_mask
from .features import smooth, zscore_stats
from .methods import Method, _zs_per_file


class Dyn(nn.Module):
    def __init__(self, C: int, H: int):
        super().__init__()
        self.align = nn.Linear(C, C)
        nn.init.eye_(self.align.weight)
        nn.init.zeros_(self.align.bias)
        self.gru = nn.GRU(C, H, batch_first=True)
        self.readout = nn.Linear(H, C)

    def forward(self, Z):
        h, _ = self.gru(self.align(Z))
        return h, self.readout(h)  # log-rates for the NEXT bin


def gauss_stats(h: torch.Tensor):
    h = h.reshape(-1, h.shape[-1])
    mu = h.mean(0)
    c = h - mu
    return mu, c.T @ c / (len(h) - 1) + 1e-3 * torch.eye(h.shape[-1], dtype=h.dtype)


def gauss_kl(mu0, S0, mu1, S1):
    """KL(N0 || N1)."""
    k = len(mu0)
    S1i = torch.linalg.inv(S1)
    d = mu1 - mu0
    return 0.5 * (torch.trace(S1i @ S0) + d @ S1i @ d - k + torch.logdet(S1) - torch.logdet(S0))


def chunks(Z, X, L, rng, n):
    T = len(Z)
    idx = rng.integers(0, T - L - 1, n)
    zb = np.stack([Z[i:i + L] for i in idx])
    xb = np.stack([X[i + 1:i + L + 1] for i in idx])
    return torch.tensor(zb, dtype=torch.float32), torch.tensor(xb, dtype=torch.float32)


def full_states(net: Dyn, Z: np.ndarray) -> np.ndarray:
    with torch.no_grad():
        h, _ = net(torch.tensor(Z[None], dtype=torch.float32))
    return h[0].numpy()


def drift_augment(zb, rng, gain=0.3, offset=0.3, drop=0.1):
    """Simulate cross-day input drift on z-scored rates, one draw per sequence: per-channel
    multiplicative gain, additive offset and dropped channels (after Sussillo et al. 2016)."""
    B, _, C = zb.shape
    g = torch.tensor(np.exp(rng.normal(0, gain, (B, 1, C))), dtype=zb.dtype)
    o = torch.tensor(rng.normal(0, offset, (B, 1, C)), dtype=zb.dtype)
    keep = torch.tensor(rng.random((B, 1, C)) > drop, dtype=zb.dtype)
    return (zb * g + o) * keep


class NoMADStyle(Method):
    name = "nomad_style"

    def fit_reference(self, ref):
        torch.manual_seed(self.seed)
        rng = np.random.default_rng(self.seed)
        H = self.kw.get("hidden", 64)
        L = self.kw.get("seq_len", 100)
        Zs = _zs_per_file([X for X, _, _ in ref])
        Xs = [X.astype(np.float32) for X, _, _ in ref]
        net = Dyn(Zs[0].shape[1], H)
        for p in net.align.parameters():
            p.requires_grad_(False)  # identity on reference data
        opt = torch.optim.Adam([p for p in net.parameters() if p.requires_grad], lr=3e-3)
        w = np.array([len(z) for z in Zs], float)
        w /= w.sum()
        for step in range(self.kw.get("steps", 1500)):
            f = rng.choice(len(Zs), p=w)
            zb, xb = chunks(Zs[f], Xs[f], L, rng, 32)
            if self.kw.get("augment"):
                zb = drift_augment(zb, rng, **self.kw["augment"])
            _, lr = net(zb)
            loss = nn.functional.poisson_nll_loss(lr[:, 10:], xb[:, 10:], log_input=True)  # skip GRU burn-in
            opt.zero_grad()
            loss.backward()
            opt.step()
        net.eval()
        self.net0 = net
        Hs = [full_states(net, z) for z in Zs]
        Hcat = np.concatenate(Hs)
        self.mu0, self.S0 = [t.detach() for t in gauss_stats(torch.tensor(Hcat, dtype=torch.float64))]
        Y = np.concatenate([y for _, y, _ in ref])
        m = train_mask(Y, np.concatenate([mm for _, _, mm in ref]), self.drop_still)
        self.wf = WienerFilter(self.history, self.kw.get("alpha")).fit(Hcat, Y, m)
        self.net = net

    def adapt(self, blocks_X, blocks_Y=None, blocks_m=None):
        torch.manual_seed(self.seed)
        rng = np.random.default_rng(self.seed)
        self.mu, self.sd = zscore_stats(np.concatenate([smooth(X) for X in blocks_X]))
        Zs = [(smooth(X) - self.mu) / self.sd for X in blocks_X]
        Xs = [X.astype(np.float32) for X in blocks_X]
        net = copy.deepcopy(self.net0)
        for p in net.gru.parameters():
            p.requires_grad_(False)
        for p in list(net.align.parameters()) + list(net.readout.parameters()):
            p.requires_grad_(True)
        ref_params = [p.detach().clone() for p in list(net.align.parameters()) + list(net.readout.parameters())]
        train = list(net.align.parameters()) + list(net.readout.parameters())
        opt = torch.optim.Adam(train, lr=self.kw.get("adapt_lr", 1e-3))
        beta, l2 = self.kw.get("beta", 0.1), self.kw.get("l2", 1e-2)
        L = min(self.kw.get("seq_len", 100), min(len(z) for z in Zs) - 2)
        for step in range(self.kw.get("adapt_steps", 300)):
            f = rng.integers(len(Zs))
            zb, xb = chunks(Zs[f], Xs[f], L, rng, 16)
            h, lr = net(zb)
            nll = nn.functional.poisson_nll_loss(lr[:, 10:], xb[:, 10:], log_input=True)
            mu, S = gauss_stats(h[:, 10:].double())
            kl = gauss_kl(mu, S, self.mu0, self.S0)
            reg = sum(((p - q) ** 2).sum() for p, q in zip(train, ref_params))
            loss = nll + beta * kl.float() / h.shape[-1] + l2 * reg
            opt.zero_grad()
            loss.backward()
            opt.step()
        net.eval()
        self.net = net

    def predict(self, X):
        return self.wf.predict(full_states(self.net, (smooth(X) - self.mu) / self.sd))


class GRUFrozen(NoMADStyle):
    """Ablation: same GRU + decoder, per-day z-score only (no alignment training)."""
    name = "gru_frozen"

    def adapt(self, blocks_X, blocks_Y=None, blocks_m=None):
        self.mu, self.sd = zscore_stats(np.concatenate([smooth(X) for X in blocks_X]))
        self.net = self.net0


class GRUFewShot(GRUFrozen):
    """Labelled recalibration of the GRU pipeline: refit the ridge readout from GRU states on
    held-in states pooled with today's labelled block (weight `day_weight`)."""
    name = "gru_fewshot"
    needs_labels = True

    def fit_reference(self, ref):
        super().fit_reference(ref)
        Zs = _zs_per_file([X for X, _, _ in ref])
        self.Href = np.concatenate([full_states(self.net0, z) for z in Zs])
        self.Yref = np.concatenate([y for _, y, _ in ref])
        self.mref = train_mask(self.Yref, np.concatenate([mm for _, _, mm in ref]), self.drop_still)

    def adapt(self, blocks_X, blocks_Y=None, blocks_m=None):
        super().adapt(blocks_X)
        Hd = np.concatenate([full_states(self.net0, (smooth(X) - self.mu) / self.sd) for X in blocks_X])
        Yd = np.concatenate(blocks_Y)
        md = train_mask(Yd, np.concatenate(blocks_m), self.drop_still)
        w = self.kw.get("day_weight", 10)
        self.wf = WienerFilter(self.history, self.kw.get("alpha")).fit(
            np.concatenate([self.Href] + [Hd] * w), np.concatenate([self.Yref] + [Yd] * w),
            np.concatenate([self.mref] + [md] * w))

    def predict(self, X):
        return self.wf.predict(full_states(self.net0, (smooth(X) - self.mu) / self.sd))


class GRUAug(GRUFrozen):
    """Zero-shot GRU trained with simulated drift (label-free at test time: per-day z-score only)."""
    name = "gru_aug"

    def fit_reference(self, ref):
        self.kw.setdefault("augment", dict(gain=0.3, offset=0.3, drop=0.1))
        super().fit_reference(ref)


class GRUTLMA(GRUFrozen):
    """TLMA in GRU-state space: align PCA(k) of the day's GRU states to the reference with lagged
    covariances; decode from the re-mapped states."""
    name = "gru_tlma"

    def fit_reference(self, ref):
        from sklearn.decomposition import PCA
        from .methods import lagged_covs
        super().fit_reference(ref)
        Zs = _zs_per_file([X for X, _, _ in ref])
        Href = np.concatenate([full_states(self.net0, z) for z in Zs])
        self.k = self.kw.get("k", 32)
        self.pca = PCA(self.k, random_state=self.seed).fit(Href)
        self.lags = self.kw.get("lags", (0, 1, 2, 4, 8, 16))
        self.C0 = lagged_covs(self.pca.transform(Href), self.lags)

    def adapt(self, blocks_X, blocks_Y=None, blocks_m=None):
        from .methods import fit_tlma_map, lagged_covs
        super().adapt(blocks_X)
        Ld = np.concatenate([self.pca.transform(full_states(self.net0, (smooth(X) - self.mu) / self.sd))
                             for X in blocks_X])
        self.A = fit_tlma_map(self.C0, lagged_covs(Ld, self.lags), self.kw.get("lam", 10.0), self.seed)

    def predict(self, X):
        H = full_states(self.net0, (smooth(X) - self.mu) / self.sd)
        L = self.pca.transform(H)
        H2 = H + (L @ self.A.T - L) @ self.pca.components_  # replace the top-k subspace component
        return self.wf.predict(H2)


class GRUBRTLMA(GRUTLMA):
    """Behaviour-reweighted TLMA in GRU-state space (this repo)."""
    name = "gru_br_tlma"

    def fit_reference(self, ref):
        super().fit_reference(ref)
        Zs = _zs_per_file([X for X, _, _ in ref])
        self.Href = np.concatenate([full_states(self.net0, z) for z in Zs])
        self.yhat_ref = self.wf.predict(self.Href)

    def adapt(self, blocks_X, blocks_Y=None, blocks_m=None):
        from .methods import behaviour_weights, ess, fit_tlma_map, lagged_covs
        GRUFrozen.adapt(self, blocks_X)
        Hd = np.concatenate([full_states(self.net0, (smooth(X) - self.mu) / self.sd) for X in blocks_X])
        w = behaviour_weights(self.yhat_ref, self.wf.predict(Hd), self.kw.get("clip_q", 0.99))
        self.ess = ess(w)
        self.fallback = bool(np.all(w == 1))
        C0w = lagged_covs(self.pca.transform(self.Href), self.lags, w)
        self.A = fit_tlma_map(C0w, lagged_covs(self.pca.transform(Hd), self.lags), self.kw.get("lam", 10.0), self.seed)
