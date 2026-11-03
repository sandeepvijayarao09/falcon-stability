| Method | Uses today's | H1 R² [95% CI] | H1 Δ vs FALCON zero-shot | M1 R² [95% CI] | M1 Δ vs FALCON zero-shot |
|---|---|---|---|---|---|
| Frozen WF, held-in normalisation (strict zero-shot) | none | -0.017 [-0.062, +0.033] | +0.021 [-0.038, +0.092] | -4.440 [-5.220, -3.619] | -4.804 [-5.686, -3.923] |
| Frozen WF, per-day z-score (FALCON zero-shot reference) | none | -0.038 [-0.125, +0.039] | - | +0.365 [+0.303, +0.466] | - |
| WF few-shot: refit on held-in + today's labels | labels | -0.035 [-0.125, +0.043] | +0.003 [-0.001, +0.007] | +0.398 [+0.347, +0.492] | +0.033 [+0.022, +0.052] |
| WF few-shot: today's labels only | labels | -0.005 [-0.018, +0.005] | +0.032 [-0.045, +0.122] | +0.344 [+0.255, +0.423] | -0.021 [-0.071, +0.051] |
| PCA latents, frozen | none | -0.013 [-0.053, +0.016] | +0.025 [-0.033, +0.083] | +0.357 [+0.289, +0.455] | -0.008 [-0.014, +0.002] |
| FA + Procrustes stabilizer (Degenhart 2020 style) | unlabelled | -0.052 [-0.084, -0.019] | -0.014 [-0.072, +0.050] | +0.317 [+0.264, +0.400] | -0.048 [-0.066, -0.016] |
| Covariance-only alignment (TLMA ablation, lag 0) | unlabelled | -0.017 [-0.062, +0.015] | +0.021 [-0.034, +0.076] | +0.354 [+0.301, +0.441] | -0.011 [-0.025, -0.002] |
| TLMA: time-lagged moment alignment (ours) | unlabelled | -0.029 [-0.084, +0.010] | +0.009 [-0.043, +0.058] | +0.352 [+0.300, +0.441] | -0.012 [-0.024, -0.003] |
| BR-TLMA: behaviour-reweighted TLMA (ours) | unlabelled | -0.017 [-0.064, +0.016] | +0.021 [-0.034, +0.075] | +0.235 [+0.163, +0.295] | -0.130 [-0.219, -0.031] |
| GRU dynamics backbone, frozen, per-day z-score | none | -0.013 [-0.058, +0.032] | +0.025 [-0.025, +0.082] | +0.388 [+0.306, +0.479] | +0.023 [-0.019, +0.074] |
| GRU few-shot: readout refit with today's labels | labels | +0.009 [-0.036, +0.051] | +0.046 [-0.006, +0.105] | +0.438 [+0.370, +0.517] | +0.073 [+0.045, +0.122] |
| NoMAD-style alignment (Karpowicz 2022, scaled down) | unlabelled | -0.019 [-0.063, +0.025] | +0.019 [-0.030, +0.075] | +0.313 [+0.217, +0.429] | -0.051 [-0.108, -0.010] |
| GRU trained with drift augmentation (after Sussillo 2016) | none | -0.008 [-0.056, +0.034] | +0.030 [-0.020, +0.083] | +0.381 [+0.312, +0.466] | +0.017 [-0.013, +0.064] |
| GRU + TLMA (ours) | unlabelled | -0.025 [-0.076, +0.023] | +0.012 [-0.034, +0.065] | +0.375 [+0.333, +0.434] | +0.010 [-0.032, +0.056] |
| GRU + BR-TLMA (ours) | unlabelled | -0.007 [-0.051, +0.035] | +0.031 [-0.021, +0.090] | +0.381 [+0.333, +0.443] | +0.016 [-0.023, +0.064] |
