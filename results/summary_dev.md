### M1-A · dev

| Method | Uses today's | 2012-09-27 (+1 d) | 2012-09-28 (+2 d) | mean | days > ref | seed SD |
|---|---|---|---|---|---|---|
| Frozen WF, held-in normalisation | nothing | +0.076 | -0.006 | +0.035 | 0/2 | – |
| Frozen WF, held-in normalisation, z clipped to ±5 | nothing | +0.091 | +0.355 | +0.223 | 0/2 | – |
| Frozen WF, per-day z-score (FALCON-style zero-shot) | unlabelled (norm. stats) | +0.414 | +0.428 | +0.421 | – | – |
| WF few-shot: refit on held-in + today's labels | labels | +0.478 | +0.526 | +0.502 | 2/2 | – |
| WF few-shot: today's labels only | labels | +0.340 | +0.475 | +0.408 | 1/2 | – |
| PCA latents, frozen, per-day z-score | unlabelled (norm. stats) | +0.462 | +0.498 | +0.480 | 2/2 | – |
| FA + Procrustes (Degenhart 2020 style) | unlabelled | +0.420 | +0.482 | +0.451 | 2/2 | +0.007 |
| Covariance-only alignment (lag 0) | unlabelled | +0.457 | +0.481 | +0.469 | 2/2 | – |
| TLMA: time-lagged moment alignment | unlabelled | +0.455 | +0.475 | +0.465 | 2/2 | – |
| BR-TLMA: behaviour-reweighted TLMA | unlabelled | +0.465 | +0.498 | +0.482 | 2/2 | – |
| GRU backbone, frozen, per-day z-score | unlabelled (norm. stats) | +0.540 | +0.593 | +0.567 | 2/2 | +0.014 |
| GRU few-shot: readout refit with today's labels | labels | +0.546 | +0.615 | +0.580 | 2/2 | +0.010 |
| NoMAD-style alignment (scaled down) | unlabelled | +0.558 | +0.587 | +0.572 | 2/2 | +0.009 |
| GRU trained with drift augmentation (after Sussillo 2016) | unlabelled (norm. stats) | +0.589 | +0.582 | +0.586 | 2/2 | +0.010 |
| GRU + TLMA | unlabelled | +0.422 | +0.400 | +0.411 | 1/2 | +0.086 |
| GRU + BR-TLMA | unlabelled | +0.469 | +0.459 | +0.464 | 2/2 | +0.060 |

Paired against the direct parent:

| Comparison | mean Δ R² | pairs better (seed×day) | days better (seed-avg) |
|---|---|---|---|
| Frozen WF, per-day z-score (FALCON-style zero-shot) vs Frozen WF, held-in normalisation | +0.387 | 2/2 | 2/2 |
| Frozen WF, held-in normalisation, z clipped to ±5 vs Frozen WF, held-in normalisation | +0.188 | 2/2 | 2/2 |
| WF few-shot: refit on held-in + today's labels vs Frozen WF, per-day z-score (FALCON-style zero-shot) | +0.081 | 2/2 | 2/2 |
| Covariance-only alignment (lag 0) vs PCA latents, frozen, per-day z-score | -0.011 | 0/2 | 0/2 |
| TLMA: time-lagged moment alignment vs PCA latents, frozen, per-day z-score | -0.015 | 0/2 | 0/2 |
| TLMA: time-lagged moment alignment vs Covariance-only alignment (lag 0) | -0.003 | 0/2 | 0/2 |
| BR-TLMA: behaviour-reweighted TLMA vs TLMA: time-lagged moment alignment | +0.016 | 2/2 | 2/2 |
| GRU few-shot: readout refit with today's labels vs GRU backbone, frozen, per-day z-score | +0.014 | 8/10 | 2/2 |
| NoMAD-style alignment (scaled down) vs GRU backbone, frozen, per-day z-score | +0.006 | 6/10 | 1/2 |
| GRU + TLMA vs GRU backbone, frozen, per-day z-score | -0.156 | 0/10 | 0/2 |
| GRU + BR-TLMA vs GRU + TLMA | +0.053 | 2/10 | 2/2 |
| GRU backbone, frozen, per-day z-score vs Frozen WF, per-day z-score (FALCON-style zero-shot) | +0.146 | 2/2 | 2/2 |

_rows from git 1cb3c13; uncommitted code: False_

### H1 · dev

