### M1-A + M1-B pooled · test

| Method | Uses today's | R² mean [95% CI over 7 days] | Δ vs FALCON-style [95% CI] | days > ref | seed SD |
|---|---|---|---|---|---|
| Frozen WF, held-in normalisation | nothing | -1.779 [-3.544, -0.278] | -2.142 [-3.909, -0.644] | 0/7 | – |
| Frozen WF, held-in normalisation, z clipped to ±5 | nothing | +0.002 [-0.210, +0.214] | -0.361 [-0.569, -0.159] | 0/7 | – |
| Frozen WF, per-day z-score (FALCON-style zero-shot) | unlabelled (norm. stats) | +0.363 [+0.322, +0.411] | – | – | – |
| WF few-shot: refit on held-in + today's labels | labels | +0.394 [+0.359, +0.435] | +0.030 [+0.019, +0.042] | 7/7 | – |
| WF few-shot: today's labels only | labels | +0.342 [+0.305, +0.378] | -0.021 [-0.050, +0.010] | 3/7 | – |
| PCA latents, frozen, per-day z-score | unlabelled (norm. stats) | +0.348 [+0.306, +0.398] | -0.015 [-0.034, +0.000] | 2/7 | – |
| FA + Procrustes (Degenhart 2020 style) | unlabelled | +0.139 [-0.001, +0.271] | -0.224 [-0.383, -0.087] | 0/7 | +0.024 |
| Covariance-only alignment (lag 0) | unlabelled | +0.354 [+0.318, +0.395] | -0.009 [-0.028, +0.006] | 3/7 | – |
| TLMA: time-lagged moment alignment | unlabelled | +0.351 [+0.319, +0.388] | -0.012 [-0.033, +0.008] | 2/7 | – |
| BR-TLMA: behaviour-reweighted TLMA | unlabelled | +0.267 [+0.219, +0.325] | -0.096 [-0.153, -0.043] | 1/7 | – |
| GRU backbone, frozen, per-day z-score | unlabelled (norm. stats) | +0.438 [+0.379, +0.495] | +0.075 [+0.034, +0.112] | 6/7 | +0.007 |
| GRU few-shot: readout refit with today's labels | labels | +0.493 [+0.440, +0.544] | +0.130 [+0.086, +0.168] | 7/7 | +0.006 |
| NoMAD-style alignment (scaled down) | unlabelled | +0.232 [+0.009, +0.436] | -0.131 [-0.383, +0.072] | 3/7 | +0.196 |
| GRU trained with drift augmentation (after Sussillo 2016) | unlabelled (norm. stats) | +0.358 [+0.173, +0.490] | -0.005 [-0.172, +0.109] | 4/7 | +0.221 |
| GRU + TLMA | unlabelled | +0.430 [+0.368, +0.495] | +0.066 [+0.018, +0.116] | 6/7 | +0.022 |
| GRU + BR-TLMA | unlabelled | +0.409 [+0.362, +0.462] | +0.046 [+0.012, +0.080] | 6/7 | +0.034 |

Paired against the direct parent:

| Comparison | mean Δ R² | pairs better (seed×day) | days better (seed-avg) | 95% CI over days |
|---|---|---|---|---|
| Frozen WF, per-day z-score (FALCON-style zero-shot) vs Frozen WF, held-in normalisation | +2.142 | 7/7 | 7/7 | [+0.644, +3.909] |
| Frozen WF, held-in normalisation, z clipped to ±5 vs Frozen WF, held-in normalisation | +1.781 | 5/7 | 5/7 | [+0.477, +3.328] |
| WF few-shot: refit on held-in + today's labels vs Frozen WF, per-day z-score (FALCON-style zero-shot) | +0.030 | 7/7 | 7/7 | [+0.019, +0.042] |
| Covariance-only alignment (lag 0) vs PCA latents, frozen, per-day z-score | +0.006 | 4/7 | 4/7 | [-0.004, +0.015] |
| TLMA: time-lagged moment alignment vs PCA latents, frozen, per-day z-score | +0.003 | 4/7 | 4/7 | [-0.017, +0.024] |
| TLMA: time-lagged moment alignment vs Covariance-only alignment (lag 0) | -0.003 | 2/7 | 2/7 | [-0.018, +0.011] |
| BR-TLMA: behaviour-reweighted TLMA vs TLMA: time-lagged moment alignment | -0.084 | 1/7 | 1/7 | [-0.137, -0.031] |
| GRU few-shot: readout refit with today's labels vs GRU backbone, frozen, per-day z-score | +0.055 | 35/35 | 7/7 | [+0.045, +0.066] |
| NoMAD-style alignment (scaled down) vs GRU backbone, frozen, per-day z-score | -0.206 | 12/35 | 3/7 | [-0.420, -0.040] |
| GRU + TLMA vs GRU backbone, frozen, per-day z-score | -0.008 | 18/35 | 3/7 | [-0.032, +0.014] |
| GRU + BR-TLMA vs GRU + TLMA | -0.021 | 6/35 | 2/7 | [-0.043, -0.001] |
| GRU backbone, frozen, per-day z-score vs Frozen WF, per-day z-score (FALCON-style zero-shot) | +0.075 | 6/7 | 6/7 | [+0.034, +0.112] |

