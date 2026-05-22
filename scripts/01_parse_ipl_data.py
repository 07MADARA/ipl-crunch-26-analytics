import json
import pandas as pd
from pathlib import Path

def parse_all_json(folder_path):
    folder = Path(folder_path)
    all_rows = []
    
    for file_path in folder.glob("*.json"):
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        info = data.get("info", {})
        
        # Metadata
        match_id = file_path.stem
        season = info.get("season", None)
        city = info.get("city", None)
        venue = info.get("venue", None)
        
        toss = info.get("toss", {})
        toss_winner = toss.get("winner", None)
        toss_decision = toss.get("decision", None)
        
        outcome = info.get("outcome", {})
        winner = outcome.get("winner", None)
        
        try:
            margin_runs = outcome.get("by", {}).get("runs", 0)
        except AttributeError:
            margin_runs = 0
            
        try:
            margin_wickets = outcome.get("by", {}).get("wickets", 0)
        except AttributeError:
            margin_wickets = 0
        
        player_of_match = info.get("player_of_match", [])
        pom = player_of_match[0] if player_of_match else None
        
        toss_win_match_win = (toss_winner == winner) if (toss_winner and winner) else False
        
        innings = data.get("innings", [])
        
        for inn_idx, inn in enumerate(innings):
            team = inn.get("team", None)
            overs = inn.get("overs", [])
            for ov in overs:
                over_num = ov.get("over", 0)
                
                # match_phase
                if 0 <= over_num <= 5:
                    match_phase = "Powerplay"
                elif 6 <= over_num <= 14:
                    match_phase = "Middle"
                elif 15 <= over_num <= 19:
                    match_phase = "Death"
                else:
                    match_phase = "Other"
                    
                deliveries = ov.get("deliveries", [])
                for ball_idx, ball in enumerate(deliveries):
                    batter = ball.get("batter")
                    bowler = ball.get("bowler")
                    non_striker = ball.get("non_striker")
                    
                    runs = ball.get("runs", {})
                    runs_batter = runs.get("batter", 0)
                    runs_extras = runs.get("extras", 0)
                    runs_total = runs.get("total", 0)
                    
                    extras = ball.get("extras", {})
                    is_wide = "wides" in extras
                    
                    wickets = ball.get("wickets", [])
                    wicket_type = wickets[0].get("kind") if wickets else None
                    player_out = wickets[0].get("player_out") if wickets else None
                    
                    # Determine dot ball for the streak
                    is_legal_ball_faced = not is_wide
                    is_dot_ball = is_legal_ball_faced and (runs_batter == 0)
                    
                    row = {
                        "match_id": match_id,
                        "season": season,
                        "city": city,
                        "venue": venue,
                        "toss_winner": toss_winner,
                        "toss_decision": toss_decision,
                        "winner": winner,
                        "margin_runs": margin_runs,
                        "margin_wickets": margin_wickets,
                        "player_of_match": pom,
                        "toss_win_match_win": toss_win_match_win,
                        
                        "innings": inn_idx + 1,
                        "team": team,
                        "over": over_num,
                        "ball": ball_idx + 1,
                        "match_phase": match_phase,
                        
                        "batter": batter,
                        "bowler": bowler,
                        "non_striker": non_striker,
                        "runs_batter": runs_batter,
                        "runs_extras": runs_extras,
                        "runs_total": runs_total,
                        
                        "is_wide": is_wide,
                        "is_dot_ball": is_dot_ball,
                        "is_legal_ball_faced": is_legal_ball_faced,
                        
                        "wicket_type": wicket_type,
                        "player_out": player_out
                    }
                    all_rows.append(row)
                    
    df = pd.DataFrame(all_rows)
    return df

def calculate_dot_ball_pressure(df):
    print("Calculating dot ball pressure...")
    df = df.sort_values(by=["match_id", "innings", "over", "ball"])
    
    # We create a column for pressure:
    df['dot_ball_pressure'] = 0
    
    # Calculate streaks
    df['reset_flag'] = (~df['is_dot_ball']).astype(int)
    df['streak_group'] = df.groupby(["match_id", "innings", "batter"])['reset_flag'].cumsum()
    df['dot_ball_pressure'] = df.groupby(["match_id", "innings", "batter", "streak_group"])['is_dot_ball'].cumsum()
    
    df = df.drop(columns=['reset_flag', 'streak_group'])
    return df

if __name__ == "__main__":
    folder_path = r"e:\ipl crunch\raw json"
    print(f"Parsing files in {folder_path}...")
    df = parse_all_json(folder_path)
    print(f"Initial DataFrame shape: {df.shape}")
    
    df = calculate_dot_ball_pressure(df)
    
    out_path = r"e:\ipl crunch\ipl_master_26.parquet"
    print(f"Saving to {out_path}...")
    df["toss_win_match_win"] = df["toss_win_match_win"].astype(bool)
    
    # Handle mixed types for pyarrow
    for col in ["season", "city", "venue", "toss_winner", "toss_decision", "winner", "player_of_match", "team", "batter", "bowler", "non_striker", "wicket_type", "player_out"]:
        df[col] = df[col].astype(str)
    
    # Save as parquet
    df.to_parquet(out_path)
    print("Done!")
