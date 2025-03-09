import pandas as pd
import os

file_path = "2025_scc_5a_nba_player_data_2023.xlsx"

# List of columns to use
columns_needed = [
    "Player_Name", "Games_Played", "Games_Started", "Minutes_Played", 
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
def normalize_stat(df, stat):
    max_value = df[stat].max()
    return df[stat] / max_value if max_value > 0 else df[stat]

# Universal stat calculation function
def calculate_stats(df):
    """ Calculate all relevant stats for players. """
    stats_df = pd.DataFrame()
    stats_df["Player_Name"] = df["Player_Name"]
    
    stats_df["PPG"] = normalize_stat(df, "Total_Points")
    stats_df["APG"] = normalize_stat(df, "Assists")
    stats_df["SPG"] = normalize_stat(df, "Steals")
    stats_df["BPG"] = normalize_stat(df, "Blocks")
    stats_df["RPG"] = normalize_stat(df, "Offensive_Rebounds") + normalize_stat(df, "Defensive_Rebounds")
    
    stats_df["TS%"] = df["Total_Points"] / (2 * (df["Field_Goals_Attempted"] + 0.44 * df["Free_Throws_Attempted"]))
    stats_df["TS%"].fillna(0, inplace=True)
    
    stats_df["A/T Ratio"] = normalize_stat(df, "Assists") / (normalize_stat(df, "Turnovers") + 1e-6)  # Avoid division by zero
    stats_df["A/T Ratio"].fillna(0, inplace=True)
    
    stats_df["EFG%"] = (df["Field_Goals_Made"] + 0.5 * df["Three_Pointers_Made"]) / df["Field_Goals_Attempted"]
    stats_df["EFG%"].fillna(0, inplace=True)
    
    stats_df["3P%"] = df["Three_Pointers_Made"] / df["Three_Pointers_Attempted"]
    stats_df["3P%"].fillna(0, inplace=True)
    
    stats_df["REB%"] = normalize_stat(df, "Offensive_Rebounds") + normalize_stat(df, "Defensive_Rebounds")
    stats_df["REB%"].fillna(0, inplace=True)
    
    return stats_df

# Create Excel file with calculated stats
def create_excel(df):
    output_file = "player_stats_all.xlsx"
    df.to_excel(output_file, index_label="Player_Name")
    print(f"Data saved successfully to {output_file}")

if __name__ == "__main__":
    df = prepare_data(file_path)
    stats_df = calculate_stats(df)
    create_excel(stats_df)
    print("Excel file created successfully!")
