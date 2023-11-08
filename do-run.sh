#!/usr/bin/env bash

set -x
source /helm/private_helm_env/bin/activate

export CONF_NAME=$(basename -s .conf "$1")

timeout --foreground 120m helm-run \
  --output-path /results \
  --conf-paths "$1" \
  --suite "$2" \
  --max-eval-instances 100 \
  -n 30 | tee "/results/helm-run-$CONF_NAME-$2.log"

helm-summarize \
  --output-path /results \
  --suite "$2" \
  -n 30 | tee "/results/helm-summarize-$CONF_NAME-$2.log"

python3 /helm/neurIPS_eval_scripts/process_helm.py \
  --dir /results \
  --idx "$2"