_rows from git 1cb3c13,bd86777; uncommitted code: False_

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

### M1-B · test

| Method | Uses today's | 2012-12-13 (+1 d) | 2012-12-14 (+2 d) | 2012-12-18 (+6 d) | 2012-12-19 (+7 d) | mean | days > ref | seed SD |
|---|---|---|---|---|---|---|---|---|
| Frozen WF, held-in normalisation | nothing | +0.150 | +0.406 | +0.306 | +0.002 | +0.216 | 0/4 | – |
| Frozen WF, held-in normalisation, z clipped to ±5 | nothing | +0.191 | +0.401 | +0.338 | -0.013 | +0.230 | 0/4 | – |
| Frozen WF, per-day z-score (FALCON-style zero-shot) | unlabelled (norm. stats) | +0.311 | +0.408 | +0.423 | +0.305 | +0.362 | – | – |
| WF few-shot: refit on held-in + today's labels | labels | +0.361 | +0.428 | +0.430 | +0.342 | +0.390 | 4/4 | – |
| WF few-shot: today's labels only | labels | +0.319 | +0.351 | +0.377 | +0.313 | +0.340 | 2/4 | – |
| PCA latents, frozen, per-day z-score | unlabelled (norm. stats) | +0.290 | +0.422 | +0.356 | +0.299 | +0.342 | 1/4 | – |
| FA + Procrustes (Degenhart 2020 style) | unlabelled | +0.168 | -0.143 | -0.060 | +0.055 | +0.005 | 0/4 | +0.052 |
| Covariance-only alignment (lag 0) | unlabelled | +0.317 | +0.421 | +0.363 | +0.317 | +0.354 | 3/4 | – |
| TLMA: time-lagged moment alignment | unlabelled | +0.348 | +0.383 | +0.362 | +0.307 | +0.350 | 2/4 | – |
| BR-TLMA: behaviour-reweighted TLMA | unlabelled | +0.237 | +0.420 | +0.260 | +0.249 | +0.292 | 1/4 | – |
| GRU backbone, frozen, per-day z-score | unlabelled (norm. stats) | +0.445 | +0.509 | +0.555 | +0.393 | +0.475 | 4/4 | +0.012 |
| GRU few-shot: readout refit with today's labels | labels | +0.503 | +0.566 | +0.592 | +0.475 | +0.534 | 4/4 | +0.016 |
| NoMAD-style alignment (scaled down) | unlabelled | +0.475 | +0.511 | +0.582 | +0.174 | +0.435 | 3/4 | +0.023 |
| GRU trained with drift augmentation (after Sussillo 2016) | unlabelled (norm. stats) | -0.167 | +0.521 | +0.545 | +0.466 | +0.341 | 3/4 | +0.394 |
| GRU + TLMA | unlabelled | +0.472 | +0.501 | +0.575 | +0.334 | +0.471 | 4/4 | +0.020 |
| GRU + BR-TLMA | unlabelled | +0.417 | +0.434 | +0.536 | +0.334 | +0.431 | 4/4 | +0.041 |

Paired against the direct parent:

| Comparison | mean Δ R² | pairs better (seed×day) | days better (seed-avg) |
|---|---|---|---|
| Frozen WF, per-day z-score (FALCON-style zero-shot) vs Frozen WF, held-in normalisation | +0.146 | 4/4 | 4/4 |
| Frozen WF, held-in normalisation, z clipped to ±5 vs Frozen WF, held-in normalisation | +0.014 | 2/4 | 2/4 |
| WF few-shot: refit on held-in + today's labels vs Frozen WF, per-day z-score (FALCON-style zero-shot) | +0.028 | 4/4 | 4/4 |
| Covariance-only alignment (lag 0) vs PCA latents, frozen, per-day z-score | +0.012 | 3/4 | 3/4 |
| TLMA: time-lagged moment alignment vs PCA latents, frozen, per-day z-score | +0.008 | 3/4 | 3/4 |
| TLMA: time-lagged moment alignment vs Covariance-only alignment (lag 0) | -0.004 | 1/4 | 1/4 |
| BR-TLMA: behaviour-reweighted TLMA vs TLMA: time-lagged moment alignment | -0.059 | 1/4 | 1/4 |
| GRU few-shot: readout refit with today's labels vs GRU backbone, frozen, per-day z-score | +0.059 | 20/20 | 4/4 |
| NoMAD-style alignment (scaled down) vs GRU backbone, frozen, per-day z-score | -0.040 | 12/20 | 3/4 |
| GRU + TLMA vs GRU backbone, frozen, per-day z-score | -0.005 | 13/20 | 2/4 |
| GRU + BR-TLMA vs GRU + TLMA | -0.040 | 0/20 | 0/4 |
| GRU backbone, frozen, per-day z-score vs Frozen WF, per-day z-score (FALCON-style zero-shot) | +0.114 | 4/4 | 4/4 |

