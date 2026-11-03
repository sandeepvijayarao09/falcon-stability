"""EvalAI entry point (mirrors falcon-challenge's decoder_demos/sklearn_sample.py).

python decode.py --evaluation {local,remote} --payload artifacts/h1_wf.pt --split h1 --phase {minival,test}
"""
import argparse
import json

from falcon_challenge.config import FalconConfig, FalconTask
from falcon_challenge.evaluator import FalconEvaluator

from falcon_stability.submission import StabilityDecoder


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--evaluation", required=True, choices=["local", "remote"])
    ap.add_argument("--payload", required=True)
    ap.add_argument("--split", required=True, choices=["h1", "m1", "m2"])
    ap.add_argument("--phase", default="minival", choices=["minival", "test"])
    ap.add_argument("--batch-size", type=int, default=1)
    ap.add_argument("--out", help="write local metrics as JSON")
    a = ap.parse_args()
    cfg = FalconConfig(task=getattr(FalconTask, a.split))
    decoder = StabilityDecoder(cfg, a.payload, batch_size=a.batch_size)
    ev = FalconEvaluator(eval_remote=a.evaluation == "remote", split=a.split, dataloader_workers=0)
    res = ev.evaluate(decoder, phase=a.phase)
    print(res)
    if a.out and res is not None:
        with open(a.out, "w") as f:
            json.dump(res, f, indent=1, default=float)


if __name__ == "__main__":
    main()
