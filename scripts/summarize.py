"""Turn results/<task>_<split>_rows.csv into tables and figures. Deterministic: CI regenerates
results/summary_*.md from the committed rows and fails on any diff.

Statistics
- Unit of analysis: a day (FALCON scores per day). Stochastic methods are first averaged over seeds.
- H1: mean over days with a 95% percentile bootstrap over days (test n=7, minival n=5), paired
  differences vs the reference row with bootstrap CI, and sign counts (days better / all days).
- M1: only 3 days per protocol, so no CIs: per-day values and sign counts.
- Seed SD (SD over seeds of the day-mean) only for stochastic methods.
- Parent comparisons are paired by seed AND day (e.g. GRU+TLMA seed s vs GRU frozen seed s share
  the same trained GRU).

Writes results/summary_<split>.md, results/summary_<split>.csv,
figures/m1_by_day.png and figures/h1_by_day_supplement.png (test + minival present).
"""
import argparse
import pathlib

import matplotlib
import numpy as np
import pandas as pd

from falcon_stability.metrics import bootstrap_ci
from falcon_stability.methods import REGISTRY

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[1]
REF = "frozen_day_zscore"
LABELS = {
    "frozen_heldin_norm": ("Frozen WF, held-in normalisation", "nothing"),
    "frozen_heldin_norm_clip5": ("Frozen WF, held-in normalisation, z clipped to ±5", "nothing"),
    "frozen_day_zscore": ("Frozen WF, per-day z-score (FALCON-style zero-shot)", "unlabelled (norm. stats)"),
    "fewshot_pooled": ("WF few-shot: refit on held-in + today's labels", "labels"),
    "fewshot_day_only": ("WF few-shot: today's labels only", "labels"),
    "latent_frozen": ("PCA latents, frozen, per-day z-score", "unlabelled (norm. stats)"),
    "fa_procrustes": ("FA + Procrustes (Degenhart 2020 style)", "unlabelled"),
    "cov_align": ("Covariance-only alignment (lag 0)", "unlabelled"),
    "tlma": ("TLMA: time-lagged moment alignment", "unlabelled"),
    "br_tlma": ("BR-TLMA: behaviour-reweighted TLMA", "unlabelled"),
    "gru_frozen": ("GRU backbone, frozen, per-day z-score", "unlabelled (norm. stats)"),
    "gru_fewshot": ("GRU few-shot: readout refit with today's labels", "labels"),
    "nomad_style": ("NoMAD-style alignment (scaled down)", "unlabelled"),
    "gru_aug": ("GRU trained with drift augmentation (after Sussillo 2016)", "unlabelled (norm. stats)"),
    "gru_tlma": ("GRU + TLMA", "unlabelled"),
    "gru_br_tlma": ("GRU + BR-TLMA", "unlabelled"),
}
PARENTS = [  # (child, parent): the child adds exactly one component to the parent
    ("frozen_day_zscore", "frozen_heldin_norm"),
    ("frozen_heldin_norm_clip5", "frozen_heldin_norm"),
    ("fewshot_pooled", "frozen_day_zscore"),
    ("cov_align", "latent_frozen"),
    ("tlma", "latent_frozen"),
    ("tlma", "cov_align"),
    ("br_tlma", "tlma"),
    ("gru_fewshot", "gru_frozen"),
    ("nomad_style", "gru_frozen"),
    ("gru_tlma", "gru_frozen"),
    ("gru_br_tlma", "gru_tlma"),
    ("gru_frozen", "frozen_day_zscore"),
]
FIG_SERIES = [  # (method, colour, marker); labelled methods get hollow markers
    ("frozen_day_zscore", "#2a78d6", "o"),
    ("fewshot_pooled", "#eb6834", "s"),
    ("gru_frozen", "#1baf7a", "^"),
    ("gru_fewshot", "#eda100", "D"),
    ("nomad_style", "#e87ba4", "v"),
    ("gru_tlma", "#008300", "P"),
]


def load(task, split):
    p = ROOT / "results" / f"{task}_{split}_rows.csv"
    return pd.read_csv(p) if p.exists() else None


def day_table(df):
    """method x day matrix of seed-averaged R^2."""
    return df.groupby(["method", "day"]).r2.mean().unstack("day")


def seed_sd(df, m):
    if not REGISTRY[m].stochastic:
        return np.nan
    return df[df.method == m].groupby("seed").r2.mean().std()


