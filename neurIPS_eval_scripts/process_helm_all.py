import json 
import os 
import sys
import argparse
from eval_metrics import Open_eval_metrics as open_metrics 
from eval_metrics import Hidden_eval_metrics  as hidden_metrics

'''
parse results from helm-summerize under helm_output_dir/runs/submission_id
--dir benchmark_dir
--idx submission_idx
'''

#this is taken from https://github.com/Lightning-AI/llm-efficiency-challenge-eval/blob/main/agents/agents.py#L182
def process_helm_results(root_path:str, suite: str, METRICS:dict = open_metrics) -> dict:
    path = f"{root_path}/{suite}/groups/"
    output = {}

    for scenario, scenario_metrics in METRICS.items():
        scenario_output = {}
        prev_filename = None
        for filename, metric, _ in scenario_metrics:
            print(filename, metric)
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
        parser.add_argument("--path", type=str, help='Helm Benchmark dir', required=True)
        parser.add_argument('--hidden', action='store_true', help="hidden eval metrics", required=False)
        args = parser.parse_args()
        
        use_metrics = open_metrics
        if args.hidden:
            use_metrics = hidden_metrics


        path = args.path
        for idx in os.listdir(path):
            try:
                print(f'processing {idx}')
                run_results = process_helm_results(path, idx, METRICS=use_metrics)
                print(run_results)

                results_dir = f"./submission_results"
                os.makedirs(results_dir, exist_ok=True)

                out_name = f"{idx}.json" 
                if args.hidden:
                    out_name = f"{idx}_hidden.json"

                result_json = os.path.join(results_dir, out_name)

                with open (result_json, 'w') as handle:
                    json.dump( run_results, handle, indent=4)

                print(f'write file {out_name}')
            except Exception as e:
                print(e)
                

    except Exception as e :
        print(e)
        print("--help for usage")
        sys.exit(2)
