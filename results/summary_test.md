### M1-A · test

| Method | Uses today's | 2012-10-04 (+6 d) | 2012-10-17 (+19 d) | 2012-10-24 (+26 d) | mean | days > ref | seed SD |
|---|---|---|---|---|---|---|---|
| Frozen WF, held-in normalisation | nothing | -5.220 | -4.479 | -3.619 | -4.440 | 0/3 | – |
| Frozen WF, held-in normalisation, z clipped to ±5 | nothing | -0.277 | -0.319 | -0.307 | -0.301 | 0/3 | – |
| Frozen WF, per-day z-score (FALCON-style zero-shot) | unlabelled (norm. stats) | +0.466 | +0.326 | +0.303 | +0.365 | – | – |
| WF few-shot: refit on held-in + today's labels | labels | +0.492 | +0.347 | +0.356 | +0.398 | 3/3 | – |
| WF few-shot: today's labels only | labels | +0.423 | +0.255 | +0.355 | +0.344 | 1/3 | – |
| PCA latents, frozen, per-day z-score | unlabelled (norm. stats) | +0.455 | +0.327 | +0.289 | +0.357 | 1/3 | – |
| FA + Procrustes (Degenhart 2020 style) | unlabelled | +0.400 | +0.264 | +0.287 | +0.317 | 0/3 | +0.019 |
| Covariance-only alignment (lag 0) | unlabelled | +0.441 | +0.319 | +0.301 | +0.354 | 0/3 | – |
| TLMA: time-lagged moment alignment | unlabelled | +0.441 | +0.316 | +0.300 | +0.352 | 0/3 | – |
| BR-TLMA: behaviour-reweighted TLMA | unlabelled | +0.247 | +0.295 | +0.163 | +0.235 | 0/3 | – |
| GRU backbone, frozen, per-day z-score | unlabelled (norm. stats) | +0.479 | +0.306 | +0.377 | +0.388 | 2/3 | +0.023 |
| GRU few-shot: readout refit with today's labels | labels | +0.517 | +0.370 | +0.426 | +0.438 | 3/3 | +0.014 |
| NoMAD-style alignment (scaled down) | unlabelled | -0.292 | -0.010 | +0.183 | -0.040 | 0/3 | +0.444 |
| GRU trained with drift augmentation (after Sussillo 2016) | unlabelled (norm. stats) | +0.466 | +0.312 | +0.367 | +0.381 | 1/3 | +0.022 |
| GRU + TLMA | unlabelled | +0.435 | +0.332 | +0.358 | +0.375 | 2/3 | +0.045 |
| GRU + BR-TLMA | unlabelled | +0.443 | +0.332 | +0.366 | +0.380 | 2/3 | +0.046 |

Paired against the direct parent:

| Comparison | mean Δ R² | pairs better (seed×day) | days better (seed-avg) |
|---|---|---|---|
| Frozen WF, per-day z-score (FALCON-style zero-shot) vs Frozen WF, held-in normalisation | +4.804 | 3/3 | 3/3 |
| Frozen WF, held-in normalisation, z clipped to ±5 vs Frozen WF, held-in normalisation | +4.139 | 3/3 | 3/3 |
| WF few-shot: refit on held-in + today's labels vs Frozen WF, per-day z-score (FALCON-style zero-shot) | +0.033 | 3/3 | 3/3 |
| Covariance-only alignment (lag 0) vs PCA latents, frozen, per-day z-score | -0.003 | 1/3 | 1/3 |
| TLMA: time-lagged moment alignment vs PCA latents, frozen, per-day z-score | -0.005 | 1/3 | 1/3 |
| TLMA: time-lagged moment alignment vs Covariance-only alignment (lag 0) | -0.001 | 1/3 | 1/3 |
| BR-TLMA: behaviour-reweighted TLMA vs TLMA: time-lagged moment alignment | -0.118 | 0/3 | 0/3 |
| GRU few-shot: readout refit with today's labels vs GRU backbone, frozen, per-day z-score | +0.050 | 15/15 | 3/3 |
| NoMAD-style alignment (scaled down) vs GRU backbone, frozen, per-day z-score | -0.428 | 0/15 | 0/3 |
| GRU + TLMA vs GRU backbone, frozen, per-day z-score | -0.013 | 5/15 | 1/3 |
| GRU + BR-TLMA vs GRU + TLMA | +0.005 | 6/15 | 2/3 |
| GRU backbone, frozen, per-day z-score vs Frozen WF, per-day z-score (FALCON-style zero-shot) | +0.023 | 2/3 | 2/3 |

_rows from git 1cb3c13; uncommitted code: False_

### H1 · test

