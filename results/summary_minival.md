### M1-A + M1-B pooled · minival

| Method | Uses today's | R² mean [95% CI over 6 days] | Δ vs FALCON-style [95% CI] | days > ref | seed SD |
|---|---|---|---|---|---|
| Frozen WF, held-in normalisation | nothing | -0.231 [-0.684, +0.211] | -0.578 [-1.027, -0.181] | 0/6 | – |
| Frozen WF, held-in normalisation, z clipped to ±5 | nothing | +0.158 [-0.090, +0.355] | -0.189 [-0.327, -0.062] | 1/6 | – |
| Frozen WF, per-day z-score (FALCON-style zero-shot) | unlabelled (norm. stats) | +0.346 [+0.217, +0.448] | – | – | – |
| WF few-shot: refit on held-in + today's labels | labels | +0.551 [+0.487, +0.619] | +0.204 [+0.142, +0.281] | 6/6 | – |
| WF few-shot: today's labels only | labels | +0.458 [+0.325, +0.581] | +0.112 [-0.050, +0.272] | 4/6 | – |
| PCA latents, frozen, per-day z-score | unlabelled (norm. stats) | +0.361 [+0.237, +0.459] | +0.015 [-0.010, +0.048] | 2/6 | – |
| FA + Procrustes (Degenhart 2020 style) | unlabelled | +0.357 [+0.248, +0.461] | +0.011 [-0.062, +0.083] | 4/6 | +0.015 |
| Covariance-only alignment (lag 0) | unlabelled | +0.371 [+0.259, +0.463] | +0.025 [-0.007, +0.059] | 3/6 | – |
| TLMA: time-lagged moment alignment | unlabelled | +0.350 [+0.238, +0.448] | +0.004 [-0.035, +0.046] | 3/6 | – |
| BR-TLMA: behaviour-reweighted TLMA | unlabelled | +0.205 [+0.037, +0.364] | -0.141 [-0.345, +0.015] | 2/6 | – |
| GRU backbone, frozen, per-day z-score | unlabelled (norm. stats) | +0.443 [+0.240, +0.586] | +0.096 [+0.020, +0.148] | 5/6 | +0.024 |
| GRU few-shot: readout refit with today's labels | labels | +0.602 [+0.529, +0.673] | +0.255 [+0.201, +0.321] | 6/6 | +0.007 |
| NoMAD-style alignment (scaled down) | unlabelled | +0.484 [+0.304, +0.607] | +0.137 [+0.080, +0.192] | 6/6 | +0.014 |
| GRU trained with drift augmentation (after Sussillo 2016) | unlabelled (norm. stats) | +0.466 [+0.278, +0.590] | +0.120 [+0.055, +0.169] | 5/6 | +0.032 |
| GRU + TLMA | unlabelled | +0.361 [+0.195, +0.513] | +0.015 [-0.082, +0.110] | 3/6 | +0.041 |
| GRU + BR-TLMA | unlabelled | +0.366 [+0.165, +0.530] | +0.020 [-0.073, +0.110] | 3/6 | +0.050 |

Paired against the direct parent:

| Comparison | mean Δ R² | pairs better (seed×day) | days better (seed-avg) | 95% CI over days |
|---|---|---|---|---|
| Frozen WF, per-day z-score (FALCON-style zero-shot) vs Frozen WF, held-in normalisation | +0.578 | 6/6 | 6/6 | [+0.181, +1.027] |
| Frozen WF, held-in normalisation, z clipped to ±5 vs Frozen WF, held-in normalisation | +0.389 | 4/6 | 4/6 | [+0.026, +0.882] |
| WF few-shot: refit on held-in + today's labels vs Frozen WF, per-day z-score (FALCON-style zero-shot) | +0.204 | 6/6 | 6/6 | [+0.142, +0.281] |
| Covariance-only alignment (lag 0) vs PCA latents, frozen, per-day z-score | +0.010 | 5/6 | 5/6 | [-0.002, +0.023] |
| TLMA: time-lagged moment alignment vs PCA latents, frozen, per-day z-score | -0.011 | 2/6 | 2/6 | [-0.030, +0.009] |
| TLMA: time-lagged moment alignment vs Covariance-only alignment (lag 0) | -0.021 | 1/6 | 1/6 | [-0.032, -0.009] |
| BR-TLMA: behaviour-reweighted TLMA vs TLMA: time-lagged moment alignment | -0.145 | 1/6 | 1/6 | [-0.324, -0.020] |
| GRU few-shot: readout refit with today's labels vs GRU backbone, frozen, per-day z-score | +0.159 | 30/30 | 6/6 | [+0.079, +0.291] |
| NoMAD-style alignment (scaled down) vs GRU backbone, frozen, per-day z-score | +0.041 | 24/30 | 5/6 | [+0.009, +0.073] |
| GRU + TLMA vs GRU backbone, frozen, per-day z-score | -0.082 | 12/30 | 2/6 | [-0.178, +0.010] |
| GRU + BR-TLMA vs GRU + TLMA | +0.005 | 3/30 | 2/6 | [-0.052, +0.067] |
| GRU backbone, frozen, per-day z-score vs Frozen WF, per-day z-score (FALCON-style zero-shot) | +0.096 | 5/6 | 5/6 | [+0.020, +0.148] |

