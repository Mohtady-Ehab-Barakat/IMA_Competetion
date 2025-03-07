import pandas as pd
import os

player_sats = {}
file_path = "/home/moamen/Vector/nba_stat.xlsx"

# ✅ List of columns to use
columns_needed = [
    "Player_Name", "Position", "Games_Played", "Games_Started", "Minutes_Played", 
    "Field_Goals_Made", "Field_Goals_Attempted", "FG_percentage", "Three_Pointers_Made",
    "Three_Pointers_Attempted", "Three_Pointers_Percentage", "Two_Pointers_Made",
    "Two_Pointers_Attempted", "Two_Pointers_Percentage", "Effective_Field_Goal_Percentage",
    "Free_Throws_Made", "Free_Throws_Attempted", "Free_Throws_Percentage", "Offensive_Rebounds",
    "Defensive_Rebounds", "Total_Rebounds", "Assists", "Steals", "Blocks", "Turnovers",
    "Personal_Fouls", "Total_Points"
]

# ✅ Read & filter Excel data
def prepare_data(file_path):
    print(f"Loading data from: {file_path}")
    df = pd.read_excel(file_path, sheet_name='Sheet1')

    # ✅ Filter to only keep necessary columns
    df = df[columns_needed].copy()

    # ✅ Replace NaN values with 0
    df.fillna(0, inplace=True)

    # ✅ Ensure Position is a string
    df["Position"] = df["Position"].astype(str)

    print("Data Loaded:", df.head())
    return df.to_dict(orient="records")

# ✅ Stat calculation functions
def stat_pg(player_stats_dict):
    """ Point Guard Stats: Assists per Game, True Shooting %, Assist/Turnover Ratio, Steals per Game """
    return {
        "PG_APG": player_stats_dict["Assists"] / player_stats_dict["Games_Played"] if player_stats_dict["Games_Played"] > 0 else 0,
        "PG_TS%": (player_stats_dict["Total_Points"] / (2 * (player_stats_dict["Field_Goals_Attempted"] + 0.44 * player_stats_dict["Free_Throws_Attempted"])) * 100) if (player_stats_dict["Field_Goals_Attempted"] + 0.44 * player_stats_dict["Free_Throws_Attempted"]) > 0 else 0,
        "PG_A/T": (player_stats_dict["Assists"] / player_stats_dict["Turnovers"]) if player_stats_dict["Turnovers"] > 0 else 0,
        "PG_SPG": player_stats_dict["Steals"] / player_stats_dict["Games_Played"] if player_stats_dict["Games_Played"] > 0 else 0
    }

def stat_sg(player_stats_dict):
    """ Shooting Guard Stats: Points per Game, Effective FG%, Three-Point % """
    return {
        "SG_PPG": player_stats_dict["Total_Points"] / player_stats_dict["Games_Played"] if player_stats_dict["Games_Played"] > 0 else 0,
        "SG_EFG%": ((player_stats_dict["Field_Goals_Made"] + 0.5 * player_stats_dict["Three_Pointers_Made"]) / 
                    player_stats_dict["Field_Goals_Attempted"] * 100) if player_stats_dict["Field_Goals_Attempted"] > 0 else 0,
        "SG_3P%": (player_stats_dict["Three_Pointers_Made"] / player_stats_dict["Three_Pointers_Attempted"] * 100) if player_stats_dict["Three_Pointers_Attempted"] > 0 else 0
    }

def stat_center(player_stats_dict):
    """ Center Stats: Defensive Rating, Blocks per Game, Rebound Percentage """
    return {
        "C_DRTG": (player_stats_dict["Defensive_Rebounds"] / player_stats_dict["Games_Played"]) * 100 if player_stats_dict["Games_Played"] > 0 else 0,
        "C_BPG": player_stats_dict["Blocks"] / player_stats_dict["Games_Played"] if player_stats_dict["Games_Played"] > 0 else 0,
        "C_REB%": ((player_stats_dict["Offensive_Rebounds"] + player_stats_dict["Defensive_Rebounds"]) / player_stats_dict["Total_Rebounds"] * 100) if player_stats_dict["Total_Rebounds"] > 0 else 0
    }

def stat_sf(player_stats_dict):
    """ Small Forward Stats: Rebounds per Game, Steals per Game, Blocks per Game, Points per Game """
    return {
        "SF_RPG": (player_stats_dict["Offensive_Rebounds"] + player_stats_dict["Defensive_Rebounds"]) / player_stats_dict["Games_Played"] if player_stats_dict["Games_Played"] > 0 else 0,
        "SF_SPG": player_stats_dict["Steals"] / player_stats_dict["Games_Played"] if player_stats_dict["Games_Played"] > 0 else 0,
        "SF_BPG": player_stats_dict["Blocks"] / player_stats_dict["Games_Played"] if player_stats_dict["Games_Played"] > 0 else 0,
        "SF_PPG": player_stats_dict["Total_Points"] / player_stats_dict["Games_Played"] if player_stats_dict["Games_Played"] > 0 else 0
    }

def stat_pf(player_stats_dict):
    """ Power Forward Stats: Rebound Percentage, Block Percentage """
    return {
        "PF_REB%": ((player_stats_dict["Offensive_Rebounds"] + player_stats_dict["Defensive_Rebounds"]) / player_stats_dict["Total_Rebounds"] * 100) if player_stats_dict["Total_Rebounds"] > 0 else 0,
        "PF_BLK%": (player_stats_dict["Blocks"] / (player_stats_dict["Blocks"] + player_stats_dict["Steals"]) * 100) if (player_stats_dict["Blocks"] + player_stats_dict["Steals"]) > 0 else 0
    }

# ✅ Process players & organize data
def process_players(player_stats_list):
    player_sats = {}  

    for player_stats in player_stats_list:
        player_name = player_stats.get("Player_Name", "Unknown")
        position = player_stats.get("Position", "").strip()

        if player_name not in player_sats:
            player_sats[player_name] = {}  # Initialize empty dictionary for each player

        # Assign stats based on position
        if position == "PG":
            player_sats[player_name].update(stat_pg(player_stats))
        elif position == "SG":
            player_sats[player_name].update(stat_sg(player_stats))
        elif position == "C":
            player_sats[player_name].update(stat_center(player_stats))
        elif position == "SF":
            player_sats[player_name].update(stat_sf(player_stats))
        elif position == "PF":
            player_sats[player_name].update(stat_pf(player_stats))

    return player_sats

# ✅ Create Excel with individual columns for each position's statistics
def create_excel(player_sats):
    df = pd.DataFrame.from_dict(player_sats, orient="index")

    output_file = "/home/moamen/Vector/IMA_Competetion/player_stats_fixed.xlsx"

    df.to_excel(output_file, index_label="Player_Name")
    print(f"Data saved successfully to {output_file}")

if __name__ == "__main__":
    player_stats_list = prepare_data(file_path)
    player_sats = process_players(player_stats_list)
    create_excel(player_sats)
    print("Excel file created successfully!")