| Method | Uses today's | R² mean [95% CI over 7 days] | Δ vs FALCON-style [95% CI] | days > ref | seed SD |
|---|---|---|---|---|---|
| Frozen WF, held-in normalisation | nothing | -0.012 [-0.071, +0.051] | +0.015 [-0.049, +0.092] | 3/7 | – |
| Frozen WF, held-in normalisation, z clipped to ±5 | nothing | +0.010 [-0.034, +0.061] | +0.037 [-0.024, +0.116] | 4/7 | – |
| Frozen WF, per-day z-score (FALCON-style zero-shot) | unlabelled (norm. stats) | -0.027 [-0.120, +0.046] | – | – | – |
| WF few-shot: refit on held-in + today's labels | labels | -0.024 [-0.121, +0.051] | +0.003 [-0.002, +0.008] | 6/7 | – |
| WF few-shot: today's labels only | labels | -0.002 [-0.015, +0.007] | +0.025 [-0.047, +0.123] | 2/7 | – |
| PCA latents, frozen, per-day z-score | unlabelled (norm. stats) | -0.009 [-0.052, +0.019] | +0.018 [-0.030, +0.070] | 4/7 | – |
| FA + Procrustes (Degenhart 2020 style) | unlabelled | -0.049 [-0.093, -0.011] | -0.022 [-0.061, +0.030] | 1/7 | +0.015 |
| Covariance-only alignment (lag 0) | unlabelled | -0.013 [-0.061, +0.018] | +0.015 [-0.030, +0.063] | 3/7 | – |
| TLMA: time-lagged moment alignment | unlabelled | -0.024 [-0.083, +0.014] | +0.003 [-0.035, +0.042] | 3/7 | – |
| BR-TLMA: behaviour-reweighted TLMA | unlabelled | -0.011 [-0.057, +0.017] | +0.016 [-0.032, +0.066] | 4/7 | – |
| GRU backbone, frozen, per-day z-score | unlabelled (norm. stats) | -0.004 [-0.053, +0.032] | +0.023 [-0.020, +0.070] | 4/7 | +0.018 |
| GRU few-shot: readout refit with today's labels | labels | +0.017 [-0.028, +0.052] | +0.044 [-0.003, +0.096] | 5/7 | +0.013 |
| NoMAD-style alignment (scaled down) | unlabelled | -0.011 [-0.061, +0.025] | +0.016 [-0.024, +0.061] | 4/7 | +0.018 |
| GRU trained with drift augmentation (after Sussillo 2016) | unlabelled (norm. stats) | -0.002 [-0.066, +0.043] | +0.025 [-0.006, +0.057] | 6/7 | +0.014 |
| GRU + TLMA | unlabelled | -0.017 [-0.080, +0.023] | +0.010 [-0.027, +0.047] | 4/7 | +0.016 |
| GRU + BR-TLMA | unlabelled | +0.000 [-0.048, +0.034] | +0.028 [-0.016, +0.075] | 5/7 | +0.017 |

Paired against the direct parent:

| Comparison | mean Δ R² | pairs better (seed×day) | days better (seed-avg) | 95% CI over days |
|---|---|---|---|---|
| Frozen WF, per-day z-score (FALCON-style zero-shot) vs Frozen WF, held-in normalisation | -0.015 | 4/7 | 4/7 | [-0.092, +0.049] |
| Frozen WF, held-in normalisation, z clipped to ±5 vs Frozen WF, held-in normalisation | +0.022 | 6/7 | 6/7 | [+0.006, +0.041] |
| WF few-shot: refit on held-in + today's labels vs Frozen WF, per-day z-score (FALCON-style zero-shot) | +0.003 | 6/7 | 6/7 | [-0.002, +0.008] |
| Covariance-only alignment (lag 0) vs PCA latents, frozen, per-day z-score | -0.004 | 1/7 | 1/7 | [-0.009, -0.000] |
| TLMA: time-lagged moment alignment vs PCA latents, frozen, per-day z-score | -0.015 | 1/7 | 1/7 | [-0.031, -0.004] |
| TLMA: time-lagged moment alignment vs Covariance-only alignment (lag 0) | -0.011 | 0/7 | 0/7 | [-0.022, -0.004] |
| BR-TLMA: behaviour-reweighted TLMA vs TLMA: time-lagged moment alignment | +0.012 | 6/7 | 6/7 | [+0.002, +0.026] |
| GRU few-shot: readout refit with today's labels vs GRU backbone, frozen, per-day z-score | +0.021 | 29/35 | 7/7 | [+0.015, +0.028] |
| NoMAD-style alignment (scaled down) vs GRU backbone, frozen, per-day z-score | -0.006 | 10/35 | 1/7 | [-0.010, -0.003] |
| GRU + TLMA vs GRU backbone, frozen, per-day z-score | -0.013 | 9/35 | 1/7 | [-0.027, -0.003] |
| GRU + BR-TLMA vs GRU + TLMA | +0.018 | 32/35 | 7/7 | [+0.009, +0.030] |
| GRU backbone, frozen, per-day z-score vs Frozen WF, per-day z-score (FALCON-style zero-shot) | +0.023 | 4/7 | 4/7 | [-0.020, +0.070] |

_rows from git 1cb3c13; uncommitted code: False_
