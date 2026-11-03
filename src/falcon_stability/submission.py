"""FALCON EvalAI decoders: frozen Wiener filter and frozen GRU, both with per-day z-scoring.

`build_payload` fits on all held-in calibration data and stores, for every session FALCON may
evaluate (held-in and held-out), the per-day mean/SD of smoothed counts from that day's
*calibration* files. No calibration labels are used, so both decoders are zero-shot / label-free
in FALCON's terms (they use unlabelled calibration statistics only).

`StabilityDecoder` implements falcon_challenge.interface.BCIDecoder and runs online, one 20 ms
bin at a time: causal FIR smoothing buffer -> per-day z-score -> (GRU step) -> ridge readout.
"""
from __future__ import annotations

import pathlib
import warnings
from typing import List

import numpy as np
import torch

from falcon_challenge.config import FalconConfig, FalconTask
from falcon_challenge.interface import BCIDecoder

from .features import exp_kernel, smooth, zscore_stats


def _session_stats(task: str, cfg: FalconConfig, norm: str = "day_smoothed") -> dict:
    """hash_dataset key -> (mu, sd) from calibration files.

    norm="day_smoothed": smoothed counts pooled over the day's calibration files (the research pipeline).
    norm="file_raw": raw counts of each calibration file (the official sklearn demo's choice). Because the
    decoder is trained on smoothed-count z-scores, the larger raw SD shrinks predictions at test time.
    """
    from .data import group_by_day, load_split
    stats = {}
    for split in ("held_in_calib", "held_out_calib"):
        for _, files in group_by_day(load_split(task, split)).items():
            if norm == "file_raw":
                for s in files:
                    mu, sd = zscore_stats(s.X.astype(np.float64))
                    stats[cfg.hash_dataset(pathlib.Path(s.name))] = (mu.astype(np.float32), sd.astype(np.float32))
                continue
            mu, sd = zscore_stats(np.concatenate([smooth(s.X) for s in files]))
            for s in files:
                # minival files of a held-in session hash to the same key as its calibration file
                stats[cfg.hash_dataset(pathlib.Path(s.name))] = (mu.astype(np.float32), sd.astype(np.float32))
    return stats


def build_payload(task: str, method: str, seed: int = 0, norm: str = "day_smoothed") -> dict:
    from .data import load_split
    from .methods import REGISTRY
    ref = [(s.X, s.Y, s.mask) for s in load_split(task, "held_in_calib")]
    name = {"wf": "frozen_day_zscore", "gru": "gru_frozen"}[method]
    m = REGISTRY[name](drop_still=task == "h1", seed=seed)
    m.fit_reference(ref)
    cfg = FalconConfig(task=getattr(FalconTask, task))
    payload = {"task": task, "method": method, "seed": seed, "norm": norm, "stats": _session_stats(task, cfg, norm),
               "coef": m.wf.model.coef_.astype(np.float32), "intercept": m.wf.model.intercept_.astype(np.float32),
               "history": m.wf.history}
    if m.wf.history != 0:
        raise NotImplementedError("online decoder supports history=0 (the configured setting)")
    if method == "gru":
        payload["gru_state"] = {k: v.cpu() for k, v in m.net0.state_dict().items()}
        payload["hidden"] = m.net0.gru.hidden_size
    return payload


class StabilityDecoder(BCIDecoder):
    def __init__(self, task_config: FalconConfig, payload_path: str, batch_size: int = 1):
        super().__init__(task_config=task_config, batch_size=batch_size)
        p = torch.load(payload_path, map_location="cpu", weights_only=False)
        self.p = p
        self.kernel = exp_kernel().astype(np.float32)[::-1].copy()  # oldest -> newest
        self.W, self.b = p["coef"].T, p["intercept"]
        C = task_config.n_channels
        self.net = None
        if p["method"] == "gru":
            from .nomad import Dyn
            self.net = Dyn(C, p["hidden"])
            self.net.load_state_dict(p["gru_state"])
            self.net.eval()
        self._alloc(batch_size)

    def _alloc(self, B):
        C = self._task_config.n_channels
        self.buf = np.zeros((B, len(self.kernel), C), np.float32)
        self.mu = np.zeros((B, C), np.float32)
        self.sd = np.ones((B, C), np.float32)
        self.h = None

    def set_batch_size(self, batch_size: int):
        self.batch_size = batch_size
        self._alloc(batch_size)

    def reset(self, dataset_tags: List[pathlib.Path] = [""]):
        self._alloc(self.batch_size)
        for i, tag in enumerate(dataset_tags):
            key = self._task_config.hash_dataset(pathlib.Path(tag))
            if key in self.p["stats"]:
                self.mu[i], self.sd[i] = self.p["stats"][key]
            else:  # unknown session: fall back to pooled stats of all known sessions (logged)
                warnings.warn(f"no calibration stats for {key}; using pooled stats")
                allmu = np.stack([v[0] for v in self.p["stats"].values()])
                allsd = np.stack([v[1] for v in self.p["stats"].values()])
                self.mu[i], self.sd[i] = allmu.mean(0), allsd.mean(0)

    def predict(self, neural_observations: np.ndarray) -> np.ndarray:
        x = np.asarray(neural_observations, np.float32)
        B = x.shape[0]
        if B < self.batch_size:
            x = np.pad(x, ((0, self.batch_size - B), (0, 0)))
        self.buf = np.roll(self.buf, -1, axis=1)
        self.buf[:, -1] = x
        z = (np.einsum("t,btc->bc", self.kernel, self.buf) - self.mu) / self.sd
        if self.net is not None:
            with torch.no_grad():
                out, self.h = self.net.gru(self.net.align(torch.from_numpy(z)[:, None, :]), self.h)
            z = out[:, 0].numpy()
        return (z @ self.W + self.b)[:B]

    def on_done(self, dones: np.ndarray):
        pass
