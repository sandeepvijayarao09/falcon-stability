"""Run every method in configs/frozen_config.json on one task/protocol and write per-day rows.

Usage: python scripts/run_experiments.py --task h1 --split {test,minival,dev}
Output: results/<task>_<split>_rows.csv, overwritten in full by each run (rows are never merged
across code versions). Every row records the git SHA and whether src/scripts/configs were dirty.
Deterministic methods run once (seed 0); stochastic ones run for every configured seed.
"""
import argparse
import json
import pathlib
import time
import warnings

import pandas as pd

from falcon_stability.methods import REGISTRY
from falcon_stability.protocol import make_episodes, run_method
from falcon_stability.provenance import git_state

warnings.filterwarnings("ignore")
ROOT = pathlib.Path(__file__).resolve().parents[1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--task", required=True, choices=["h1", "m1"])
    ap.add_argument("--split", default="test", choices=["dev", "test", "minival"])
    ap.add_argument("--allow-dirty", action="store_true", help="permit uncommitted code (rows are flagged)")
    a = ap.parse_args()
    state = git_state()
    if state["code_dirty"] and not a.allow_dirty:
        raise SystemExit("uncommitted changes in src/scripts/configs; commit first or pass --allow-dirty")
    cfg = json.loads((ROOT / "configs" / "frozen_config.json").read_text())
    methods = cfg["methods"][a.task]
    episodes = make_episodes(a.task, a.split, adapt_frac=cfg["adapt_frac"], n_dev_days=cfg["dev_days"][a.task])
    rows = []
    for name, kw in methods.items():
        seeds = cfg["seeds"] if REGISTRY[name].stochastic else [0]
        for seed in seeds:
            t = time.time()
            r = run_method(name, episodes, drop_still=a.task == "h1", seed=seed, **kw)
            rows += r
            print(f"{a.task} {a.split} {name:26s} seed {seed}  mean R2 {pd.DataFrame(r).r2.mean():+.3f}  "
                  f"({time.time() - t:.0f}s)", flush=True)
    out = ROOT / "results" / f"{a.task}_{a.split}_rows.csv"
    pd.DataFrame(rows).assign(**state).to_csv(out, index=False, float_format="%.6f")
    print("wrote", out.relative_to(ROOT), state)


if __name__ == "__main__":
    main()
