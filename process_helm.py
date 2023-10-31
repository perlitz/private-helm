import json 
import os 
import sys
import argparse

'''
parse results from helm-summerize under helm_output_dir/runs/submission_id
--dir benchmark_dir
--idx submission_idx
'''

#these are the metrics we use for evalu
# adapted from https://github.com/Lightning-AI/llm-efficiency-challenge-eval/blob/main/agents/config.py
METRICS = {
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

#this is taken from https://github.com/Lightning-AI/llm-efficiency-challenge-eval/blob/main/agents/agents.py#L182
def process_helm_results(root_path:str, suite: str) -> dict:
    path = f"{root_path}/{suite}/groups/"
    output = {}

    for scenario, scenario_metrics in METRICS.items():
        scenario_output = {}
        prev_filename = None
        for filename, metric, _ in scenario_metrics:
            if filename != prev_filename:
                with open(os.path.join(path, filename), "r") as f:
                    data = json.load(f)
                prev_filename = filename
            scenario_data = [el for el in data if el["title"] == scenario][0]
            metric_idx = None
            for i, header in enumerate(scenario_data["header"]):
                if header["value"] == metric:
                    metric_idx = i
                    break
            value = scenario_data["rows"][0][metric_idx].get("value")
            if value is not None:
                scenario_output[metric] = value
            else:
                print(f'{metric} is None ')
        output[scenario] = scenario_output

    return output


if __name__ == "__main__":

    try:
        parser = argparse.ArgumentParser(description="Parse helm-summerize results")
        parser.add_argument("--dir", type=str, help='Helm Benchmark dir', required=True)
        parser.add_argument('--idx', type=str, help='submission id', required=True)
        args = parser.parse_args()
        run_results = process_helm_results(args.dir, args.idx)
        with open (f'{args.idx}.json', 'w') as handle:
            json.dump( run_results, handle)

    except Exception as e :
        print(e)
        print("--help for usage")
        sys.exit(2)
