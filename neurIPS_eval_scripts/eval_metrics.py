#these are the metrics we use for evalu
# adapted from https://github.com/Lightning-AI/llm-efficiency-challenge-eval/blob/main/agents/config.py
Open_eval_metrics = {
    "Accuracy": [
        ("core_scenarios.json", "MMLU - EM", False),
        ("core_scenarios.json", "CNN/DailyMail - ROUGE-2", False),
        ("core_scenarios.json", "TruthfulQA - EM", False),
        ("targeted_evaluations.json", "BBQ - EM", False),
        ("core_scenarios.json", "GSM8K - EM", False),
        ("core_scenarios.json", "BIG-bench - EM", False),
    ],

    "Robustness": [
        ("core_scenarios.json", "MMLU - EM (Robustness)", False),
        ("core_scenarios.json", "TruthfulQA - EM (Robustness)", False),
    ],

    "Fairness": [
        ("core_scenarios.json", "MMLU - EM (Fairness)", False),
        ("core_scenarios.json", "TruthfulQA - EM (Fairness)", False),

    ],

    "Bias": [
        ("core_scenarios.json", "CNN/DailyMail - Stereotypes (race)", True),
        ("core_scenarios.json", "CNN/DailyMail - Stereotypes (gender)", True),
        ("core_scenarios.json", "CNN/DailyMail - Representation (race)", True),
        ("core_scenarios.json", "CNN/DailyMail - Representation (gender)", True),
    ],

}