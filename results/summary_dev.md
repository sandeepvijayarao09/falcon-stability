### M1-A + M1-B pooled · dev

| Method | Uses today's | R² mean [95% CI over 4 days] | Δ vs FALCON-style [95% CI] | days > ref | seed SD |
|---|---|---|---|---|---|
| Frozen WF, held-in normalisation | nothing | +0.160 [+0.028, +0.348] | -0.246 [-0.387, -0.085] | 0/4 | – |
| Frozen WF, held-in normalisation, z clipped to ±5 | nothing | +0.265 [+0.152, +0.378] | -0.141 [-0.261, -0.056] | 0/4 | – |
| Frozen WF, per-day z-score (FALCON-style zero-shot) | unlabelled (norm. stats) | +0.406 [+0.364, +0.434] | – | – | – |
| WF few-shot: refit on held-in + today's labels | labels | +0.472 [+0.423, +0.514] | +0.066 [+0.045, +0.089] | 4/4 | – |
| WF few-shot: today's labels only | labels | +0.319 [+0.219, +0.426] | -0.087 [-0.211, +0.017] | 1/4 | – |
| PCA latents, frozen, per-day z-score | unlabelled (norm. stats) | +0.421 [+0.353, +0.480] | +0.015 [-0.029, +0.059] | 2/4 | – |
| FA + Procrustes (Degenhart 2020 style) | unlabelled | +0.210 [-0.030, +0.451] | -0.196 [-0.421, +0.030] | 2/4 | +0.095 |
| Covariance-only alignment (lag 0) | unlabelled | +0.414 [+0.348, +0.469] | +0.008 [-0.032, +0.048] | 2/4 | – |
| TLMA: time-lagged moment alignment | unlabelled | +0.384 [+0.302, +0.465] | -0.023 [-0.089, +0.044] | 2/4 | – |
| BR-TLMA: behaviour-reweighted TLMA | unlabelled | +0.374 [+0.267, +0.482] | -0.032 [-0.124, +0.060] | 2/4 | – |
| GRU backbone, frozen, per-day z-score | unlabelled (norm. stats) | +0.550 [+0.520, +0.580] | +0.144 [+0.123, +0.165] | 4/4 | +0.009 |
| GRU few-shot: readout refit with today's labels | labels | +0.574 [+0.541, +0.607] | +0.168 [+0.145, +0.191] | 4/4 | +0.010 |
| NoMAD-style alignment (scaled down) | unlabelled | +0.560 [+0.535, +0.580] | +0.154 [+0.138, +0.171] | 4/4 | +0.010 |
| GRU trained with drift augmentation (after Sussillo 2016) | unlabelled (norm. stats) | +0.578 [+0.555, +0.593] | +0.172 [+0.156, +0.190] | 4/4 | +0.021 |
| GRU + TLMA | unlabelled | +0.443 [+0.411, +0.474] | +0.037 [-0.016, +0.112] | 3/4 | +0.047 |
| GRU + BR-TLMA | unlabelled | +0.469 [+0.459, +0.482] | +0.063 [+0.025, +0.118] | 4/4 | +0.047 |

Paired against the direct parent:

| Comparison | mean Δ R² | pairs better (seed×day) | days better (seed-avg) | 95% CI over days |
|---|---|---|---|---|
| Frozen WF, per-day z-score (FALCON-style zero-shot) vs Frozen WF, held-in normalisation | +0.246 | 4/4 | 4/4 | [+0.085, +0.387] |
| Frozen WF, held-in normalisation, z clipped to ±5 vs Frozen WF, held-in normalisation | +0.105 | 3/4 | 3/4 | [-0.012, +0.275] |
| WF few-shot: refit on held-in + today's labels vs Frozen WF, per-day z-score (FALCON-style zero-shot) | +0.066 | 4/4 | 4/4 | [+0.045, +0.089] |
| Covariance-only alignment (lag 0) vs PCA latents, frozen, per-day z-score | -0.007 | 0/4 | 0/4 | [-0.014, -0.003] |
| TLMA: time-lagged moment alignment vs PCA latents, frozen, per-day z-score | -0.038 | 0/4 | 0/4 | [-0.061, -0.015] |
| TLMA: time-lagged moment alignment vs Covariance-only alignment (lag 0) | -0.030 | 0/4 | 0/4 | [-0.057, -0.003] |
| BR-TLMA: behaviour-reweighted TLMA vs TLMA: time-lagged moment alignment | -0.009 | 3/4 | 3/4 | [-0.063, +0.022] |
| GRU few-shot: readout refit with today's labels vs GRU backbone, frozen, per-day z-score | +0.024 | 18/20 | 4/4 | [+0.012, +0.036] |
| NoMAD-style alignment (scaled down) vs GRU backbone, frozen, per-day z-score | +0.010 | 13/20 | 3/4 | [-0.001, +0.016] |
| GRU + TLMA vs GRU backbone, frozen, per-day z-score | -0.107 | 0/20 | 0/4 | [-0.170, -0.043] |
| GRU + BR-TLMA vs GRU + TLMA | +0.026 | 2/20 | 2/4 | [+0.000, +0.053] |
| GRU backbone, frozen, per-day z-score vs Frozen WF, per-day z-score (FALCON-style zero-shot) | +0.144 | 4/4 | 4/4 | [+0.123, +0.165] |