| Method | Uses today's | R² mean [95% CI over 3 days] | Δ vs FALCON-style [95% CI] | days > ref | seed SD |
|---|---|---|---|---|---|
| Frozen WF, held-in normalisation | nothing | -0.049 [-0.165, +0.060] | -0.072 [-0.167, -0.018] | 0/3 | – |
| Frozen WF, held-in normalisation, z clipped to ±5 | nothing | -0.034 [-0.149, +0.069] | -0.058 [-0.151, -0.009] | 0/3 | – |
| Frozen WF, per-day z-score (FALCON-style zero-shot) | unlabelled (norm. stats) | +0.024 [-0.010, +0.078] | – | – | – |
| WF few-shot: refit on held-in + today's labels | labels | +0.030 [-0.002, +0.087] | +0.007 [+0.003, +0.009] | 3/3 | – |
| WF few-shot: today's labels only | labels | -0.027 [-0.056, -0.003] | -0.050 [-0.099, +0.006] | 1/3 | – |
| PCA latents, frozen, per-day z-score | unlabelled (norm. stats) | -0.022 [-0.039, +0.005] | -0.046 [-0.112, +0.003] | 1/3 | – |
| FA + Procrustes (Degenhart 2020 style) | unlabelled | -0.059 [-0.105, +0.000] | -0.083 [-0.183, -0.002] | 0/3 | +0.008 |
| Covariance-only alignment (lag 0) | unlabelled | -0.025 [-0.040, +0.003] | -0.048 [-0.114, -0.000] | 0/3 | – |
| TLMA: time-lagged moment alignment | unlabelled | -0.035 [-0.047, -0.013] | -0.058 [-0.123, -0.015] | 0/3 | – |
| BR-TLMA: behaviour-reweighted TLMA | unlabelled | -0.017 [-0.042, +0.001] | -0.041 [-0.089, -0.002] | 0/3 | – |
| GRU backbone, frozen, per-day z-score | unlabelled (norm. stats) | -0.048 [-0.073, -0.034] | -0.072 [-0.113, -0.028] | 0/3 | +0.014 |
| GRU few-shot: readout refit with today's labels | labels | -0.008 [-0.046, +0.018] | -0.032 [-0.060, +0.013] | 1/3 | +0.009 |
| NoMAD-style alignment (scaled down) | unlabelled | -0.035 [-0.061, -0.015] | -0.059 [-0.093, -0.020] | 0/3 | +0.013 |
| GRU trained with drift augmentation (after Sussillo 2016) | unlabelled (norm. stats) | -0.018 [-0.029, -0.011] | -0.042 [-0.094, -0.002] | 0/3 | +0.020 |
| GRU + TLMA | unlabelled | -0.058 [-0.106, -0.029] | -0.082 [-0.109, -0.031] | 0/3 | +0.019 |
| GRU + BR-TLMA | unlabelled | -0.058 [-0.107, -0.027] | -0.082 [-0.109, -0.031] | 0/3 | +0.021 |

Paired against the direct parent:

| Comparison | mean Δ R² | pairs better (seed×day) | days better (seed-avg) | 95% CI over days |
|---|---|---|---|---|
| Frozen WF, per-day z-score (FALCON-style zero-shot) vs Frozen WF, held-in normalisation | +0.072 | 3/3 | 3/3 | [+0.018, +0.167] |
| Frozen WF, held-in normalisation, z clipped to ±5 vs Frozen WF, held-in normalisation | +0.015 | 3/3 | 3/3 | [+0.009, +0.019] |
| WF few-shot: refit on held-in + today's labels vs Frozen WF, per-day z-score (FALCON-style zero-shot) | +0.007 | 3/3 | 3/3 | [+0.003, +0.009] |
| Covariance-only alignment (lag 0) vs PCA latents, frozen, per-day z-score | -0.002 | 0/3 | 0/3 | [-0.003, -0.001] |
| TLMA: time-lagged moment alignment vs PCA latents, frozen, per-day z-score | -0.012 | 0/3 | 0/3 | [-0.018, -0.008] |
| TLMA: time-lagged moment alignment vs Covariance-only alignment (lag 0) | -0.010 | 0/3 | 0/3 | [-0.015, -0.007] |
| BR-TLMA: behaviour-reweighted TLMA vs TLMA: time-lagged moment alignment | +0.018 | 3/3 | 3/3 | [+0.006, +0.033] |
| GRU few-shot: readout refit with today's labels vs GRU backbone, frozen, per-day z-score | +0.040 | 14/15 | 3/3 | [+0.026, +0.052] |
| NoMAD-style alignment (scaled down) vs GRU backbone, frozen, per-day z-score | +0.013 | 12/15 | 3/3 | [+0.008, +0.019] |
| GRU + TLMA vs GRU backbone, frozen, per-day z-score | -0.010 | 6/15 | 1/3 | [-0.033, +0.005] |
| GRU + BR-TLMA vs GRU + TLMA | +0.001 | 8/15 | 1/3 | [-0.001, +0.003] |
| GRU backbone, frozen, per-day z-score vs Frozen WF, per-day z-score (FALCON-style zero-shot) | -0.072 | 0/3 | 0/3 | [-0.113, -0.028] |

_rows from git 1cb3c13; uncommitted code: False_
