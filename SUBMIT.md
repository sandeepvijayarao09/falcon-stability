# Submitting to the FALCON leaderboard (EvalAI)

Everything here has been built and tested locally, but **nothing has been submitted**. You submit yourself, under your own EvalAI account.

## What is ready

Each payload in `submission/artifacts/` is a frozen decoder fitted on held-in calibration data. Every one is **zero-shot** in FALCON's terms: it uses per-session normalisation statistics from calibration files, but no held-out labels. That is the same data use as the official zero-shot Wiener-filter baseline.

| Payload (`--build-arg METHOD=`) | Decoder | Normalisation | H1 | M1 | M2 | In Docker? |
|---|---|---|---|---|---|---|
| `wf` | Wiener filter | per-day, smoothed counts (pre-specified, = research tables) | 0.171 | 0.386 | 0.012 | H1, M1, M2 |
| `gru` | small GRU | per-day, smoothed counts (pre-specified) | 0.069 | 0.458 | 0.087 | H1, M1, M2 |
| `wf_rawnorm` | Wiener filter | per-file, raw counts (= official demo) | 0.195 | 0.375 | 0.100 | not yet |
| `gru_rawnorm` | small GRU | per-file, raw counts | 0.149 | 0.437 | 0.094 | H1, M1, M2 |

Numbers are **held-in minival R²** from FALCON's own local evaluator, from [`results/evalai_local/`](results/evalai_local/). Local minival covers held-in sessions only; held-out scores exist only on EvalAI.

**Two equivalence checks:**
- **Docker vs native.** For every payload marked in the last column, the `linux/amd64` Docker image reproduced the native score to within 1e-7 ([`results/evalai_local/docker_check.txt`](results/evalai_local/docker_check.txt)). The `wf_rawnorm` images use the same Dockerfile and decoder code but weren't run in Docker, because Docker Desktop was closed at the time. Run step 3 for them before pushing.
- **Online vs offline.** `tests/test_core.py::test_online_submission_decoder_matches_offline_pipeline` checks that the online decoder, which runs one 20 ms bin at a time, reproduces the offline pipeline behind the README tables.

**Which to submit.** The pre-specified choice is `wf` and `gru`, which match the README's analysis. The `*_rawnorm` variants score better on H1 and M2 held-in minival but worse on M1. Picking per dataset by minival is a legitimate use of the public phase, but say so in the method description. `wf_rawnorm` reproduces the official baseline (0.195 on H1), so it is a reproduction check, not a new entry.

## 1. One-time setup

1. Create an account at <https://eval.ai>, open the FALCON challenge (<https://eval.ai/web/challenges/challenge-page/2319>), and create a **participant team** on the challenge page. The CLI instructions on the *Submit* tab appear only once you have a team; refresh if they don't.
2. Make sure Docker runs without `sudo`: `docker info` must work. On a Mac that means Docker Desktop is running.
3. Install the EvalAI CLI in its own environment (`pip install evalai` can fail on Python 3.11):
   ```bash
   python3 -m venv ~/.evalai-cli && ~/.evalai-cli/bin/pip install evalai
   ~/.evalai-cli/bin/evalai set_token <token from your EvalAI profile page>
   ```

## 2. Payloads

The payloads are committed (14–420 kB each). To rebuild them from the data:
```bash
.venv/bin/python scripts/get_data.py h1 m1 m2                         # verifies checksums; M2 is ~16 GB
.venv/bin/python scripts/build_submission.py --task h1 --method gru                 # -> h1_gru.pt
.venv/bin/python scripts/build_submission.py --task h1 --method gru --norm file_raw # -> h1_gru_rawnorm.pt
```

## 3. Build and test an image locally

From the repo root (`--platform linux/amd64` because EvalAI runs x86-64):
```bash
docker build --platform linux/amd64 -t falcon-stability-h1-gru -f submission/Dockerfile \
  --build-arg SPLIT=h1 --build-arg METHOD=gru .
docker run --rm --platform linux/amd64 -v "$(pwd)/data:/dataset/evaluation_data:ro" \
  -e EVALUATION_LOC=local falcon-stability-h1-gru
```
The last line should include `'Held In R2 Mean': ...` matching the table above (0.069 for H1 GRU). If it differs, stop and don't push.

## 4. Push

Copy the exact phase name from the challenge's *Submit* tab; it should look like `few-shot-minival-2319` or `few-shot-test-2319`. Submit to minival first, privately:
```bash
~/.evalai-cli/bin/evalai push falcon-stability-h1-gru:latest --phase <minival phase from the Submit tab> --private
```
Once the EvalAI minival result matches the local number, push the same image to the test phase:
```bash
~/.evalai-cli/bin/evalai push falcon-stability-h1-gru:latest --phase <test phase from the Submit tab> --private
```
The image's default `PHASE` is `minival`. If the challenge page says the test phase needs `PHASE=test` inside the container, build a separate tag with `ENV PHASE=test` and push that. The official demo Dockerfiles set it this way. Each image decodes one dataset (set by `SPLIT` at build time), so H1, M1 and M2 are separate submissions. Submissions have a **6-hour limit**. FALCON's M1 track is monkey L (M1-A) only; M1-B has no leaderboard split in `falcon-challenge` 1.0.2.

Keep submissions `--private` until you have looked at the result, then make them public from *My Submissions* if you want them on the leaderboard. In the method description, state that the decoder is zero-shot, uses unlabelled calibration statistics only, and which normalisation it uses.

## 5. After submitting

Add the held-out numbers to the README's "Checks against the paper" table, next to FALCON Table 1's zero-shot WF: 0.16 on H1, 0.34 on M1-A, 0.06 on M2.
