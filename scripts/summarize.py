"""Turn results/<task>_<split>_rows.csv into the README table and figure.

Per session, R^2 is first averaged over seeds; the 95% CI is a percentile bootstrap over sessions
(H1: 14 held-out sessions on 7 days; M1: 3 sessions on 3 days, so M1 CIs are very coarse).
Delta columns are paired (same sessions) against the FALCON reference zero-shot WF.

Writes results/summary_<split>.csv, results/summary_<split>.md, figures/r2_vs_days.png (test only).
"""
import argparse
import pathlib

import matplotlib
import numpy as np
import pandas as pd

from falcon_stability.metrics import bootstrap_ci, paired_bootstrap_ci

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[1]
REF = "frozen_day_zscore"
LABELS = {
    "frozen_heldin_norm": ("Frozen WF, held-in normalisation (strict zero-shot)", "none"),
    "frozen_day_zscore": ("Frozen WF, per-day z-score (FALCON zero-shot reference)", "none"),
    "fewshot_pooled": ("WF few-shot: refit on held-in + today's labels", "labels"),
    "fewshot_day_only": ("WF few-shot: today's labels only", "labels"),
    "latent_frozen": ("PCA latents, frozen", "none"),
    "fa_procrustes": ("FA + Procrustes stabilizer (Degenhart 2020 style)", "unlabelled"),
    "cov_align": ("Covariance-only alignment (TLMA ablation, lag 0)", "unlabelled"),
    "tlma": ("TLMA: time-lagged moment alignment (ours)", "unlabelled"),
    "br_tlma": ("BR-TLMA: behaviour-reweighted TLMA (ours)", "unlabelled"),
    "gru_frozen": ("GRU dynamics backbone, frozen, per-day z-score", "none"),
    "gru_fewshot": ("GRU few-shot: readout refit with today's labels", "labels"),
    "nomad_style": ("NoMAD-style alignment (Karpowicz 2022, scaled down)", "unlabelled"),
    "gru_aug": ("GRU trained with drift augmentation (after Sussillo 2016)", "none"),
    "gru_tlma": ("GRU + TLMA (ours)", "unlabelled"),
    "gru_br_tlma": ("GRU + BR-TLMA (ours)", "unlabelled"),
}
FIG_SERIES = [  # (method, colour, linestyle, marker) - labelled methods dashed
    ("frozen_day_zscore", "#2a78d6", "-", "o"),
    ("fewshot_pooled", "#eb6834", "--", "s"),
    ("gru_frozen", "#1baf7a", "-", "^"),
    ("gru_fewshot", "#eda100", "--", "D"),
    ("nomad_style", "#e87ba4", "-", "v"),
    ("gru_br_tlma", "#008300", "-", "P"),
]


def summarize(task, split):
    df = pd.read_csv(ROOT / "results" / f"{task}_{split}_rows.csv")
    per = df.groupby(["method", "session"]).r2.mean().unstack("session")
    seed_sd = df.groupby(["method", "seed"]).r2.mean().groupby("method").std().fillna(0)
    rows = []
    for m in per.index:
        mean, lo, hi = bootstrap_ci(per.loc[m].values)
        d, dlo, dhi = paired_bootstrap_ci(per.loc[m].values, per.loc[REF].values)
        rows.append(dict(task=task, method=m, label=LABELS[m][0], uses=LABELS[m][1], r2=mean, ci_lo=lo, ci_hi=hi,
                         seed_sd=seed_sd[m], delta_vs_ref=d, delta_lo=dlo, delta_hi=dhi, n_sessions=per.shape[1]))
    order = list(LABELS)
    return pd.DataFrame(rows).sort_values("method", key=lambda s: s.map(order.index)), df


def fmt(r):
    return f"{r.r2:+.3f} [{r.ci_lo:+.3f}, {r.ci_hi:+.3f}]"


def fmt_d(r):
    return "-" if r.method == REF else f"{r.delta_vs_ref:+.3f} [{r.delta_lo:+.3f}, {r.delta_hi:+.3f}]"


def figure(raw):
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2), dpi=160)
    for ax, task in zip(axes, ["h1", "m1"]):
        d = raw[raw.task == task]
        for m, c, ls, mk in FIG_SERIES:
            g = d[d.method == m].groupby("days_since").r2
            x, y = g.mean().index.values, g.mean().values
            ax.plot(x, y, ls, color=c, lw=2, marker=mk, ms=7, label=LABELS[m][0],
                    markeredgecolor="#fcfcfb", markeredgewidth=1.2)
        ax.set_title({"h1": "H1 (human, 7-DoF reach, 176 ch)", "m1": "M1 (monkey, 16 EMG, 64 ch)"}[task],
                     loc="left", fontsize=11, color="#0b0b0b")
        ax.set_xlabel("Days since last calibration (held-in) day", color="#52514e")
        ax.axhline(0, color="#52514e", lw=0.8, alpha=0.5)
        ax.grid(axis="y", color="#e6e5e1", lw=0.8)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        ax.tick_params(colors="#52514e")
        ax.set_facecolor("#fcfcfb")
    axes[0].set_ylabel("Variance-weighted R² (eval half of each held-out file)", color="#52514e")
    h, l = axes[0].get_legend_handles_labels()
    fig.legend(h, l, loc="lower center", ncol=2, frameon=False, fontsize=8.5, bbox_to_anchor=(0.5, -0.12))
    fig.patch.set_facecolor("#fcfcfb")
    fig.tight_layout()
    out = ROOT / "figures" / "r2_vs_days.png"
    fig.savefig(out, bbox_inches="tight", facecolor="#fcfcfb")
    print("wrote", out.relative_to(ROOT))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--split", default="test")
    a = ap.parse_args()
    tabs, raws = [], []
    for task in ["h1", "m1"]:
        p = ROOT / "results" / f"{task}_{a.split}_rows.csv"
        if p.exists():
            t, r = summarize(task, a.split)
            tabs.append(t)
            raws.append(r.assign(task=task))
    tab = pd.concat(tabs)
    tab.to_csv(ROOT / "results" / f"summary_{a.split}.csv", index=False, float_format="%.4f")
    wide = tab.pivot(index="method", columns="task")
    lines = ["| Method | Uses today's | H1 R² [95% CI] | H1 Δ vs FALCON zero-shot | M1 R² [95% CI] | M1 Δ vs FALCON zero-shot |",
             "|---|---|---|---|---|---|"]
    for m in LABELS:
        if m not in wide.index:
            continue
        cells = []
        for task in ["h1", "m1"]:
            r = tab[(tab.task == task) & (tab.method == m)]
            cells += [fmt(r.iloc[0]), fmt_d(r.iloc[0])] if len(r) else ["n/a", "n/a"]
        lines.append(f"| {LABELS[m][0]} | {LABELS[m][1]} | " + " | ".join(cells) + " |")
    md = "\n".join(lines) + "\n"
    (ROOT / "results" / f"summary_{a.split}.md").write_text(md)
    print(md)
    if a.split == "test":
        figure(pd.concat(raws))


if __name__ == "__main__":
    main()