_rows from git bd86777; uncommitted code: False_

### M2 · test

| Method | Uses today's | 2020-10-30 (+2 d) | 2020-11-18 (+21 d) | 2020-11-19 (+22 d) | 2020-11-24 (+27 d) | mean | days > ref | seed SD |
|---|---|---|---|---|---|---|---|---|
| Frozen WF, held-in normalisation | nothing | +0.095 | +0.236 | -0.063 | -0.106 | +0.041 | 0/4 | – |
| Frozen WF, held-in normalisation, z clipped to ±5 | nothing | +0.100 | +0.211 | +0.048 | -0.059 | +0.075 | 0/4 | – |
| Frozen WF, per-day z-score (FALCON-style zero-shot) | unlabelled (norm. stats) | +0.155 | +0.293 | +0.150 | +0.069 | +0.167 | – | – |
| WF few-shot: refit on held-in + today's labels | labels | +0.193 | +0.308 | +0.183 | +0.122 | +0.202 | 4/4 | – |
| WF few-shot: today's labels only | labels | +0.176 | +0.093 | +0.136 | +0.143 | +0.137 | 2/4 | – |
| PCA latents, frozen, per-day z-score | unlabelled (norm. stats) | +0.113 | +0.242 | +0.119 | +0.073 | +0.137 | 1/4 | – |
| FA + Procrustes (Degenhart 2020 style) | unlabelled | +0.083 | +0.167 | +0.115 | +0.075 | +0.110 | 1/4 | +0.008 |
| Covariance-only alignment (lag 0) | unlabelled | +0.115 | +0.249 | +0.130 | +0.072 | +0.141 | 1/4 | – |
| TLMA: time-lagged moment alignment | unlabelled | +0.103 | +0.240 | +0.143 | +0.067 | +0.138 | 0/4 | – |
| BR-TLMA: behaviour-reweighted TLMA | unlabelled | +0.102 | +0.218 | +0.133 | +0.068 | +0.130 | 0/4 | – |
| GRU backbone, frozen, per-day z-score | unlabelled (norm. stats) | +0.145 | +0.212 | +0.131 | +0.088 | +0.144 | 1/4 | +0.007 |
| GRU few-shot: readout refit with today's labels | labels | +0.157 | +0.223 | +0.153 | +0.110 | +0.161 | 3/4 | +0.007 |
| NoMAD-style alignment (scaled down) | unlabelled | +0.144 | +0.209 | +0.128 | +0.086 | +0.142 | 1/4 | +0.005 |
| GRU trained with drift augmentation (after Sussillo 2016) | unlabelled (norm. stats) | +0.122 | +0.208 | +0.144 | +0.099 | +0.143 | 1/4 | +0.019 |
| GRU + TLMA | unlabelled | +0.142 | +0.220 | +0.128 | +0.083 | +0.143 | 1/4 | +0.006 |
| GRU + BR-TLMA | unlabelled | +0.139 | +0.214 | +0.123 | +0.081 | +0.139 | 1/4 | +0.006 |

Paired against the direct parent:

| Comparison | mean Δ R² | pairs better (seed×day) | days better (seed-avg) |
|---|---|---|---|
| Frozen WF, per-day z-score (FALCON-style zero-shot) vs Frozen WF, held-in normalisation | +0.126 | 4/4 | 4/4 |
| Frozen WF, held-in normalisation, z clipped to ±5 vs Frozen WF, held-in normalisation | +0.034 | 3/4 | 3/4 |
| WF few-shot: refit on held-in + today's labels vs Frozen WF, per-day z-score (FALCON-style zero-shot) | +0.035 | 4/4 | 4/4 |
| Covariance-only alignment (lag 0) vs PCA latents, frozen, per-day z-score | +0.005 | 3/4 | 3/4 |
| TLMA: time-lagged moment alignment vs PCA latents, frozen, per-day z-score | +0.001 | 1/4 | 1/4 |
| TLMA: time-lagged moment alignment vs Covariance-only alignment (lag 0) | -0.003 | 1/4 | 1/4 |
| BR-TLMA: behaviour-reweighted TLMA vs TLMA: time-lagged moment alignment | -0.008 | 1/4 | 1/4 |
| GRU few-shot: readout refit with today's labels vs GRU backbone, frozen, per-day z-score | +0.017 | 20/20 | 4/4 |
| NoMAD-style alignment (scaled down) vs GRU backbone, frozen, per-day z-score | -0.002 | 5/20 | 0/4 |
| GRU + TLMA vs GRU backbone, frozen, per-day z-score | -0.001 | 6/20 | 1/4 |
| GRU + BR-TLMA vs GRU + TLMA | -0.004 | 2/20 | 0/4 |
| GRU backbone, frozen, per-day z-score vs Frozen WF, per-day z-score (FALCON-style zero-shot) | -0.023 | 1/4 | 1/4 |

_rows from git da99e1d; uncommitted code: False_

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
