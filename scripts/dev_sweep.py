"""Hyperparameter sweep on the dev split (held-in days only) and mechanical selection.

Writes results/<task>_dev_sweep.csv (every grid point, per day and seed) and, with --select,
configs/frozen_config.json: for each method the grid point with the highest mean dev R^2 (first in
grid order on ties; grids are ordered from most to least regularised). cov_align is an ablation
and copies tlma's selection.

Usage: python scripts/dev_sweep.py --task h1 [--select]
"""
import argparse
import itertools
import json
import pathlib
import warnings

import pandas as pd

from falcon_stability.methods import REGISTRY
from falcon_stability.protocol import make_episodes, run_method
from falcon_stability.provenance import git_state

warnings.filterwarnings("ignore")
ROOT = pathlib.Path(__file__).resolve().parents[1]
SWEEP_SEEDS = [0, 1]
DEV_DAYS = {"h1": 3, "m1": 2}


def grid(task):
    ks = [10, 20, 40]
    lams = [10.0, 1.0, 0.1, 0.01]
    return {
        "frozen_heldin_norm": [{}],
        "frozen_heldin_norm_clip5": [{}],
        "frozen_day_zscore": [{}],
        "fewshot_pooled": [{"day_weight": w} for w in (1, 10, 30)],
        "fewshot_day_only": [{}],
        "latent_frozen": [{"k": k} for k in ks],
        "fa_procrustes": [{"k": k} for k in ks],
        "tlma": [{"k": k, "lam": l} for k, l in itertools.product(ks, lams)],
        "br_tlma": [{"k": k, "lam": l} for k, l in itertools.product(ks, lams)],
        "gru_frozen": [{}],
        "gru_fewshot": [{"day_weight": w} for w in (1, 3, 10, 30)],
        "nomad_style": [{"beta": b} for b in (1.0, 0.1, 0.0)],
        "gru_aug": [{"augment": dict(gain=0.5, offset=0.5, drop=0.2)}, {"augment": dict(gain=0.3, offset=0.3, drop=0.1)}],
        "gru_tlma": [{"lam": l} for l in (10.0, 1.0, 0.1)],
        "gru_br_tlma": [{"lam": l} for l in (10.0, 1.0, 0.1)],
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--task", required=True, choices=["h1", "m1"])
    ap.add_argument("--select", action="store_true")
    a = ap.parse_args()
    eps = make_episodes(a.task, "dev", n_dev_days=DEV_DAYS[a.task])
    rows = []
    for name, points in grid(a.task).items():
        seeds = SWEEP_SEEDS if REGISTRY[name].stochastic else [0]
        for i, kw in enumerate(points):
            for seed in seeds:
                r = run_method(name, eps, drop_still=a.task == "h1", seed=seed, **kw)
                rows += [dict(row, point=i, params=json.dumps(kw, sort_keys=True)) for row in r]
            m = pd.DataFrame([x for x in rows if x["method"] == name and x["point"] == i]).r2.mean()
            print(f"{a.task} dev {name:26s} {json.dumps(kw):55s} {m:+.3f}", flush=True)
    df = pd.DataFrame(rows).assign(**git_state())
    df.to_csv(ROOT / "results" / f"{a.task}_dev_sweep.csv", index=False, float_format="%.6f")
    if a.select:
        p = ROOT / "configs" / "frozen_config.json"
        cfg = json.loads(p.read_text())
        means = df.groupby(["method", "point", "params"]).r2.mean().reset_index()
        chosen = {}
        for name in grid(a.task):
            g = means[means.method == name].sort_values("point")
            chosen[name] = json.loads(g.loc[g.r2.idxmax(), "params"])
        chosen["cov_align"] = {"k": chosen["tlma"]["k"], "lam": chosen["tlma"]["lam"]}
        order = list(grid(a.task)) + ["cov_align"]
        cfg["methods"][a.task] = {k: chosen[k] for k in order}
        p.write_text(json.dumps(cfg, indent=2) + "\n")
        print("selected", json.dumps(cfg["methods"][a.task]))


if __name__ == "__main__":
    main()
