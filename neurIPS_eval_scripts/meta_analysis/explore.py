from utils import get_args, load_data
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

plt.ioff()
import os

sns.set(font_scale=1.3, context="paper")

if __name__ == "__main__":
    do_plot_scores_hist = False
    do_compare_mean_rank_and_mean_score = False
    do_compare_full_open_hidden_scores_final = False
    do_compare_full_open_hidden_scores_open_hidden_stages = False
    do_compare_scores_between_stages_score = False
    do_rank_agreement_between_scenarios = True

    analysis_dir = os.path.dirname(os.path.abspath(__file__))

    args = get_args()
    df, agg_df = load_data(args["res_dir"])

    df.dropna(inplace=True)
    agg_df.dropna(inplace=True)

    def plot_scores_hist(df):
        for name, group in df.groupby("comp_round"):
            sns.displot(group, x="score", col="scenario", hue="GPU", col_wrap=4, stat="density")
            plt.savefig(f"{analysis_dir}/figs/scores_dist/{name}.png")

    if do_plot_scores_hist:
        plot_scores_hist(df)

    def compare_mean_rank_and_mean_score(df):
        df["avg_over_scenarios_score"] = df.groupby(["comp_round", "GPU", "model"])["score"].transform("mean")
        df["per_scenario_rank"] = df.groupby(["comp_round", "GPU", "scenario"])["score"].transform(
            "rank", method="min", ascending=False
        )
        df["avg_over_scenarios_rank"] = df.groupby(["comp_round", "GPU", "model"])["per_scenario_rank"].transform(
            "mean"
        )

        sns.relplot(
            df,
            x="avg_over_scenarios_score",
            y="avg_over_scenarios_rank",
            hue="GPU",
            col="comp_round",
            col_order=["open", "hidden", "final"],
            facet_kws={"sharey": False, "sharex": False},
        )

        plt.savefig(f"{analysis_dir}/figs/mean_rank_v_mean_score/fig.png")

    if do_compare_mean_rank_and_mean_score:
        compare_mean_rank_and_mean_score(df)

    def compare_full_open_hidden_scores_final(agg_df):
        score_cols = ["Score_full", "Score_open", "Score_hidden"]
        piv_df = agg_df[agg_df["scenario"].isin(score_cols)].query('comp_round=="final"')

        # Pivot the dataframe to reshape it
        piv_df = piv_df.pivot(index=["model", "GPU", "comp_round"], columns="scenario", values="score")

        g = sns.pairplot(
            piv_df.reset_index(),
            kind="reg",
            diag_kind="kde",
            hue="GPU",
            aspect=1.2,
            diag_kws={"cumulative": True, "bw_adjust": 0.1},
        )
        g.set(ylim=(-0.02, 0.78), xlim=(-0.02, 0.78))
        g.fig.suptitle("Open/Closed/Full eval sets concurrence")
        g.figure.subplots_adjust(top=0.95)

        plt.savefig(f"{analysis_dir}/figs/compare_full_open_hidden_scores/final_stage.png")

    if do_compare_full_open_hidden_scores_final:
        compare_full_open_hidden_scores_final(agg_df)

    def compare_full_open_hidden_scores_open_hidden_stages(agg_df):
        # get models that appear in the second stage
        piv_df = agg_df[agg_df.model.isin(agg_df.query('comp_round=="hidden"').model.unique())]
        piv_df = piv_df[piv_df["scenario"].str.contains("Score")].query('comp_round!="final"')

        # Pivot the dataframe to reshape it
        piv_df.drop_duplicates(subset=["model", "GPU", "comp_round", "scenario"], inplace=True)
        piv_df = piv_df.pivot(index=["model", "GPU"], columns="comp_round", values="score")

        g = sns.pairplot(
            piv_df.reset_index(),
            kind="reg",
            diag_kind="kde",
            hue="GPU",
            aspect=1.2,
            diag_kws={"cumulative": True, "bw_adjust": 0.1},
        )
        g.fig.suptitle("Open vs hidden Eval set concurrence")
        g.figure.subplots_adjust(top=0.9)

        plt.savefig(f"{analysis_dir}/figs/compare_full_open_hidden_scores/open_hidden_stages.png")

    if do_compare_full_open_hidden_scores_open_hidden_stages:
        compare_full_open_hidden_scores_open_hidden_stages(agg_df)

    def compare_scores_between_stages_score(df):
        finalist_models = df.query('comp_round=="final"').model.unique()
        piv_df = df[df.model.isin(finalist_models)]

        piv_df["comp_round"] = piv_df["comp_round"].apply(lambda x: x if x == "final" else "initial")

        piv_df.drop_duplicates(subset=["model", "GPU", "subscenario", "comp_round", "scenario"], inplace=True)
        piv_df = piv_df.pivot(
            index=["model", "GPU", "subscenario", "scenario"], columns="comp_round", values="score"
        ).reset_index()

        g = sns.lmplot(
            piv_df,
            x="initial",
            y="final",
            hue="subscenario",
            col="scenario",
            col_wrap=4,
            facet_kws={"sharey": False, "sharex": False},
            ci=None,
        )

        plt.savefig(f"{analysis_dir}/figs/concurrence_first_two_stages_vs_final/score.png")

        # g = sns.lmplot(
        #     piv_df,
        #     x="initial",
        #     y="final",
        #     hue="GPU",
        #     # col="scenario",
        #     # col_wrap=4,
        #     # facet_kws={"sharey": False, "sharex": False},
        #     ci=None,
        # )

        plt.title("Compare Stages Mean Score")
        plt.xlabel("Open+Hidden Mean Score")
        plt.ylabel("Final Mean Score")
        plt.savefig(f"{analysis_dir}/figs/concurrence_first_two_stages_vs_final/score_average_over_subscenarios.png")

        piv_df["final_rank"] = piv_df.groupby(["subscenario", "GPU"])["final"].rank(ascending=False, method="min")
        piv_df["initial_rank"] = piv_df.groupby(["subscenario", "GPU"])["initial"].rank(ascending=False, method="min")

        g = sns.pointplot(
            piv_df,
            x="initial_rank",
            y="final_rank",
            linestyles=" ",
            hue="GPU",
            # col="scenario",
            # col_wrap=4,
            # facet_kws={"sharey": False, "sharex": False},
            # ci=None,
        )

        plt.xlabel("Open+Hidden Mean Rank")
        plt.ylabel("Final Mean Rank")
        plt.title("Mean Rank Concurrene between Open+Hidden & Final Evaluations")
        plt.savefig(f"{analysis_dir}/figs/concurrence_first_two_stages_vs_final/rank.png")

    if do_compare_scores_between_stages_score:
        compare_scores_between_stages_score(df)

    def rank_agreement_between_scenarios(agg_df):
        mwr_df = agg_df[agg_df["subscenario"].str.contains("Mean Win Rate")]
        mwr_df = mwr_df[mwr_df["comp_round"] == "final"]
        mwr_df = mwr_df[mwr_df["GPU"] == "A100"]

        mwr_df["mean_mwr"] = mwr_df.groupby(["model", "GPU"])["score"].transform("mean")
        mwr_df.sort_values("mean_mwr", ascending=False, inplace=True)

        mwr_df["rank"] = mwr_df.groupby(["scenario", "GPU"])["score"].transform("rank", method="min", ascending=False)

        mwr_df["model_short"] = mwr_df["model"].apply(lambda x: x.split("_")[0])

        ax = sns.pointplot(
            mwr_df,
            x="scenario",
            y="rank",
            hue="model_short",
        )

        sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))

        plt.gca().invert_yaxis()
        plt.xlabel("Scanario")
        plt.ylabel("Rank (based on mean-mean win rate)")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f"{analysis_dir}/figs/ranks_with_wmr/fig.png")

    if do_rank_agreement_between_scenarios:
        rank_agreement_between_scenarios(agg_df)
