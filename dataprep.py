import pandas as pd
import os
import numpy as np

file_path = "2025_scc_5a_nba_player_data_2023.xlsx"

# List of columns to use
columns_needed = [
    "Player_Name", "Team","Games_Played", "Games_Started", "Minutes_Played", 
    "Field_Goals_Made", "Field_Goals_Attempted", "FG_percentage", "Three_Pointers_Made",
    "Three_Pointers_Attempted", "Three_Pointers_Percentage", "Two_Pointers_Made",
    "Two_Pointers_Attempted", "Two_Pointers_Percentage", "Effective_Field_Goal_Percentage",
    "Free_Throws_Made", "Free_Throws_Attempted", "Free_Throws_Percentage", "Offensive_Rebounds",
    "Defensive_Rebounds", "Total_Rebounds", "Assists", "Steals", "Blocks", "Turnovers",
    "Personal_Fouls", "Total_Points"
]

# Read & filter Excel data
def prepare_data(file_path):
    print(f"Loading data from: {file_path}")
    df = pd.read_excel(file_path, sheet_name='Sheet1')
    df = df[columns_needed].copy()
    df.fillna(0, inplace=True)
    print("Data Loaded:", df.head())
    return df

# Normalize non-percentage stats
def normalize_stat(series):
    max_value = series.max()
    return series / max_value if max_value > 0 else series

# Universal stat calculation function
def calculate_stats(df):
    """ Calculate all relevant stats for players. """
    stats_df = pd.DataFrame()
    stats_df["Player_Name"] = df["Player_Name"]
    stats_df["Team"] = df["Team"]

    stats_df["PPG"] = df["Total_Points"] / df["Games_Played"]
    stats_df["APG"] = df["Assists"] / df["Games_Played"]
    stats_df["SPG"] = df["Steals"] / df["Games_Played"]
    stats_df["BPG"] = df["Blocks"] / df["Games_Played"]
    stats_df["RPG"] = df["Total_Rebounds"] / df["Games_Played"]

    # True Shooting Percentage (TS%)
    stats_df["TS%"] = df["Total_Points"] / (2 * (df["Field_Goals_Attempted"] + 0.44 * df["Free_Throws_Attempted"]))
    stats_df["TS%"].fillna(0, inplace=True)

    # Assist-to-Turnover Ratio (A/T Ratio)
    stats_df["A/T Ratio"] = np.where(df["Turnovers"] > 0, df["Assists"] / df["Turnovers"], 0) 
    stats_df["A/T Ratio"] = normalize_stat(stats_df["A/T Ratio"])
    stats_df["A/T Ratio"].fillna(0, inplace=True)

    # Effective Field Goal Percentage (EFG%)
    stats_df["EFG%"] = (df["Field_Goals_Made"] + 0.5 * df["Three_Pointers_Made"]) / df["Field_Goals_Attempted"]
    stats_df["EFG%"].fillna(0, inplace=True)

    # Three-Point Percentage (3P%)
    stats_df["3P%"] = df["Three_Pointers_Made"] / df["Three_Pointers_Attempted"]
    stats_df["3P%"].fillna(0, inplace=True)

    # Rebounding Percentage (REB%)
    stats_df["REB%"] = df["Total_Rebounds"] / df["Total_Rebounds"].sum() if df["Total_Rebounds"].sum() > 0 else df["Total_Rebounds"]
    stats_df["REB%"].fillna(0, inplace=True)

    # Block Percentage (BLK%)
    team_minutes_played = df["Games_Played"] * 240  # 5 players per 48 min
    opponent_2pa = df["Field_Goals_Attempted"] - df["Three_Pointers_Attempted"]
    stats_df["BLK%"] = (df["Blocks"] * (team_minutes_played / 5)) / (df["Minutes_Played"] * opponent_2pa)
    stats_df["BLK%"] = (stats_df["BLK%"] * 100).replace([np.inf, -np.inf], np.nan).fillna(0)
    
    # Defensive Rating (DRTG)
    total_possessions = 0.5 * (df["Field_Goals_Attempted"] + 0.44 * df["Free_Throws_Attempted"]
                               - df["Offensive_Rebounds"] + df["Turnovers"])
    stats_df["DRTG"] = 100 * (df["Total_Points"] * (df["Steals"] + df["Blocks"] + df["Defensive_Rebounds"])) / total_possessions
    stats_df["DRTG"] = stats_df["DRTG"].replace([np.inf, -np.inf], np.nan).fillna(0)
    
    # Usage Percentage (USG%)
    stats_df["USG%"] = ((df["Field_Goals_Attempted"] + 0.44 * df["Free_Throws_Attempted"] + df["Turnovers"]) * (team_minutes_played / 5)) / \
                        (df["Minutes_Played"] * (df["Field_Goals_Attempted"] + 0.44 * df["Free_Throws_Attempted"] + df["Turnovers"]))
    stats_df["USG%"] = (stats_df["USG%"] * 100).replace([np.inf, -np.inf], np.nan).fillna(0)

    return stats_df

# Create Excel file with calculated stats
def create_excel(df):
    output_file = "player_stats_all.xlsx"
    df.to_excel(output_file, index=False)
    print(f"Data saved successfully to {output_file}")

if __name__ == "__main__":
    df = prepare_data(file_path)
    stats_df = calculate_stats(df)
    create_excel(stats_df)
    print("Excel file created successfully!")