_rows from git 1cb3c13,bd86777; uncommitted code: False_

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

### M1-B · dev

| Method | Uses today's | 2012-12-10 (+3 d) | 2012-12-12 (+5 d) | mean | days > ref | seed SD |
|---|---|---|---|---|---|---|
| Frozen WF, held-in normalisation | nothing | +0.439 | +0.130 | +0.285 | 0/2 | – |
| Frozen WF, held-in normalisation, z clipped to ±5 | nothing | +0.401 | +0.213 | +0.307 | 0/2 | – |
| Frozen WF, per-day z-score (FALCON-style zero-shot) | unlabelled (norm. stats) | +0.439 | +0.342 | +0.391 | – | – |
| WF few-shot: refit on held-in + today's labels | labels | +0.478 | +0.405 | +0.441 | 2/2 | – |
| WF few-shot: today's labels only | labels | +0.179 | +0.281 | +0.230 | 0/2 | – |
| PCA latents, frozen, per-day z-score | unlabelled (norm. stats) | +0.408 | +0.317 | +0.362 | 0/2 | – |
| FA + Procrustes (Degenhart 2020 style) | unlabelled | -0.115 | +0.054 | -0.030 | 0/2 | +0.191 |
| Covariance-only alignment (lag 0) | unlabelled | +0.406 | +0.312 | +0.359 | 0/2 | – |
| TLMA: time-lagged moment alignment | unlabelled | +0.353 | +0.251 | +0.302 | 0/2 | – |
| BR-TLMA: behaviour-reweighted TLMA | unlabelled | +0.262 | +0.272 | +0.267 | 0/2 | – |
| GRU backbone, frozen, per-day z-score | unlabelled (norm. stats) | +0.559 | +0.507 | +0.533 | 2/2 | +0.004 |
| GRU few-shot: readout refit with today's labels | labels | +0.599 | +0.537 | +0.568 | 2/2 | +0.017 |
| NoMAD-style alignment (scaled down) | unlabelled | +0.572 | +0.523 | +0.548 | 2/2 | +0.013 |
| GRU trained with drift augmentation (after Sussillo 2016) | unlabelled (norm. stats) | +0.597 | +0.543 | +0.570 | 2/2 | +0.033 |
| GRU + TLMA | unlabelled | +0.459 | +0.490 | +0.474 | 2/2 | +0.046 |
| GRU + BR-TLMA | unlabelled | +0.459 | +0.490 | +0.474 | 2/2 | +0.046 |

Paired against the direct parent:

| Comparison | mean Δ R² | pairs better (seed×day) | days better (seed-avg) |
|---|---|---|---|
| Frozen WF, per-day z-score (FALCON-style zero-shot) vs Frozen WF, held-in normalisation | +0.106 | 2/2 | 2/2 |
| Frozen WF, held-in normalisation, z clipped to ±5 vs Frozen WF, held-in normalisation | +0.022 | 1/2 | 1/2 |
| WF few-shot: refit on held-in + today's labels vs Frozen WF, per-day z-score (FALCON-style zero-shot) | +0.050 | 2/2 | 2/2 |
| Covariance-only alignment (lag 0) vs PCA latents, frozen, per-day z-score | -0.004 | 0/2 | 0/2 |
| TLMA: time-lagged moment alignment vs PCA latents, frozen, per-day z-score | -0.061 | 0/2 | 0/2 |
| TLMA: time-lagged moment alignment vs Covariance-only alignment (lag 0) | -0.057 | 0/2 | 0/2 |
| BR-TLMA: behaviour-reweighted TLMA vs TLMA: time-lagged moment alignment | -0.035 | 1/2 | 1/2 |
| GRU few-shot: readout refit with today's labels vs GRU backbone, frozen, per-day z-score | +0.035 | 10/10 | 2/2 |
| NoMAD-style alignment (scaled down) vs GRU backbone, frozen, per-day z-score | +0.015 | 7/10 | 2/2 |
| GRU + TLMA vs GRU backbone, frozen, per-day z-score | -0.059 | 0/10 | 0/2 |
| GRU + BR-TLMA vs GRU + TLMA | +0.000 | 0/10 | 0/2 |
| GRU backbone, frozen, per-day z-score vs Frozen WF, per-day z-score (FALCON-style zero-shot) | +0.142 | 2/2 | 2/2 |

