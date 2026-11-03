| Method | Uses today's | H1 R² [95% CI] | H1 Δ vs FALCON zero-shot | M1 R² [95% CI] | M1 Δ vs FALCON zero-shot |
|---|---|---|---|---|---|
| Frozen WF, held-in normalisation (strict zero-shot) | none | -0.058 [-0.145, +0.026] | -0.074 [-0.146, -0.020] | +0.035 [-0.006, +0.076] | -0.387 [-0.435, -0.338] |
| Frozen WF, per-day z-score (FALCON zero-shot reference) | none | +0.016 [-0.053, +0.080] | - | +0.421 [+0.414, +0.428] | - |
| WF few-shot: refit on held-in + today's labels | labels | +0.023 [-0.048, +0.088] | +0.007 [+0.004, +0.008] | +0.502 [+0.478, +0.526] | +0.081 [+0.064, +0.098] |
| WF few-shot: today's labels only | labels | -0.032 [-0.058, -0.013] | -0.048 [-0.128, +0.031] | +0.408 [+0.340, +0.475] | -0.013 [-0.074, +0.047] |
| PCA latents, frozen | none | -0.026 [-0.061, +0.018] | -0.042 [-0.101, +0.023] | +0.480 [+0.462, +0.498] | +0.059 [+0.048, +0.070] |
| FA + Procrustes stabilizer (Degenhart 2020 style) | unlabelled | -0.061 [-0.107, -0.009] | -0.077 [-0.160, +0.014] | +0.451 [+0.420, +0.482] | +0.030 [+0.006, +0.054] |
| Covariance-only alignment (TLMA ablation, lag 0) | unlabelled | -0.028 [-0.062, +0.014] | -0.044 [-0.105, +0.022] | +0.469 [+0.457, +0.481] | +0.048 [+0.042, +0.053] |
| TLMA: time-lagged moment alignment (ours) | unlabelled | -0.038 [-0.068, -0.003] | -0.055 [-0.115, +0.014] | +0.465 [+0.455, +0.475] | +0.044 [+0.041, +0.047] |
| BR-TLMA: behaviour-reweighted TLMA (ours) | unlabelled | -0.021 [-0.052, +0.013] | -0.037 [-0.091, +0.022] | +0.482 [+0.465, +0.498] | +0.060 [+0.051, +0.070] |
| GRU dynamics backbone, frozen, per-day z-score | none | -0.057 [-0.137, +0.013] | -0.073 [-0.111, -0.039] | +0.567 [+0.540, +0.593] | +0.146 [+0.126, +0.165] |
| GRU few-shot: readout refit with today's labels | labels | -0.016 [-0.081, +0.035] | -0.032 [-0.062, +0.001] | +0.580 [+0.546, +0.615] | +0.159 [+0.132, +0.187] |
| NoMAD-style alignment (Karpowicz 2022, scaled down) | unlabelled | -0.044 [-0.119, +0.022] | -0.060 [-0.091, -0.032] | +0.467 [+0.407, +0.526] | +0.045 [-0.021, +0.112] |
| GRU trained with drift augmentation (after Sussillo 2016) | none | -0.025 [-0.081, +0.027] | -0.042 [-0.091, +0.004] | +0.586 [+0.582, +0.589] | +0.165 [+0.154, +0.175] |
| GRU + TLMA (ours) | unlabelled | -0.067 [-0.149, -0.001] | -0.084 [-0.118, -0.049] | +0.413 [+0.402, +0.424] | -0.008 [-0.027, +0.010] |
| GRU + BR-TLMA (ours) | unlabelled | -0.067 [-0.149, -0.001] | -0.083 [-0.117, -0.049] | +0.465 [+0.460, +0.470] | +0.044 [+0.032, +0.056] |
