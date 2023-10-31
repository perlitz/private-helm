import os 
import json
import math
import statistics
from eval_metrics import Open_eval_metrics as METRICS
import argparse

def load_run_results(run_result_dir:str):
 
    results = {}

    for filename in os.listdir(run_result_dir):
        filepath = os.path.join(run_result_dir, filename)
        with open(filepath, 'r') as handle:
            res = json.load(handle)
            idx, _ = os.path.splitext(filename)
            results[idx] = res
    return results


#take from https://github.com/Lightning-AI/llm-efficiency-challenge-eval/blob/main/agents/helm_postprocessing.py
def rank_results(data:dict, metrics_config:dict):
    # mean win rate to be computed here

    # data layout
    # {"<submission_id>": {"<scenario>": {"metric1": value, ...}}}

    # so we compute the mean win rate per scenario and the geometric
    # mean across scenarios per submission_id

    if not data:
        return []

    lower_is_better_map = {}
    for scenario, scenario_metrics in metrics_config.items():
        lower_is_better_map[scenario] = {}
        for _, metric, lower_is_better in scenario_metrics:
            lower_is_better_map[scenario][metric] = lower_is_better

    submission_ids = list(data.keys())
    scenarios = list(metrics_config.keys())

    mean_win_rates = {submission_id: {} for submission_id in submission_ids}

    for scenario in scenarios:
        win_rates_per_row = [[] for _ in submission_ids]
        metrics = [metric for _, metric, _ in metrics_config[scenario]]
        for metric in metrics:
            lower_is_better = lower_is_better_map[scenario][metric]
            default_value = 0.0 if not lower_is_better else 1000.0
            values = [(data[submission_id].get(scenario, {metric: default_value}).get(metric, 0.0), j) for j, submission_id in enumerate(submission_ids)]
            # temporary fix for populating lower is better entries with 0.0's;
            # this has been fixed in agents.py, but it's needed for older submissions;
            # we can remove once we move to flash helm
            if lower_is_better:
                values = [(default_value, j) if val == 0.0 else (val, j) for val, j in values]
            for wins, (v, j) in enumerate(sorted(values, reverse=lower_is_better)):
                win_rate = wins / (len(values) - 1) if len(values) > 1 else 1.0  # normalize to [0, 1]
                win_rates_per_row[j].append(win_rate)

        for submission_id, win_rates in zip(submission_ids, win_rates_per_row):
            if not win_rates:
                continue
            mean_win_rates[submission_id][scenario] = statistics.mean(win_rates)

    # mean_win_rates layout
    # {"<submission_id>": {"<scenario>": value}}

    eps = math.nextafter(0.0, math.inf)

    scores = {}
    for submission_id in submission_ids:
        values = list(mean_win_rates[submission_id].values())
        values = [el if el > 0.0 else eps for el in values]
        score = statistics.geometric_mean(values) if values else 0.0
        scores[submission_id] = score

    table = []
    score_key = "Score"

    for submission_id, scenarios in data.items():
        row = {}
        for scenario, metrics in metrics_config.items():
            for _, metric, _ in metrics:
                lower_is_better = lower_is_better_map[scenario][metric]
                value = None
                if scenario in data[submission_id] and metric in data[submission_id][scenario]:
                    value = data[submission_id][scenario][metric]
                # temporary fix for populating lower is better entries with 0.0's;
                # this has been fixed in agents.py, but it's needed for older submissions;
                # we can remove once we move to flash helm
                if lower_is_better and value == 0.0:
                    value = None
                row[metric] = value
            row[f"{scenario} Mean Win Rate"] = mean_win_rates[submission_id][scenario]
        row[score_key] = scores[submission_id]
        table.append([submission_id, row])

    table = list(sorted(table, key=lambda x: x[1][score_key], reverse=True))
    #[(submission_id, {metric:score})]
    return table 



if __name__ == "__main__":

    try:
        parser = argparse.ArgumentParser(description="rank helm evaluation results")
        parser.add_argument("--dir", type=str, help='helm evaluation dir for al submissions', required=True)
        parser.add_argument('--name', type=str, help='evaluation_name', default='open')

        args = parser.parse_args()
        submission_results =load_run_results(args.dir)
        ranked_results = rank_results(submission_results, METRICS)

        with open (f"{args.name}_full_rank.json", 'w') as handle:
            json.dump( ranked_results, handle)

    except Exception as e :
        print(e)
