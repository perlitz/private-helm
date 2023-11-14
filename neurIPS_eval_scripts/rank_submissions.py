import os 
import json
import math
import statistics
from eval_metrics import *
import argparse
from collections import defaultdict, Counter 

def load_run_results(run_result_dir:str):
 
    results = {}

    for filename in os.listdir(run_result_dir):
        filepath = os.path.join(run_result_dir, filename)
        with open(filepath, 'r') as handle:
            res = json.load(handle)
            idx, _ = os.path.splitext(filename)
            results[idx] = res
    return results



def transpose_results(results):
    data_sets = ['CNN/DailyMail', "sam_sum", "corr2cause", 'ethics', 'MATH']
    transposed_results = {}
    for name, res in results.items():
        t_res = defaultdict(dict)
        for val in res.values():
            for d in data_sets:
                for k,v in val.items():
                    if d in k:
                        t_res[d][k] = v 
                        continue 
        transposed_results[name]= t_res 
    return transposed_results


def calc_win_rate(values, lower_is_better=False):
    #This function calculate win rate, allow entries in values to repeat, such as [1, 1, 1, 3, 4, 5, 1]
    # in this case, the repeated values will get the same win-rate, which is 1/(n_repeats) + count(lower_rank)
    counts = Counter( values)
    win_rate ={idx: 0.0 for idx in range( len(values) )}

    for i, v in enumerate(values):
        for j, vv in enumerate(values):
            if i == j:
                continue
            if not lower_is_better and  v > vv:
                win_rate[i] += 1
            elif lower_is_better and v < vv:
                win_rate[i] += 1
            elif v == vv:
                win_rate[i] += 1.0/counts[v]
    
    win_rate = [(k, v/len(values)) for k, v in win_rate.items()]
    win_rate = [x[1] for x in sorted(win_rate, key=lambda k : k[0] )]
    return win_rate

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
            
            vv = [x[0] for x in values]
            win_rates = calc_win_rate(vv, lower_is_better=lower_is_better)
            for (win, (_, j)) in zip (win_rates, values):
                win_rates_per_row[j].append(win)
    
            

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
        parser.add_argument('--hidden', action='store_true', help="hidden eval metrics", required=False)
        parser.add_argument('--track', type=str, default='A100', required=False)
        parser.add_argument('--acc_only', action='store_true', help="only use accuracy metrics", required=False)

        args = parser.parse_args()
        submission_results =load_run_results(args.dir)
        METRICS = Open_eval_metrics
        
        name = 'open'
        if args.hidden:
            name = 'hidden'

            if args.acc_only:
                METRICS = Hidden_acc_only_metrics
                name = f'{name}_accuracy_only'
            else:
                METRICS = Hidden_dataset_centric_eval_metrics
                submission_results = transpose_results(submission_results)

                # METRICS = Hidden_eval_metrics
                # # submission_results = transpose_results(submission_results)

        name = f"{args.track}_{name}"

        ranked_results = rank_results(submission_results, METRICS)
        with open (f"{name}_full_rank.json", 'w') as handle:
            json.dump( ranked_results, handle, indent=4)

    except Exception as e :
        print(e)
