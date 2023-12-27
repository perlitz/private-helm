import pandas as pd
import os
import argparse


def load_data(res_dir):
    assert os.path.exists(
        res_dir
    ), f"Please dump your .json results file in {res_dir} or define a different one in --res_dir"

    process_res_dfs = []
    for res_file in os.listdir(res_dir):
        cur_res_df = pd.read_json(os.path.join(res_dir, res_file)).reset_index()

        models = cur_res_df.rename(columns={0: "model"})["model"]
        res_dicts = pd.json_normalize(cur_res_df[1])

        process_cur_df = pd.concat([models, res_dicts], axis=1)
        process_cur_df["source_file"] = res_file.replace(".json", "")

        process_res_dfs.append(process_cur_df)

    res_df = pd.concat(process_res_dfs, axis=0)
    res_df = res_df.sort_values("source_file")

    identifiers = ["model", "source_file"]

    res_df = pd.melt(
        frame=res_df,
        id_vars=identifiers,
        value_vars=[col_name for col_name in res_df.columns.tolist() if col_name not in identifiers],
        var_name="scenario",
        value_name="score",
    )

    res_df["GPU"] = res_df["source_file"].apply(lambda x: x.split("_")[0])
    res_df["comp_round"] = res_df["source_file"].apply(lambda x: x.split("_")[1].replace("full", "final"))
    res_df.drop(columns=["source_file"], inplace=True)

    res_df["subscenario"] = res_df["scenario"]

    res_df["scenario"] = res_df["subscenario"].apply(lambda x: x.split(" ")[0])

    # seperate results to aggragated and scores
    agg_df = res_df[res_df["subscenario"].str.contains("Score") | res_df["subscenario"].str.contains("Mean Win Rate")]
    reg_df = res_df[
        ~(res_df["subscenario"].str.contains("Score") | res_df["subscenario"].str.contains("Mean Win Rate"))
    ]

    def fix_model_names(x):
        return (
            x.replace("_hidden", "")
            .replace("_lit_gpt", "")
            .replace("_reproduce_eval", "")
            .replace("datta0_neurips_submission_1", "datta0_neurips_submission")
            .replace("tvergho_lm_neurips_train", "tvergho_llm_neurips_train")
            .replace(
                "mrigankramanllm_compa100_submissionsa100_1st_submission",
                "mrigankraman_llm_comp_a100_submissions_a100_1st_submission",
            )
        )

    agg_df["model"] = agg_df["model"].apply(fix_model_names)
    reg_df["model"] = reg_df["model"].apply(fix_model_names)

    assert (
        len(
            [
                m
                for m in agg_df.query('comp_round=="final"').model.unique()
                if m not in agg_df.query('comp_round=="open"').model.unique()
            ]
        )
        == 0
    ), "Some models in final are not in open"
    assert (
        len(
            [
                m
                for m in agg_df.query('comp_round=="final"').model.unique()
                if m not in agg_df.query('comp_round=="hidden"').model.unique()
            ]
        )
        == 0
    ), "Some models in final are not in hidden"

    return reg_df, agg_df


def get_args():
    parser = argparse.ArgumentParser(description="Load and process challenge results")
    parser.add_argument(
        "--res_dir", help="dir with .json model results", default="neurIPS_eval_scripts/meta_analysis/results"
    )
    args = vars(parser.parse_args())

    return args


if __name__ == "__main__":
    args = get_args()
    df = load_data(args["res_dir"])
