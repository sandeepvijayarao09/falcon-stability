"""Sanity check against the falcon-challenge README for H1:
`sklearn_decoder.py --mode all` should print CV fit 0.26 and minival Held In Mean 0.195."""
import numpy as np
from sklearn.linear_model import Ridge
from sklearn.model_selection import GridSearchCV

from falcon_stability.data import load_split
from falcon_stability.decoders import ALPHAS, train_mask
from falcon_stability.features import smooth, zscore_stats
from falcon_stability.metrics import r2_vw

cal = load_split("h1", "held_in_calib")
mv = load_split("h1", "minival")
X = np.concatenate([s.X for s in cal]); Y = np.concatenate([s.Y for s in cal])
M = np.concatenate([s.mask for s in cal])
S = smooth(X)
n = int(0.8 * len(S))
mu, sd = zscore_stats(S[:n])  # reference z-scores with stats of the 80% train split
Z = (S - mu) / sd
m = train_mask(Y, M, drop_still=True)
gs = GridSearchCV(Ridge(), {"alpha": ALPHAS}).fit(Z[:n][m[:n]], Y[:n][m[:n]])
# NB the reference globs files unsorted, so its 80/20 split (and the 0.26) depends on filesystem order.
print(f"CV fit score (uniform R2 on last 20%): {gs.score(Z[n:][m[n:]], Y[n:][m[n:]]):.3f}  (reference 0.26)")

# minival: reference reset() z-scores each file with mean/std of RAW counts of the matching calib file
by_ses = {s.name.split("_ses-")[1]: s for s in cal}
scores, by_day = [], {}
for s in mv:
    c = by_ses[s.name.split("_ses-")[1]]
    mu_c, sd_c = zscore_stats(c.X.astype(float))
    pred = gs.predict((smooth(s.X) - mu_c) / sd_c)  # reference smooths raw counts, then z-scores
    scores.append(r2_vw(s.Y[s.mask], pred[s.mask]))
    y, p = by_day.setdefault(s.day_key, ([], []))
    y.append(s.Y[s.mask]); p.append(pred[s.mask])
print(f"minival R2, mean over files: {np.mean(scores):.3f} +/- {np.std(scores):.3f}")
# falcon_challenge groups H1 sets of one day under one session key and scores per day:
day = [r2_vw(np.concatenate(y), np.concatenate(p)) for y, p in by_day.values()]
print(f"minival Held In Mean R2, per day (FALCON grouping): {np.mean(day):.3f} +/- {np.std(day):.3f}  (reference 0.195)")