_rows from git 1cb3c13,bd86777; uncommitted code: False_

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

### M1-B · minival

| Method | Uses today's | 2012-12-07 (+1 d) | 2012-12-10 (+3 d) | 2012-12-12 (+2 d) | mean | days > ref | seed SD |
|---|---|---|---|---|---|---|---|
| Frozen WF, held-in normalisation | nothing | -1.014 | +0.207 | +0.352 | -0.152 | 0/3 | – |
| Frozen WF, held-in normalisation, z clipped to ±5 | nothing | +0.472 | +0.225 | +0.346 | +0.348 | 1/3 | – |
| Frozen WF, per-day z-score (FALCON-style zero-shot) | unlabelled (norm. stats) | +0.463 | +0.275 | +0.430 | +0.389 | – | – |
| WF few-shot: refit on held-in + today's labels | labels | +0.686 | +0.493 | +0.540 | +0.573 | 3/3 | – |
| WF few-shot: today's labels only | labels | +0.295 | +0.199 | +0.522 | +0.339 | 1/3 | – |
| PCA latents, frozen, per-day z-score | unlabelled (norm. stats) | +0.444 | +0.274 | +0.421 | +0.380 | 0/3 | – |
| FA + Procrustes (Degenhart 2020 style) | unlabelled | +0.475 | +0.159 | +0.347 | +0.327 | 1/3 | +0.027 |
| Covariance-only alignment (lag 0) | unlabelled | +0.456 | +0.286 | +0.409 | +0.383 | 1/3 | – |
| TLMA: time-lagged moment alignment | unlabelled | +0.427 | +0.251 | +0.370 | +0.349 | 0/3 | – |
| BR-TLMA: behaviour-reweighted TLMA | unlabelled | -0.136 | +0.075 | +0.265 | +0.068 | 0/3 | – |
| GRU backbone, frozen, per-day z-score | unlabelled (norm. stats) | +0.636 | +0.418 | +0.526 | +0.527 | 3/3 | +0.018 |
| GRU few-shot: readout refit with today's labels | labels | +0.730 | +0.569 | +0.607 | +0.635 | 3/3 | +0.008 |
| NoMAD-style alignment (scaled down) | unlabelled | +0.667 | +0.509 | +0.531 | +0.569 | 3/3 | +0.031 |
| GRU trained with drift augmentation (after Sussillo 2016) | unlabelled (norm. stats) | +0.610 | +0.476 | +0.535 | +0.541 | 3/3 | +0.029 |
| GRU + TLMA | unlabelled | +0.641 | +0.392 | +0.519 | +0.517 | 3/3 | +0.027 |
| GRU + BR-TLMA | unlabelled | +0.641 | +0.392 | +0.520 | +0.517 | 3/3 | +0.028 |

Paired against the direct parent:

| Comparison | mean Δ R² | pairs better (seed×day) | days better (seed-avg) |
|---|---|---|---|
| Frozen WF, per-day z-score (FALCON-style zero-shot) vs Frozen WF, held-in normalisation | +0.541 | 3/3 | 3/3 |
| Frozen WF, held-in normalisation, z clipped to ±5 vs Frozen WF, held-in normalisation | +0.499 | 2/3 | 2/3 |
| WF few-shot: refit on held-in + today's labels vs Frozen WF, per-day z-score (FALCON-style zero-shot) | +0.184 | 3/3 | 3/3 |
| Covariance-only alignment (lag 0) vs PCA latents, frozen, per-day z-score | +0.004 | 2/3 | 2/3 |
| TLMA: time-lagged moment alignment vs PCA latents, frozen, per-day z-score | -0.030 | 0/3 | 0/3 |
| TLMA: time-lagged moment alignment vs Covariance-only alignment (lag 0) | -0.034 | 0/3 | 0/3 |
| BR-TLMA: behaviour-reweighted TLMA vs TLMA: time-lagged moment alignment | -0.281 | 0/3 | 0/3 |
| GRU few-shot: readout refit with today's labels vs GRU backbone, frozen, per-day z-score | +0.109 | 15/15 | 3/3 |
| NoMAD-style alignment (scaled down) vs GRU backbone, frozen, per-day z-score | +0.042 | 13/15 | 3/3 |
| GRU + TLMA vs GRU backbone, frozen, per-day z-score | -0.010 | 7/15 | 1/3 |
| GRU + BR-TLMA vs GRU + TLMA | +0.000 | 1/15 | 1/3 |
| GRU backbone, frozen, per-day z-score vs Frozen WF, per-day z-score (FALCON-style zero-shot) | +0.137 | 3/3 | 3/3 |

