import json 
import argparse


OPEN_WEIGHT = 1/3
HIDDEN_WEIGHT = 2/3

#combines open and hidden results based on the specified weights, then rank the submissions based on combined score
if __name__ == "__main__":


    parser = argparse.ArgumentParser(description="combin open close eval results")
    parser.add_argument("--path", type=str, help='ranked submissions json path', required=True)
    parser.add_argument('--track', type=str, default='A100', required=False)

    args = parser.parse_args()

    open_rank = json.load(
        open(f"{args.path}/{args.track}_open_rank.json", 'r' ))
    open_rank = {x[0]:x[1] for x in open_rank}
    
    close_rank = json.load(
        open(f"{args.path}/{args.track}_hidden_rank.json", 'r' ))
    close_rank = {x[0]: x[1] for x in close_rank}

    print(f'open_size:{len(open_rank)}, close_size:{len(close_rank)}')

    full_rank = []
    for idx, open_res in open_rank.items():
        close_res =  close_rank[f'{idx}_hidden']
        score_open = open_res["Score"]
        score_close = close_res['Score']
        weighted_score = OPEN_WEIGHT * score_open + HIDDEN_WEIGHT*score_close
        res = open_res
        res = {**open_res, **close_res}
        del res["Score"]
        res['Score_full'] = weighted_score
        res['Score_open'] = open_res['Score']
        res['Score_hidden'] = close_res['Score']

        full_rank.append((idx, res))
    
    full_rank = sorted(full_rank, key=lambda x : x[1]['Score_full'], reverse=True)
    
    with open(f'{args.track}_full_ranks.json', 'w') as handle:
        json.dump(full_rank, handle, indent=4)