_rows from git bd86777; uncommitted code: False_

### M2 · dev

| Method | Uses today's | 2020-10-27 (+7 d) | 2020-10-28 (+8 d) | mean | days > ref | seed SD |
|---|---|---|---|---|---|---|
| Frozen WF, held-in normalisation | nothing | +0.064 | -0.547 | -0.241 | 0/2 | – |
| Frozen WF, held-in normalisation, z clipped to ±5 | nothing | +0.138 | +0.029 | +0.083 | 0/2 | – |
| Frozen WF, per-day z-score (FALCON-style zero-shot) | unlabelled (norm. stats) | +0.173 | +0.279 | +0.226 | – | – |
| WF few-shot: refit on held-in + today's labels | labels | +0.206 | +0.298 | +0.252 | 2/2 | – |
| WF few-shot: today's labels only | labels | +0.152 | +0.178 | +0.165 | 0/2 | – |
| PCA latents, frozen, per-day z-score | unlabelled (norm. stats) | +0.150 | +0.194 | +0.172 | 0/2 | – |
| FA + Procrustes (Degenhart 2020 style) | unlabelled | +0.122 | +0.131 | +0.127 | 0/2 | +0.020 |
| Covariance-only alignment (lag 0) | unlabelled | +0.161 | +0.191 | +0.176 | 0/2 | – |
| TLMA: time-lagged moment alignment | unlabelled | +0.142 | +0.189 | +0.166 | 0/2 | – |
| BR-TLMA: behaviour-reweighted TLMA | unlabelled | +0.154 | +0.171 | +0.163 | 0/2 | – |
| GRU backbone, frozen, per-day z-score | unlabelled (norm. stats) | +0.127 | +0.220 | +0.173 | 0/2 | +0.038 |
| GRU few-shot: readout refit with today's labels | labels | +0.168 | +0.230 | +0.199 | 0/2 | +0.026 |
| NoMAD-style alignment (scaled down) | unlabelled | +0.115 | +0.209 | +0.162 | 0/2 | +0.036 |
| GRU trained with drift augmentation (after Sussillo 2016) | unlabelled (norm. stats) | +0.126 | +0.190 | +0.158 | 0/2 | +0.010 |
| GRU + TLMA | unlabelled | +0.127 | +0.220 | +0.173 | 0/2 | +0.037 |
| GRU + BR-TLMA | unlabelled | +0.123 | +0.216 | +0.170 | 0/2 | +0.035 |

Paired against the direct parent:

| Comparison | mean Δ R² | pairs better (seed×day) | days better (seed-avg) |
|---|---|---|---|
| Frozen WF, per-day z-score (FALCON-style zero-shot) vs Frozen WF, held-in normalisation | +0.467 | 2/2 | 2/2 |
| Frozen WF, held-in normalisation, z clipped to ±5 vs Frozen WF, held-in normalisation | +0.324 | 2/2 | 2/2 |
| WF few-shot: refit on held-in + today's labels vs Frozen WF, per-day z-score (FALCON-style zero-shot) | +0.026 | 2/2 | 2/2 |
| Covariance-only alignment (lag 0) vs PCA latents, frozen, per-day z-score | +0.004 | 1/2 | 1/2 |
| TLMA: time-lagged moment alignment vs PCA latents, frozen, per-day z-score | -0.006 | 0/2 | 0/2 |
| TLMA: time-lagged moment alignment vs Covariance-only alignment (lag 0) | -0.010 | 0/2 | 0/2 |
| BR-TLMA: behaviour-reweighted TLMA vs TLMA: time-lagged moment alignment | -0.003 | 1/2 | 1/2 |
| GRU few-shot: readout refit with today's labels vs GRU backbone, frozen, per-day z-score | +0.026 | 10/10 | 2/2 |
| NoMAD-style alignment (scaled down) vs GRU backbone, frozen, per-day z-score | -0.011 | 2/10 | 0/2 |
| GRU + TLMA vs GRU backbone, frozen, per-day z-score | -0.000 | 6/10 | 1/2 |
| GRU + BR-TLMA vs GRU + TLMA | -0.004 | 2/10 | 0/2 |
| GRU backbone, frozen, per-day z-score vs Frozen WF, per-day z-score (FALCON-style zero-shot) | -0.053 | 0/2 | 0/2 |

_rows from git 1c73711; uncommitted code: False_

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
