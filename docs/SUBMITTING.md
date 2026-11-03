# Submitting to the FALCON leaderboard (EvalAI)

The numbers in this repo come from a **local proxy protocol**: FALCON's held-out *evaluation*
data is private, so held-out calibration files are split in time (see `src/falcon_stability/protocol.py`).
Only an EvalAI submission gives a number that is comparable with the leaderboard. You do the
submission yourself; nothing here uploads anything.

## 1. One-time setup
1. Create an account on [EvalAI](https://eval.ai) and open the FALCON challenge
   (challenge 2319: <https://eval.ai/web/challenges/challenge-page/2319>).
2. Create a participant team from the challenge page. The CLI instructions on the
   *Submit* tab only appear once you have a team; refresh if they don't.
3. Install Docker and make sure `docker info` works **without sudo** (EvalAI's push needs this).
4. Install the CLI in a separate env (`pip install evalai` can fail on Python 3.11):
   ```bash
   python3.10 -m venv ~/.evalai && ~/.evalai/bin/pip install evalai
   ~/.evalai/bin/evalai set_token <your token from the EvalAI profile page>
   ```

## 2. Package a decoder
EvalAI runs your Docker image against the hidden data through the `falcon_challenge` interface:
your decoder class must implement `reset(dataset_tags)`, `predict(neural_observations)` and
`on_done(dones)` (see `falcon_challenge/interface.py`). `reset` receives a file tag, which is how a
per-day method knows which day's calibration statistics to use.

The fastest path is to start from the official example in
[snel-repo/falcon-challenge](https://github.com/snel-repo/falcon-challenge):
`decoder_demos/sklearn_decoder.py`, `sklearn_sample.py` and `sklearn_sample.Dockerfile`.
To submit a method from this repo:
- **Frozen WF, per-day z-score**: this *is* the official sklearn demo (`--mode all`), so submit that
  as a smoke test first.
- **GRU frozen / BR-TLMA**: fit on all held-in data plus each held-out day's calibration file, store
  the per-day statistics (z-score, TLMA map `A`) keyed by `FalconConfig.hash_dataset(tag)`, and
  apply them in `reset`. Run the GRU one step at a time in `predict`, keeping the hidden state per batch item.
  A ready-made wrapper is not in this repo yet (see Next steps in the README).

## 3. Test locally, then push
```bash
docker build -t falcon-mine -f <your>.Dockerfile .
bash test_docker_local.sh --docker-name falcon-mine     # runs on local minival; check the metrics are non-trivial
~/.evalai/bin/evalai push falcon-mine:latest --phase few-shot-minival-2319 --private   # minival first
~/.evalai/bin/evalai push falcon-mine:latest --phase few-shot-test-2319 --private      # then test
```
The exact phase names are on the Submit tab; copy them from there. Submissions have a 6-hour limit.
Use `--private` until you have checked the result, then make it public from the *My Submissions* page.