def fmt(x, nd=3):
    return "–" if x is None or (isinstance(x, float) and np.isnan(x)) else f"{x:+.{nd}f}"


def main_table(task, split, df):
    D = day_table(df)
    days = list(D.columns)
    rows, md = [], []
    if task == "h1":
        md += [f"| Method | Uses today's | R² mean [95% CI over {len(days)} days] | Δ vs FALCON-style [95% CI] | days > ref | seed SD |",
               "|---|---|---|---|---|---|"]
    else:
        md += ["| Method | Uses today's | " + " | ".join(f"{d} (+{int(df[df.day == d].days_since.iloc[0])} d)" for d in days)
               + " | mean | days > ref | seed SD |", "|---|---|" + "---|" * (len(days) + 3)]
    for m in LABELS:
        if m not in D.index:
            continue
        v, ref = D.loc[m].values, D.loc[REF].values
        sd = seed_sd(df, m)
        wins = "–" if m == REF else f"{int((v > ref).sum())}/{len(v)}"
        mean, lo, hi = bootstrap_ci(v)
        d, dlo, dhi = bootstrap_ci(v - ref)
        rows.append(dict(task=task, split=split, method=m, r2=mean, ci_lo=lo, ci_hi=hi, delta=d, delta_lo=dlo,
                         delta_hi=dhi, wins=wins, seed_sd=sd, n_days=len(v), **{f"day_{k}": x for k, x in zip(days, v)}))
        if task == "h1":
            delta = "–" if m == REF else f"{fmt(d)} [{fmt(dlo)}, {fmt(dhi)}]"
            md.append(f"| {LABELS[m][0]} | {LABELS[m][1]} | {fmt(mean)} [{fmt(lo)}, {fmt(hi)}] | {delta} | {wins} | {fmt(sd)} |")
        else:
            md.append(f"| {LABELS[m][0]} | {LABELS[m][1]} | " + " | ".join(fmt(x) for x in v)
                      + f" | {fmt(mean)} | {wins} | {fmt(sd)} |")
    return pd.DataFrame(rows), md


def parent_table(task, df):
    md = ["| Comparison | mean Δ R² | pairs better (seed×day) | days better (seed-avg) |" + (" 95% CI over days |" if task == "h1" else ""),
          "|---|---|---|---|" + ("---|" if task == "h1" else "")]
    for child, parent in PARENTS:
        if child not in set(df.method) or parent not in set(df.method):
            continue
        a = df[df.method == child].set_index(["seed", "day"]).r2
        b = df[df.method == parent].set_index(["seed", "day"]).r2
        if not REGISTRY[child].stochastic or not REGISTRY[parent].stochastic:
            a = a.groupby("day").mean()  # deterministic side: compare seed-averaged per day
            b = b.groupby("day").mean()
        j = pd.concat([a.rename("a"), b.rename("b")], axis=1).dropna()
        diff = j.a - j.b
        per_day = diff.groupby("day").mean() if "seed" in diff.index.names else diff
        line = (f"| {LABELS[child][0]} vs {LABELS[parent][0]} | {fmt(diff.mean())} | "
                f"{int((diff > 0).sum())}/{len(diff)} | {int((per_day > 0).sum())}/{len(per_day)} |")
        if task == "h1":
            _, lo, hi = bootstrap_ci(per_day.values)
            line += f" [{fmt(lo)}, {fmt(hi)}] |"
        md.append(line)
    return md


def diag_table(frames):
    md = ["| Task | Protocol | Method | ‖A−I‖_F (mean, range) | per-dim ‖A−I‖_F/√k | ESS (mean) | fallback rate |",
          "|---|---|---|---|---|---|---|"]
    for (task, split), df in frames.items():
        for m in ["cov_align", "tlma", "br_tlma", "gru_tlma", "gru_br_tlma"]:
            g = df[df.method == m]
            if not len(g) or "A_minus_I_fro" not in g:
                continue
            a = g.A_minus_I_fro
            ess = f"{g.ess.mean():.2f}" if "ess" in g and g.ess.notna().any() else "–"
            fb = f"{int(g.fallback.fillna(False).astype(bool).sum())}/{len(g)}" if "fallback" in g and g.fallback.notna().any() else "–"
            md.append(f"| {task} | {split} | {LABELS[m][0]} | {a.mean():.3f} ({a.min():.3f}–{a.max():.3f}) | "
                      f"{g.A_minus_I_rel.mean():.3f} | {ess} | {fb} |")
    return md


