#!/usr/bin/env bash

source /helm/private_helm_env/bin/activate

if [[ "$1" == "big" ]]; then
  export FIRST_CONF="/helm/configs/run_specs_open_2000_budget.conf"
  export SECOND_CONF="/helm/configs/run_specs_closed_5000_budget.conf"
elif [[ "$1" == "small" ]]; then
  export FIRST_CONF="/helm/configs/run_specs_open_100_budget.conf"
  export SECOND_CONF="/helm/configs/run_specs_closed_100_budget.conf"
else
  echo "Either big or small for the first arg"
  exit 1
fi

echo "Going to run $FIRST_CONF then $SECOND_CONF"

date > "/results/helm-run-open-set-$CONF_NAME-$2.log"

timeout --foreground 300m helm-run \
  --output-path /results \
  --conf-paths "$FIRST_CONF" \
  --suite "$2" \
  --max-eval-instances 100 \
  -n 30 | tee "/results/helm-run-open-set-$CONF_NAME-$2.log"

date >> "/results/helm-run-open-set-$CONF_NAME-$2.log"

date > "/results/helm-run-hidden-set-$CONF_NAME-$2.log"

timeout --foreground 600m helm-run \
  --output-path /results \
  --conf-paths "$SECOND_CONF" \
  --suite "$2" \
  --max-eval-instances 100 \
  -n 30 | tee "/results/helm-run-hidden-set-$CONF_NAME-$2.log"

date >> "/results/helm-run-hidden-set-$CONF_NAME-$2.log"

helm-summarize \
  --output-path /results \
  --suite "$2" \
  -n 30 | tee "/results/helm-summarize-$CONF_NAME-$2.log"

python3 /helm/neurIPS_eval_scripts/process_helm.py \
  --dir /results \
  --idx "$2"

python3 /helm/neurIPS_eval_scripts/process_helm.py \
  --dir /results \
  --idx "$2" \
  --hidden