_rows from git bd86777; uncommitted code: False_

### M2 · minival

| Method | Uses today's | 2020-10-20 (+1 d) | 2020-10-27 (+7 d) | 2020-10-28 (+1 d) | mean | days > ref | seed SD |
|---|---|---|---|---|---|---|---|
| Frozen WF, held-in normalisation | nothing | -3.213 | -0.149 | -0.013 | -1.125 | 0/3 | – |
| Frozen WF, held-in normalisation, z clipped to ±5 | nothing | -0.748 | +0.096 | +0.168 | -0.161 | 1/3 | – |
| Frozen WF, per-day z-score (FALCON-style zero-shot) | unlabelled (norm. stats) | -0.297 | +0.117 | +0.110 | -0.023 | – | – |
| WF few-shot: refit on held-in + today's labels | labels | +0.101 | +0.303 | +0.307 | +0.237 | 3/3 | – |
| WF few-shot: today's labels only | labels | +0.282 | +0.396 | +0.490 | +0.389 | 3/3 | – |
| PCA latents, frozen, per-day z-score | unlabelled (norm. stats) | -0.248 | +0.184 | +0.044 | -0.007 | 2/3 | – |
| FA + Procrustes (Degenhart 2020 style) | unlabelled | -0.464 | +0.106 | +0.275 | -0.028 | 1/3 | +0.057 |
| Covariance-only alignment (lag 0) | unlabelled | -0.251 | +0.163 | +0.094 | +0.002 | 2/3 | – |
| TLMA: time-lagged moment alignment | unlabelled | -0.273 | +0.144 | +0.194 | +0.021 | 3/3 | – |
| BR-TLMA: behaviour-reweighted TLMA | unlabelled | -0.126 | +0.189 | +0.158 | +0.074 | 3/3 | – |
| GRU backbone, frozen, per-day z-score | unlabelled (norm. stats) | -0.248 | -0.011 | +0.102 | -0.052 | 1/3 | +0.092 |
| GRU few-shot: readout refit with today's labels | labels | +0.202 | +0.202 | +0.278 | +0.227 | 3/3 | +0.032 |
| NoMAD-style alignment (scaled down) | unlabelled | -0.201 | -0.028 | +0.099 | -0.043 | 1/3 | +0.084 |
| GRU trained with drift augmentation (after Sussillo 2016) | unlabelled (norm. stats) | -0.656 | -0.188 | -0.038 | -0.294 | 0/3 | +0.281 |
| GRU + TLMA | unlabelled | -0.259 | -0.028 | +0.123 | -0.055 | 2/3 | +0.082 |
| GRU + BR-TLMA | unlabelled | -0.211 | -0.019 | +0.099 | -0.044 | 1/3 | +0.089 |

Paired against the direct parent:

| Comparison | mean Δ R² | pairs better (seed×day) | days better (seed-avg) |
|---|---|---|---|
| Frozen WF, per-day z-score (FALCON-style zero-shot) vs Frozen WF, held-in normalisation | +1.102 | 3/3 | 3/3 |
| Frozen WF, held-in normalisation, z clipped to ±5 vs Frozen WF, held-in normalisation | +0.964 | 3/3 | 3/3 |
| WF few-shot: refit on held-in + today's labels vs Frozen WF, per-day z-score (FALCON-style zero-shot) | +0.260 | 3/3 | 3/3 |
| Covariance-only alignment (lag 0) vs PCA latents, frozen, per-day z-score | +0.008 | 1/3 | 1/3 |
| TLMA: time-lagged moment alignment vs PCA latents, frozen, per-day z-score | +0.028 | 1/3 | 1/3 |
| TLMA: time-lagged moment alignment vs Covariance-only alignment (lag 0) | +0.020 | 1/3 | 1/3 |
| BR-TLMA: behaviour-reweighted TLMA vs TLMA: time-lagged moment alignment | +0.053 | 2/3 | 2/3 |
| GRU few-shot: readout refit with today's labels vs GRU backbone, frozen, per-day z-score | +0.279 | 15/15 | 3/3 |
| NoMAD-style alignment (scaled down) vs GRU backbone, frozen, per-day z-score | +0.009 | 8/15 | 1/3 |
| GRU + TLMA vs GRU backbone, frozen, per-day z-score | -0.003 | 5/15 | 1/3 |
| GRU + BR-TLMA vs GRU + TLMA | +0.011 | 9/15 | 2/3 |
| GRU backbone, frozen, per-day z-score vs Frozen WF, per-day z-score (FALCON-style zero-shot) | -0.029 | 1/3 | 1/3 |

_rows from git 1c73711; uncommitted code: False_

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