def plot_by_day(ax, df, title):
    methods = [s for s in FIG_SERIES if s[0] in set(df.method)]
    days = sorted(df.days_since.unique())
    width = 0.8 if len(days) > 3 else 1.6
    for i, (m, c, mk) in enumerate(methods):
        g = df[df.method == m]
        per = g.groupby(["days_since", "seed"]).r2.mean().groupby("days_since")
        x = np.array(list(per.groups)) + (i - (len(methods) - 1) / 2) * width / len(methods)
        y = per.mean().values
        err = per.std().fillna(0).values if REGISTRY[m].stochastic else None
        hollow = REGISTRY[m].needs_labels
        ax.errorbar(x, y, yerr=err, fmt=mk, color=c, ms=7, capsize=3, lw=1.2, linestyle="none",
                    mfc="#fcfcfb" if hollow else c, mec=c, mew=1.6, label=LABELS[m][0] + (" (labels)" if hollow else ""))
    ax.set_title(title, loc="left", fontsize=10.5, color="#0b0b0b")
    ax.set_xlabel("Days since last calibration (training) day", color="#52514e")
    ax.axhline(0, color="#52514e", lw=0.8, alpha=0.5)
    ax.grid(axis="y", color="#e6e5e1", lw=0.8)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.tick_params(colors="#52514e")
    ax.set_facecolor("#fcfcfb")


def figures(frames):
    style = dict(facecolor="#fcfcfb")
    if ("m1", "test") in frames:
        fig, ax = plt.subplots(figsize=(7.5, 4.2), dpi=160)
        plot_by_day(ax, frames[("m1", "test")], "M1 held-out days (monkey, 16 EMG, 64 ch): seed mean ± SD")
        ax.set_ylabel("Variance-weighted R² (per day)", color="#52514e")
        ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.18), ncol=2, frameon=False, fontsize=8)
        fig.patch.set_facecolor("#fcfcfb")
        fig.savefig(ROOT / "figures" / "m1_by_day.png", bbox_inches="tight", **style)
        plt.close(fig)
    panels = [k for k in [("h1", "test"), ("h1", "minival")] if k in frames]
    if panels:
        fig, axes = plt.subplots(1, len(panels), figsize=(6 * len(panels), 4.2), dpi=160, squeeze=False)
        names = {"test": "H1 held-out days, local split (uninformative, see README)",
                 "minival": "H1 minival protocol (held-in days scored on minival)"}
        for ax, k in zip(axes[0], panels):
            plot_by_day(ax, frames[k], names[k[1]])
        axes[0][0].set_ylabel("Variance-weighted R² (per day)", color="#52514e")
        h, lab = axes[0][0].get_legend_handles_labels()
        fig.legend(h, lab, loc="lower center", ncol=3, frameon=False, fontsize=8, bbox_to_anchor=(0.5, -0.1))
        fig.patch.set_facecolor("#fcfcfb")
        fig.tight_layout()
        fig.savefig(ROOT / "figures" / "h1_by_day_supplement.png", bbox_inches="tight", **style)
        plt.close(fig)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-figures", action="store_true")
    a = ap.parse_args()
    frames = {}
    for split in ["test", "minival", "dev"]:
        out_md, out_rows = [], []
        for task in ["m1", "h1"]:
            df = load(task, split)
            if df is None:
                continue
            frames[(task, split)] = df
            rows, md = main_table(task, split, df)
            out_rows.append(rows)
            out_md += [f"### {task.upper()} · {split}", "", *md, "", "Paired against the direct parent:", "",
                       *parent_table(task, df), ""]
            sha = ",".join(sorted(df.git_sha.astype(str).unique())) if "git_sha" in df else "?"
            dirty = bool(df.code_dirty.any()) if "code_dirty" in df else None
            out_md += [f"_rows from git {sha}; uncommitted code: {dirty}_", ""]
        if out_rows:
            pd.concat(out_rows).to_csv(ROOT / "results" / f"summary_{split}.csv", index=False, float_format="%.4f")
            (ROOT / "results" / f"summary_{split}.md").write_text("\n".join(out_md))
    (ROOT / "results" / "diagnostics.md").write_text("\n".join(diag_table(frames)) + "\n")
    if not a.no_figures:
        figures(frames)
    print("wrote summaries for", sorted(frames))


if __name__ == "__main__":
    main()
