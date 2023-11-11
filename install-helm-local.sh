#!/usr/bin/env bash

python3 -m venv private_helm_env
source private_helm_env/bin/activate

pip install --upgrade pip
pip install -e .
pip install summ-eval
pip install bert-score
pip install numba
pip install 'jieba==0.42.1'
pip install -U datasets
