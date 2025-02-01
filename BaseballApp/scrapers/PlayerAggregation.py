import requests
import time
import json
from bs4 import BeautifulSoup
from bs4 import Comment
import pandas as pd
import logging

from utils.utils import replace_text

# Create and configure logger
logging.basicConfig(filename="./logs/playerAnalysis.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')

# Creating an object
logger = logging.getLogger()

# Setting the threshold of logger to DEBUG
logger.setLevel(logging.DEBUG)

key_data_types = {
    # General Player Info
    "age": int,
    "team_name_abbr": str,
    "comp_name_abbr": str,
    "pos": str,
    "awards": str, 
    "salary_info": float,
    
    # Pitching Stats
    "p_war": float,
    "p_w": int,
    "p_l": int,
    "p_win_loss_perc": float,
    "p_earned_run_avg": float,
    "p_g": int,
    "p_gs": int,
    "p_gf": int,
    "p_cg": int,
    "p_sho": int,
    "p_sv": int,
    "p_ip": float,
    "p_h": float,
    "p_r": float,
    "p_er": float,
    "p_hr": int,
    "p_bb": int,
    "p_ibb": int,
    "p_so": int,
    "p_hbp": int,
    "p_bk": int,
    "p_wp": int,
    "p_bfp": int,
    "p_earned_run_avg_plus": int,
    "p_fip": float,
    "p_whip": float,
    "p_hits_per_nine": float,
    "p_hr_per_nine": float,
    "p_bb_per_nine": float,
    "p_so_per_nine": float,
    "p_strikeouts_per_base_on_balls": float,
    "p_g_per_dollar": float,
    "p_war_per_dollar": float,
    "p_w_per_dollar": float,
    "p_ip_per_dollar": float,
    "p_so_per_dollar": float,
    "p_so_per_nine_per_dollar": float,
    "p_earned_run_avg_plus_per_dollar": float,
    
    # Batting Stats
    "b_war": float,
    "b_games": int,
    "b_pa": int,
    "b_ab": int,
    "b_r": int,
    "b_h": int,
    "b_doubles": int,
    "b_triples": int,
    "b_hr": int,
    "b_rbi": int,
    "b_sb": int,
    "b_cs": int,
    "b_bb": int,
    "b_so": int,
    "b_batting_avg": float,
    "b_onbase_perc": float,
    "b_slugging_perc": float,
    "b_onbase_plus_slugging": float,
    "b_onbase_plus_slugging_plus": int,
    "b_roba": float,
    "b_rbat_plus": int,
    "b_tb": int,
    "b_gidp": int,
    "b_hbp": int,
    "b_sh": int,
    "b_sf": int,
    "b_ibb": int,
    "b_war_per_dollar": float,
    "b_h_per_dollar": float,
    "b_hr_per_dollar": float,
    "b_doubles_per_dollar": float,
    "b_triples_per_dollar": float,
    "b_sb_per_dollar": float,
    "b_bb_per_dollar": float,
    "b_tb_per_dollar": float,
    "b_games_per_dollar": float,
    "ops_plus_per_dollar": float,
}


batting_stat_names = [
    "b_war",
    "b_games",
    "b_pa",
    "b_ab",
    "b_r",
    "b_h",
    "b_doubles",
    "b_triples",
    "b_hr",
    "b_rbi",
    "b_sb",
    "b_cs",
    "b_bb",
    "b_so",
    "b_batting_avg",
    "b_onbase_perc",
    "b_slugging_perc",
    "b_onbase_plus_slugging",
    "b_onbase_plus_slugging_plus",
    "b_roba",
    "b_rbat_plus",
    "b_tb",
    "b_gidp",
    "b_hbp",
    "b_sh",
    "b_sf",
    "b_ibb",
    "b_war_per_dollar",
    "b_h_per_dollar",
    "b_hr_per_dollar",
    "b_doubles_per_dollar",
    "b_triples_per_dollar",
    "b_sb_per_dollar",
    "b_bb_per_dollar",
    "b_tb_per_dollar",
    "b_games_per_dollar",
    "ops_plus_per_dollar",
]

pitching_stat_names = [
    "p_war",
    "p_w",
    "p_l",
    "p_win_loss_perc",
    "p_earned_run_avg",
    "p_g",
    "p_gs",
    "p_gf",
    "p_cg",
    "p_sho",
    "p_sv",
    "p_ip",
    "p_h",
    "p_r",
    "p_er",
    "p_hr",
    "p_bb",
    "p_ibb",
    "p_so",
    "p_hbp",
    "p_bk",
    "p_wp",
    "p_bfp",
    "p_earned_run_avg_plus",
    "p_fip",
    "p_whip",
    "p_hits_per_nine",
    "p_hr_per_nine",
    "p_bb_per_nine",
    "p_so_per_nine",
    "p_strikeouts_per_base_on_balls",
    "p_g_per_dollar",
    "p_war_per_dollar",
    "p_w_per_dollar",
    "p_ip_per_dollar",
    "p_so_per_dollar",
    "p_so_per_nine_per_dollar",
    "p_earned_run_avg_plus_per_dollar",
]

batter_desired_low_stats = [
    "b_gidp",
    "b_cs",
    "b_so"
]
pitcher_desired_low_stats = [
    "p_earned_run_avg",
    "p_er",
    "p_hr",
    "p_hbp",
    "p_bb",
    "p_ibb",
    "p_bk",
    "p_fip",
    "p_whip",
    "p_hits_per_nine",
    "p_hr_per_nine",
    "p_bb_per_nine"
]


BATTER_FILTER_SIZE = 100 # Only accept hitters over this many at bats into the aggregate
PITCHER_FILTER_SIZE = 25 # Only accept pitchers of this many innings into the aggregate

def main():
    with open("./static_data/basic_player_data.json", 'r') as file:
        player_stats = json.load(file)

        # Step 1: Flatten the nested dictionary
        pitcher_rows = []
        batter_rows = []
        for player, years in player_stats.items():
            position = list(years.items())[-1][1]
            for year, stats in list(years.items())[:-1]:
                row = {'player': replace_text(player), 'year': year, 'position': position} # Filter out unwanted characters at this point
                for key, value in stats.items():
                    # Get the target data type
                    target_type = key_data_types.get(key, str)  # Default to string if type not found
                    # Convert value to the target type   
                    try:
                        row[key] = target_type(value) if value not in [None, "null"] else None
                    except ValueError:
                        logger.warning(f"Error converting key '{key}' with value '{value}' to {target_type}")
                    
                # row.update({key: float(value) if value.replace('.', '', 1).isdigit() else value for key, value in stats.items()})
                if (position == "pitching"):
                    pitcher_rows.append(row)
                elif (position == "batting"):
                    batter_rows.append(row)

        # Convert to DataFrame
        pitcher_df = pd.DataFrame(pitcher_rows)
        batter_df = pd.DataFrame(batter_rows)

        # Step 2: Select numeric columns
        numeric_cols = batter_df.select_dtypes(include=['float', 'int']).columns
        aggregate_batter_df = batter_df[batter_df["b_ab"] > 100].groupby(['year'])[numeric_cols].agg(['mean', 'std']).reset_index()

        numeric_cols = pitcher_df.select_dtypes(include=['float', 'int']).columns
        aggregate_pitcher_df = pitcher_df[pitcher_df["p_ip"] > 20].groupby(['year'])[numeric_cols].agg(['mean', 'std']).reset_index()

        # Flatten the hierarchical columns
        aggregate_batter_df.columns = ["_".join(filter(None, col)) for col in aggregate_batter_df.columns]
        aggregate_pitcher_df.columns = ["_".join(filter(None, col)) for col in aggregate_pitcher_df.columns]

        aggregate_batter_df.set_index("year", inplace=True)
        aggregate_pitcher_df.set_index("year", inplace=True)


        aggregate_batter_json = aggregate_batter_df.to_json(orient="index", indent=4)
        aggregate_pitcher_json = aggregate_pitcher_df.to_json(orient="index", indent=4)

        with open("./static_data/batter_analysis.json", "w") as file:
            file.write(aggregate_batter_json)

        with open("./static_data/pitcher_analysis.json", "w") as file:
            file.write(aggregate_pitcher_json)

        batter_df = batter_df.merge(aggregate_batter_df, on="year")
        pitcher_df = pitcher_df.merge(aggregate_pitcher_df, on="year")

        for batting_stat in batting_stat_names:
            if batting_stat in batter_desired_low_stats:
                batter_df[f"{batting_stat}_score"] = (batter_df[f"{batting_stat}_mean"] - batter_df[batting_stat]) / batter_df[f"{batting_stat}_std"] # Sign should be flipped
            else:
                batter_df[f"{batting_stat}_score"] = (batter_df[batting_stat] - batter_df[f"{batting_stat}_mean"]) / batter_df[f"{batting_stat}_std"] # Calculates z-score for player for each metric

        for pitching_stat in pitching_stat_names:
            if pitching_stat in pitcher_desired_low_stats:
                pitcher_df[f"{pitching_stat}_score"] = (pitcher_df[f"{pitching_stat}_mean"] - pitcher_df[pitching_stat]) / pitcher_df[f"{pitching_stat}_std"] # Sign flipped if desired score is low
            else:
                pitcher_df[f"{pitching_stat}_score"] = (pitcher_df[pitching_stat] - pitcher_df[f"{pitching_stat}_mean"]) / pitcher_df[f"{pitching_stat}_std"]
        
        batter_df = batter_df.fillna(0.0)
        pitcher_df = pitcher_df.fillna(0.0)

        batter_df = batter_df.drop(
            columns=[col for col in batter_df.columns if "_mean" in col or "_std" in col]
        )
              
        pitcher_df = pitcher_df.drop(
            columns=[col for col in pitcher_df.columns if "_mean" in col or "_std" in col]
        )

        all_players = { player: {} for player in batter_df["player"].to_list() + pitcher_df["player"].to_list()}

        for i in range(len(batter_df)):
            all_players[batter_df.iloc[i]["player"]][batter_df.iloc[i]["year"]] = batter_df.iloc[i][2:].to_dict()

        for i in range(len(pitcher_df)):
            all_players[pitcher_df.iloc[i]["player"]][pitcher_df.iloc[i]["year"]] = pitcher_df.iloc[i][2:].to_dict()

        with open("./static_data/all_player_data.json", "w") as file:
            json.dump(all_players, file, indent=4)
        
        batting_leaders_2022 = batter_df[batter_df["year"] == "2022"].sort_values(by="b_war_per_dollar_score", ascending=False)[:10].set_index("player").to_dict(orient="index")
        batting_leaders_2023 = batter_df[batter_df["year"] == "2023"].sort_values(by="b_war_per_dollar_score", ascending=False)[:10].set_index("player").to_dict(orient="index")
        batting_leaders_2024 = batter_df[batter_df["year"] == "2024"].sort_values(by="b_war_per_dollar_score", ascending=False)[:10].set_index("player").to_dict(orient="index")

        pitching_leaders_2022 = pitcher_df[pitcher_df["year"] == "2022"].sort_values(by="p_war_per_dollar_score", ascending=False)[:10].set_index("player").to_dict(orient="index")
        pitching_leaders_2023 = pitcher_df[pitcher_df["year"] == "2023"].sort_values(by="p_war_per_dollar_score", ascending=False)[:10].set_index("player").to_dict(orient="index")
        pitching_leaders_2024 = pitcher_df[pitcher_df["year"] == "2024"].sort_values(by="p_war_per_dollar_score", ascending=False)[:10].set_index("player").to_dict(orient="index")

        worst_batters_2024 = batter_df[batter_df["year"] == "2024"].sort_values(by="b_war_per_dollar_score", ascending=True)[:10].set_index("player").to_dict(orient="index")
        worst_pitchers_2024 = pitcher_df[pitcher_df["year"] == "2024"].sort_values(by="p_war_per_dollar_score", ascending=True)[:10].set_index("player").to_dict(orient="index")

        # Dictionary mapping file names to data variables
        data_files = {
            "batting_leaders_2022.json": batting_leaders_2022,
            "batting_leaders_2023.json": batting_leaders_2023,
            "batting_leaders_2024.json": batting_leaders_2024,
            "pitching_leaders_2022.json": pitching_leaders_2022,
            "pitching_leaders_2023.json": pitching_leaders_2023,
            "pitching_leaders_2024.json": pitching_leaders_2024,  # Fix: Previously used batting_leaders_2024 incorrectly
            "worst_batters_2024.json": worst_batters_2024,
            "worst_pitchers_2024.json": worst_pitchers_2024
        }

        # Save each dataset to its respective file
        for filename, data in data_files.items():
            with open(f"./static_data/{filename}", "w") as file:
                json.dump(data, file, indent=4)

        logger.info("Data analysis complete. Files have been successfully updated.")

if __name__ == "__main__":
    main()