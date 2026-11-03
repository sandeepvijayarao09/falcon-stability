# FALCON EvalAI submission image (CPU). Build from the repo root:
#   docker build -t falcon-stability-h1-wf -f submission/Dockerfile \
#     --build-arg SPLIT=h1 --build-arg METHOD=wf .
FROM python:3.11-slim

ARG SPLIT=h1
ARG METHOD=wf
RUN pip install --no-cache-dir --extra-index-url https://download.pytorch.org/whl/cpu \
        torch==2.15.0 numpy==2.4.6 scipy==1.17.1 scikit-learn==1.9.1 pandas==3.1.0 falcon-challenge==1.0.2

WORKDIR /submission_code
COPY src/ src/
COPY pyproject.toml .
RUN pip install --no-cache-dir --no-deps -e .
COPY submission/decode.py decode.py
COPY submission/artifacts/${SPLIT}_${METHOD}.pt payload.pt

ENV SPLIT=${SPLIT} PHASE=minival BATCH_SIZE=1 EVALUATION_LOC=remote
ENV PREDICTION_PATH=/submission/submission.csv PREDICTION_PATH_LOCAL=/tmp/submission.pkl GT_PATH=/tmp/ground_truth.pkl
# EvalAI mounts the evaluation data here (same as the official Dockerfiles).
ENV EVAL_DATA_PATH=/dataset/evaluation_data

CMD ["/bin/bash", "-c", "python decode.py --evaluation $EVALUATION_LOC --payload payload.pt --split $SPLIT --phase $PHASE --batch-size $BATCH_SIZE"]
