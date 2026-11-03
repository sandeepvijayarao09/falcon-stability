"""Is behaviour stationary within a held-out calibration file? (H1 motivation for BR-TLMA.)

For each held-out file, compare the share of movement variance carried by each DoF in the
adaptation half vs the evaluation half (masked, moving bins). Writes results/behaviour_shift.json.
"""
import json
import pathlib

import numpy as np

from falcon_stability.data import load_split

ROOT = pathlib.Path(__file__).resolve().parents[1]


def dof_share(Y):
    v = Y.var(0)
    return v / v.sum()


out = {}
for task in ["h1", "m1"]:
    rows = []
    for s in load_split(task, "held_out_calib"):
        c = len(s.X) // 2
        a, e = s.Y[:c][s.mask[:c]], s.Y[c:][s.mask[c:]]
        pa, pe = dof_share(a), dof_share(e)
        rows.append(dict(session=s.name, tv_distance=float(0.5 * np.abs(pa - pe).sum()),
                         adapt_share=pa.round(3).tolist(), eval_share=pe.round(3).tolist()))
    tv = [r["tv_distance"] for r in rows]
    out[task] = dict(mean_tv=float(np.mean(tv)), min_tv=float(np.min(tv)), max_tv=float(np.max(tv)), sessions=rows)
    print(f"{task}: total-variation distance between per-DoF variance shares (adapt vs eval half): "
          f"mean {np.mean(tv):.2f}, range {np.min(tv):.2f}-{np.max(tv):.2f}")
(ROOT / "results" / "behaviour_shift.json").write_text(json.dumps(out, indent=1))
