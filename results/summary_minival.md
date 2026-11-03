### M1-A · minival

| Method | Uses today's | 2012-09-26 (+2 d) | 2012-09-27 (+1 d) | 2012-09-28 (+1 d) | mean | days > ref | seed SD |
|---|---|---|---|---|---|---|---|
| Frozen WF, held-in normalisation | nothing | -1.097 | +0.091 | +0.073 | -0.311 | 0/3 | – |
| Frozen WF, held-in normalisation, z clipped to ±5 | nothing | -0.434 | +0.069 | +0.269 | -0.032 | 0/3 | – |
| Frozen WF, per-day z-score (FALCON-style zero-shot) | unlabelled (norm. stats) | +0.044 | +0.387 | +0.479 | +0.303 | – | – |
| WF few-shot: refit on held-in + today's labels | labels | +0.421 | +0.564 | +0.600 | +0.528 | 3/3 | – |
| WF few-shot: today's labels only | labels | +0.488 | +0.575 | +0.668 | +0.577 | 3/3 | – |
| PCA latents, frozen, per-day z-score | unlabelled (norm. stats) | +0.080 | +0.476 | +0.472 | +0.342 | 2/3 | – |
| FA + Procrustes (Degenhart 2020 style) | unlabelled | +0.211 | +0.428 | +0.521 | +0.387 | 3/3 | +0.010 |
| Covariance-only alignment (lag 0) | unlabelled | +0.119 | +0.478 | +0.479 | +0.359 | 2/3 | – |
| TLMA: time-lagged moment alignment | unlabelled | +0.108 | +0.466 | +0.481 | +0.351 | 3/3 | – |
| BR-TLMA: behaviour-reweighted TLMA | unlabelled | +0.132 | +0.422 | +0.472 | +0.342 | 2/3 | – |
| GRU backbone, frozen, per-day z-score | unlabelled (norm. stats) | -0.038 | +0.505 | +0.609 | +0.359 | 2/3 | +0.047 |
| GRU few-shot: readout refit with today's labels | labels | +0.441 | +0.582 | +0.682 | +0.568 | 3/3 | +0.012 |
| NoMAD-style alignment (scaled down) | unlabelled | +0.060 | +0.534 | +0.601 | +0.398 | 3/3 | +0.023 |
| GRU trained with drift augmentation (after Sussillo 2016) | unlabelled (norm. stats) | +0.012 | +0.545 | +0.619 | +0.392 | 2/3 | +0.039 |
| GRU + TLMA | unlabelled | +0.008 | +0.236 | +0.371 | +0.205 | 0/3 | +0.093 |
| GRU + BR-TLMA | unlabelled | -0.096 | +0.370 | +0.371 | +0.215 | 0/3 | +0.104 |

Paired against the direct parent:

| Comparison | mean Δ R² | pairs better (seed×day) | days better (seed-avg) |
|---|---|---|---|
| Frozen WF, per-day z-score (FALCON-style zero-shot) vs Frozen WF, held-in normalisation | +0.614 | 3/3 | 3/3 |
| Frozen WF, held-in normalisation, z clipped to ±5 vs Frozen WF, held-in normalisation | +0.279 | 2/3 | 2/3 |
| WF few-shot: refit on held-in + today's labels vs Frozen WF, per-day z-score (FALCON-style zero-shot) | +0.225 | 3/3 | 3/3 |
| Covariance-only alignment (lag 0) vs PCA latents, frozen, per-day z-score | +0.016 | 3/3 | 3/3 |
| TLMA: time-lagged moment alignment vs PCA latents, frozen, per-day z-score | +0.009 | 2/3 | 2/3 |
| TLMA: time-lagged moment alignment vs Covariance-only alignment (lag 0) | -0.007 | 1/3 | 1/3 |
| BR-TLMA: behaviour-reweighted TLMA vs TLMA: time-lagged moment alignment | -0.010 | 1/3 | 1/3 |
| GRU few-shot: readout refit with today's labels vs GRU backbone, frozen, per-day z-score | +0.210 | 15/15 | 3/3 |
| NoMAD-style alignment (scaled down) vs GRU backbone, frozen, per-day z-score | +0.040 | 11/15 | 2/3 |
| GRU + TLMA vs GRU backbone, frozen, per-day z-score | -0.154 | 5/15 | 1/3 |
| GRU + BR-TLMA vs GRU + TLMA | +0.010 | 2/15 | 1/3 |
| GRU backbone, frozen, per-day z-score vs Frozen WF, per-day z-score (FALCON-style zero-shot) | +0.055 | 2/3 | 2/3 |

_rows from git 1cb3c13; uncommitted code: False_

### H1 · minival

