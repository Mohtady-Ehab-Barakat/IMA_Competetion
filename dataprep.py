import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import os

player_sats={}

def prepare_data(file_path):
    xls = pd.ExcelFile(file_path)

    # Load the first sheet into a DataFrame
    df = pd.read_excel(xls, sheet_name='Sheet1')

    # Selecting relevant columns
    columns_needed = [
        "Player_Name", "Games_Played","Games_Started", "Minutes_Played", "Field_Goals_Made",
        "Field_Goals_Attempted", "FG_percentage", "Three_Pointers_Made",
        "Three_Pointers_Attempted", "Three_Pointers_Percentage", "Two_Pointers_Made",
        "Two_Pointers_Attempted", "Two_Pointers_Percentage", "Effective_Field_Goal_Percentage",
        "Free_Throws_Made", "Free_Throws_Attempted", "Free_Throws_Percentage", "Offensive_Rebounds",
        "Defensive_Rebounds", "Total_Rebounds", "Assists", "Steals", "Blocks", "Turnovers",
        "Personal_Fouls", "Total_Points"
    ]

    # Filtering the dataframe to only needed columns
    df_filtered = df[columns_needed]

    # Creating the dictionary
    player_stats_dict = df_filtered.set_index("Player_Name").T.to_dict()

    return player_stats_dict

def stat_pg(player_stats_dict, player_sats):
    stats = []
    player_name = player_stats_dict["Player_Name"]
    apg = player_stats_dict["Assists"] / player_stats_dict["Games_Played"]
    stats.append(apg)
    ts_percentage = (player_stats_dict["Total_Points"] / (2 * (player_stats_dict["Field_Goals_Attempted"] + 0.44 * player_stats_dict["Free_Throws_Attempted"]))) * 100
    stats.append(ts_percentage)
    at_percentage = player_stats_dict["Assists"] / player_stats_dict["Turnovers"] * 100
    stats.append(at_percentage)
    usg_percentage = ((player_stats_dict["Field_Goals_Attempted"] + 0.44 * player_stats_dict["Free_Throws_Attempted"] + player_stats_dict["Turnovers"]) * (player_stats_dict["Minutes_Played"] / 5)) / (player_stats_dict["Minutes_Played"] * (player_stats_dict["Field_Goals_Attempted"] + 0.44 * player_stats_dict["Free_Throws_Attempted"] + player_stats_dict["Turnovers"]))
    stats.append(usg_percentage)
    spg_percentage = player_stats_dict["Steals"] / player_stats_dict["Games_Played"]
    stats.append(spg_percentage)
    player_sats[player_name] = stats
    return player_sats

def stat_sg(player_stats):
    return  
def stat_center(player_stats):
    return  
def stat_pf(player_stats):  
    return
def stat_sf(player_stats):
    return  

def create_csv(player_sats):
    df = pd.DataFrame(player_sats)
    df.to_csv("player_stats.csv")

def clean_data(player_stats):
    for player, stats in player_stats.items():
        for key, value in stats.items():
            if pd.isna(value):  # Check if value is NaN
                stats[key] = 0  # Replace with 0 or a reasonable default
    return player_stats

def router(player_stats):
    position = player_stats["Position"]
    if position == "PG":
        return stat_pg(player_stats)
    elif position == "SG":
        return stat_sg(player_stats)
    elif position == "C":
        return stat_center(player_stats)
    elif position == "PF":
        return stat_pf(player_stats)
    elif position == "SF":
        return stat_sf(player_stats)
    
if __name__ == "__main__":
    file_path = "2025_scc_5a_nba_player_data_2023.xlsx"