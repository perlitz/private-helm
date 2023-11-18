import json
from collections import defaultdict
import argparse


def hide_name (ranked):
    metrics = defaultdict(list)
    for item in ranked:
        for k, v in item[1].items():
            metrics[k].append(v)

    names= list(metrics.keys())     
    names = [x.split(' ')[0].strip() for x in names]
    name_dic = {x: f"dataset_{i}" for i, x in enumerate(set(names)) if x!="Score"}

    clean_ranked = []

    for (k, v) in ranked:
        nn = {}
        for kk, vv in v.items():
            t = kk.split(' ')
            a = t[0]
            p = t[1:]
            new_k = ' '.join([name_dic.get(a, 'Score')] + p)
            nn[new_k] = vv
        clean_ranked.append((k, nn))
    return clean_ranked

if __name__ == "__main__":

    try:
        parser = argparse.ArgumentParser(description="hide dataset name")
        parser.add_argument("--file", type=str, help='ranked submission file', required=True)
        parser.add_argument("--outfile", type=str, help="output file name", required=True)
        args = parser.parse_args()
        with open (args.file, 'r') as handle:
            ranked = json.load(handle)
        clean_ranked = hide_name(ranked=ranked)

        with open(args.outfile,'w') as handle:
            json.dump(clean_ranked, handle, indent=4)
    except Exception as e:
        print(e)