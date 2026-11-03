"""Fit a submission payload on all held-in calibration data.

Usage: python scripts/build_submission.py --task h1 --method {wf,gru}
Output: submission/artifacts/<task>_<method>.pt
"""
import argparse
import pathlib
import warnings

import torch

from falcon_stability.submission import build_payload

warnings.filterwarnings("ignore")
ROOT = pathlib.Path(__file__).resolve().parents[1]

ap = argparse.ArgumentParser()
ap.add_argument("--task", required=True, choices=["h1", "m1", "m2"])
ap.add_argument("--method", required=True, choices=["wf", "gru"])
a = ap.parse_args()
out = ROOT / "submission" / "artifacts" / f"{a.task}_{a.method}.pt"
torch.save(build_payload(a.task, a.method), out)
print("wrote", out.relative_to(ROOT), f"{out.stat().st_size / 1e3:.0f} kB")
