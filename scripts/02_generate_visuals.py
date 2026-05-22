import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

def generate_visuals(data_path, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    df = pd.read_parquet(data_path)
    
    # Set up dark modern style
    plt.style.use("dark_background")
    sns.set_theme(style="darkgrid", rc={"axes.facecolor": "#121212", "figure.facecolor": "#121212", "text.color": "white", "axes.labelcolor": "white", "xtick.color": "white", "ytick.color": "white"})
    
    # 1. Toss Impact
    match_df = df.drop_duplicates(subset=["match_id"])
    venue_counts = match_df["venue"].value_counts()
    valid_venues = venue_counts[venue_counts >= 20].index
    
    venue_impact = match_df[match_df["venue"].isin(valid_venues)].copy()
    toss_win_pct = venue_impact.groupby("venue")["toss_win_match_win"].mean().sort_values() * 100
    
    plt.figure(figsize=(10, 8))
    toss_win_pct.plot(kind="barh", color="#1DB954")
    plt.axvline(x=50, color='red', linestyle='--', alpha=0.7)
    plt.title("Impact of Winning Toss on Match Win % by Venue (Min 20 Matches)", fontsize=14, pad=15)
    plt.xlabel("Match Win % when Winning Toss")
    plt.ylabel("Venue")
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "toss_impact_by_venue.png"), dpi=300)
    plt.close()

    # 2. Phase Impact
    # For Phase impact, group by match, team, phase and calculate runs.
    phase_runs = df.groupby(["match_id", "team", "match_phase"])["runs_total"].sum().reset_index()
    phase_runs = phase_runs.merge(match_df[["match_id", "winner", "margin_runs"]], on="match_id", how="left")
    runs_won_df = phase_runs[(phase_runs["winner"] == phase_runs["team"]) & (phase_runs["margin_runs"] > 0)]
    
    plt.figure(figsize=(12, 6))
    sns.lmplot(data=runs_won_df, x="runs_total", y="margin_runs", hue="match_phase", col="match_phase", scatter_kws={'alpha':0.5})
    plt.suptitle("Impact of Runs Scored in Phases on Victory Margin (Runs)", y=1.05)
    plt.savefig(os.path.join(out_dir, "phase_impact_margin.png"), dpi=300)
    plt.close()

    # 3. Top Batters Scatter Plot
    df["is_out"] = df["player_out"] == df["batter"]
    outs_series = df.groupby("batter")["is_out"].sum()
    
    batter_stats = df.groupby("batter").agg(
        runs=("runs_batter", "sum"),
        balls_faced=("is_legal_ball_faced", "sum")
    ).reset_index()
    batter_stats["outs"] = batter_stats["batter"].map(outs_series)
    
    batter_stats = batter_stats[batter_stats["runs"] >= 500].copy()
    batter_stats["average"] = np.where(batter_stats["outs"] > 0, batter_stats["runs"] / batter_stats["outs"], batter_stats["runs"])
    batter_stats["strike_rate"] = (batter_stats["runs"] / batter_stats["balls_faced"]) * 100
    
    plt.figure(figsize=(10, 8))
    sns.scatterplot(data=batter_stats, x="average", y="strike_rate", size="runs", sizes=(20, 400), alpha=0.7, color="#E1306C")
    plt.title("Top Batters: Strike Rate vs Average (Min 500 runs)", fontsize=14, pad=15)
    plt.xlabel("Batting Average")
    plt.ylabel("Strike Rate")
    
    # Annotate top 5 by runs
    top_5 = batter_stats.nlargest(5, "runs")
    for _, row in top_5.iterrows():
        plt.text(row["average"], row["strike_rate"], row["batter"], fontsize=9, color="white")
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "top_batters.png"), dpi=300)
    plt.close()

    # 4. Top Bowlers Scatter Plot
    bowler_stats = df.groupby("bowler").agg(
        balls_bowled=("is_wide", lambda x: (~x).sum()),
        runs_conceded=("runs_total", "sum"),
        wickets=("wicket_type", lambda x: x.isin(['bowled', 'caught', 'lbw', 'stumped', 'caught and bowled', 'hit wicket']).sum())
    ).reset_index()
    
    bowler_stats["overs"] = bowler_stats["balls_bowled"] / 6
    bowler_stats = bowler_stats[bowler_stats["overs"] >= 50].copy()
    bowler_stats["economy"] = bowler_stats["runs_conceded"] / bowler_stats["overs"]
    bowler_stats["bowling_sr"] = np.where(bowler_stats["wickets"] > 0, bowler_stats["balls_bowled"] / bowler_stats["wickets"], 0)
    bowler_stats = bowler_stats[bowler_stats["wickets"] > 0]
    
    plt.figure(figsize=(10, 8))
    sns.scatterplot(data=bowler_stats, x="economy", y="bowling_sr", size="wickets", sizes=(20, 400), alpha=0.7, color="#1DA1F2")
    plt.title("Top Bowlers: Economy vs Strike Rate (Min 50 overs)", fontsize=14, pad=15)
    plt.xlabel("Economy Rate (Runs per Over)")
    plt.ylabel("Strike Rate (Balls per Wicket)")
    
    top_5_b = bowler_stats.nlargest(5, "wickets")
    for _, row in top_5_b.iterrows():
        plt.text(row["economy"], row["bowling_sr"], row["bowler"], fontsize=9, color="white")
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "top_bowlers.png"), dpi=300)
    plt.close()
    
    print("Visuals generated successfully!")

if __name__ == "__main__":
    generate_visuals(r"e:\ipl crunch\ipl_master_26.parquet", r"e:\ipl crunch\output_visuals")
