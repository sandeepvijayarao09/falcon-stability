"""Run every method in configs/frozen_config.json on one task/split; write per-session rows.

Usage: python scripts/run_experiments.py --task h1 --split test [--methods a b] [--seeds 0 1]
Output: results/<task>_<split>_rows.csv
"""
import argparse
import json
import pathlib
import time
import warnings

import pandas as pd

from falcon_stability.protocol import make_split, run_method

warnings.filterwarnings("ignore")
ROOT = pathlib.Path(__file__).resolve().parents[1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--task", required=True)
    ap.add_argument("--split", default="test", choices=["dev", "test"])
    ap.add_argument("--methods", nargs="*")
    ap.add_argument("--seeds", nargs="*", type=int)
    a = ap.parse_args()
    cfg = json.loads((ROOT / "configs" / "frozen_config.json").read_text())
    methods = cfg["methods"][a.task]
    names = a.methods or list(methods)
    seeds = a.seeds if a.seeds is not None else cfg["seeds"]
    ref, days = make_split(a.task, a.split, n_dev_days=cfg["dev_days"][a.task])
    out = ROOT / "results" / f"{a.task}_{a.split}_rows.csv"
    old = pd.read_csv(out) if out.exists() else pd.DataFrame()
    rows = []
    for name in names:
        for seed in seeds:
            t = time.time()
            r = run_method(name, ref, days, adapt_frac=cfg["adapt_frac"], drop_still=a.task == "h1", seed=seed,
                           **methods[name])
            rows += r
            print(f"{a.task} {a.split} {name:20s} seed {seed}  mean R2 {pd.DataFrame(r).r2.mean():+.3f}  "
                  f"({time.time() - t:.0f}s)", flush=True)
    new = pd.DataFrame(rows)
    if len(old):
        old = old[~(old.method.isin(names) & old.seed.isin(seeds))]
    pd.concat([old, new]).to_csv(out, index=False, float_format="%.6f")
    print("wrote", out.relative_to(ROOT))


if __name__ == "__main__":
    main()