| Method | Uses today's | R² mean [95% CI over 5 days] | Δ vs FALCON-style [95% CI] | days > ref | seed SD |
|---|---|---|---|---|---|
| Frozen WF, held-in normalisation | nothing | -0.071 [-0.160, +0.006] | -0.137 [-0.216, -0.077] | 0/5 | – |
| Frozen WF, held-in normalisation, z clipped to ±5 | nothing | -0.040 [-0.119, +0.028] | -0.106 [-0.163, -0.064] | 0/5 | – |
| Frozen WF, per-day z-score (FALCON-style zero-shot) | unlabelled (norm. stats) | +0.065 [+0.023, +0.108] | – | – | – |
| WF few-shot: refit on held-in + today's labels | labels | +0.159 [+0.099, +0.226] | +0.093 [+0.054, +0.134] | 5/5 | – |
| WF few-shot: today's labels only | labels | +0.142 [+0.050, +0.263] | +0.076 [-0.014, +0.174] | 4/5 | – |
| PCA latents, frozen, per-day z-score | unlabelled (norm. stats) | +0.030 [-0.004, +0.057] | -0.036 [-0.073, -0.005] | 1/5 | – |
| FA + Procrustes (Degenhart 2020 style) | unlabelled | -0.055 [-0.090, -0.019] | -0.121 [-0.181, -0.068] | 0/5 | +0.018 |
| Covariance-only alignment (lag 0) | unlabelled | +0.032 [-0.002, +0.058] | -0.033 [-0.072, -0.003] | 1/5 | – |
| TLMA: time-lagged moment alignment | unlabelled | +0.029 [-0.005, +0.056] | -0.036 [-0.076, -0.003] | 1/5 | – |
| BR-TLMA: behaviour-reweighted TLMA | unlabelled | +0.034 [-0.000, +0.064] | -0.031 [-0.068, +0.000] | 1/5 | – |
| GRU backbone, frozen, per-day z-score | unlabelled (norm. stats) | +0.006 [-0.046, +0.049] | -0.059 [-0.098, -0.023] | 0/5 | +0.010 |
| GRU few-shot: readout refit with today's labels | labels | +0.158 [+0.120, +0.197] | +0.093 [+0.044, +0.139] | 5/5 | +0.015 |
| NoMAD-style alignment (scaled down) | unlabelled | +0.011 [-0.040, +0.051] | -0.054 [-0.088, -0.020] | 1/5 | +0.007 |
| GRU trained with drift augmentation (after Sussillo 2016) | unlabelled (norm. stats) | +0.030 [-0.022, +0.084] | -0.036 [-0.066, -0.006] | 1/5 | +0.004 |
| GRU + TLMA | unlabelled | +0.011 [-0.036, +0.058] | -0.054 [-0.112, -0.011] | 1/5 | +0.012 |
| GRU + BR-TLMA | unlabelled | +0.019 [-0.030, +0.060] | -0.046 [-0.090, -0.008] | 1/5 | +0.015 |

Paired against the direct parent:

| Comparison | mean Δ R² | pairs better (seed×day) | days better (seed-avg) | 95% CI over days |
|---|---|---|---|---|
| Frozen WF, per-day z-score (FALCON-style zero-shot) vs Frozen WF, held-in normalisation | +0.137 | 5/5 | 5/5 | [+0.077, +0.216] |
| Frozen WF, held-in normalisation, z clipped to ±5 vs Frozen WF, held-in normalisation | +0.031 | 5/5 | 5/5 | [+0.012, +0.053] |
| WF few-shot: refit on held-in + today's labels vs Frozen WF, per-day z-score (FALCON-style zero-shot) | +0.093 | 5/5 | 5/5 | [+0.054, +0.134] |
| Covariance-only alignment (lag 0) vs PCA latents, frozen, per-day z-score | +0.002 | 4/5 | 4/5 | [-0.000, +0.005] |
| TLMA: time-lagged moment alignment vs PCA latents, frozen, per-day z-score | -0.001 | 3/5 | 3/5 | [-0.006, +0.004] |
| TLMA: time-lagged moment alignment vs Covariance-only alignment (lag 0) | -0.003 | 1/5 | 1/5 | [-0.006, -0.000] |
| BR-TLMA: behaviour-reweighted TLMA vs TLMA: time-lagged moment alignment | +0.005 | 5/5 | 5/5 | [+0.001, +0.011] |
| GRU few-shot: readout refit with today's labels vs GRU backbone, frozen, per-day z-score | +0.152 | 25/25 | 5/5 | [+0.121, +0.184] |
| NoMAD-style alignment (scaled down) vs GRU backbone, frozen, per-day z-score | +0.005 | 17/25 | 5/5 | [+0.002, +0.009] |
| GRU + TLMA vs GRU backbone, frozen, per-day z-score | +0.005 | 17/25 | 4/5 | [-0.015, +0.021] |
| GRU + BR-TLMA vs GRU + TLMA | +0.008 | 19/25 | 3/5 | [-0.002, +0.022] |
| GRU backbone, frozen, per-day z-score vs Frozen WF, per-day z-score (FALCON-style zero-shot) | -0.059 | 0/5 | 0/5 | [-0.098, -0.023] |

_rows from git 1cb3c13; uncommitted code: False_
