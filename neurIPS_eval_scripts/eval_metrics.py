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


Hidden_eval_metrics = {
    "Accuracy": [
        ("core_scenarios.json", "sam_sum - ROUGE-2", False),
        ("core_scenarios.json", "corr2cause - EM", False),
        ("core_scenarios.json", "ethics_justice - EM", False),
        ("core_scenarios.json", "ethics_commonsense - EM", False),
        ("core_scenarios.json", "ethics_virtue - EM", False),
        ("core_scenarios.json", "ethics_deontology - EM", False),
        ("core_scenarios.json", "ethics_utilitarianism - EM", False),
        ("core_scenarios.json", "MATH (chain-of-thoughts) - Equivalent (chain of thought)", False),
    ],

    # "Robustness": [
    #     ("core_scenarios.json", "MMLU - EM (Robustness)", False),
    #     ("core_scenarios.json", "TruthfulQA - EM (Robustness)", False),
    # ],

    # "Fairness": [
    #     ("core_scenarios.json", "MMLU - EM (Fairness)", False),
    #     ("core_scenarios.json", "TruthfulQA - EM (Fairness)", False),

    # ],

    "Bias": [
        ("core_scenarios.json", "sam_sum - Stereotypes (race)", True),
        ("core_scenarios.json", "sam_sum - Stereotypes (gender)", True),
        ("core_scenarios.json", "sam_sum - Representation (race)", True),
        ("core_scenarios.json", "sam_sum - Representation (gender)", True),
        
        # ("core_scenarios.json", "ethics_justice - Stereotypes (race)", True),
        # ("core_scenarios.json", "ethics_justice - Stereotypes (gender)", True),
        # ("core_scenarios.json", "ethics_justice - Representation (race)", True),
        # ("core_scenarios.json", "ethics_justice - Representation (gender)", True),
    ],

}