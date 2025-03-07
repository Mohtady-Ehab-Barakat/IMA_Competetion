import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import os

player_sats={}
file_path = "/home/moamen/Vector/nba_stat.xlsx"
def prepare_data(file_path):
    xls = pd.ExcelFile(file_path)
    df = pd.read_excel(xls, sheet_name='Sheet1')
    columns_needed = [
        "Player_Name","Position",  "Games_Played","Games_Started", "Minutes_Played", "Field_Goals_Made",
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
    player_stats_dict = df_filtered.to_dict(orient="records")
    return player_stats_dict

def stat_pg(player_stats_dict, player_sats):
    stats0 = []
    player_name = player_stats_dict["Player_Name"]
    apg = player_stats_dict["Assists"] / player_stats_dict["Games_Played"]
    stats0.append(apg)
    ts_percentage = (player_stats_dict["Total_Points"] / (2 * (player_stats_dict["Field_Goals_Attempted"] + 0.44 * player_stats_dict["Free_Throws_Attempted"]))) * 100
    stats0.append(ts_percentage)
    at_percentage = (player_stats_dict["Assists"] / player_stats_dict["Turnovers"] * 100) if player_stats_dict["Turnovers"] > 0 else 0
    stats0.append(at_percentage)
    usg_percentage = ((player_stats_dict["Field_Goals_Attempted"] + 0.44 * player_stats_dict["Free_Throws_Attempted"] + player_stats_dict["Turnovers"]) * (player_stats_dict["Minutes_Played"] / 5)) / (player_stats_dict["Minutes_Played"] * (player_stats_dict["Field_Goals_Attempted"] + 0.44 * player_stats_dict["Free_Throws_Attempted"] + player_stats_dict["Turnovers"]))
    stats0.append(usg_percentage)
    spg_percentage = player_stats_dict["Steals"] / player_stats_dict["Games_Played"]
    stats0.append(spg_percentage)
    player_sats[player_name] = stats0
    return player_sats

def stat_sg(player_stats_dict, player_sats):
    stats1 = []
    player_name = player_stats_dict["Player_Name"]
    ppg = player_stats_dict["Total_Points"] / player_stats_dict["Games_Played"]
    stats1.append(ppg)
    efg_percentage = (player_stats_dict["Field_Goals_Made"] + 0.5 * player_stats_dict["Three_Pointers_Made"]) / player_stats_dict["Field_Goals_Attempted"] * 100
    stats1.append(efg_percentage)
    threep_percentage = (player_stats_dict["Three_Pointers_Made"] / player_stats_dict["Three_Pointers_Attempted"]) * 100
    stats1.append(threep_percentage)
    player_sats[player_name] = stats1
    return  player_sats

def stat_center(player_stats_dict, player_sats):
    stats2 = []
    player_name = player_stats_dict["Player_Name"]
    drtg = (player_stats_dict["Defensive_Rebounds"] / player_stats_dict["Games_Played"]) * 100  # Approximation
    stats2.append(drtg)
    bpg = player_stats_dict["Blocks"] / player_stats_dict["Games_Played"]
    stats2.append(bpg)
    reb_percentage = (player_stats_dict["Offensive_Rebounds"] + player_stats_dict["Defensive_Rebounds"]) / player_stats_dict["Total_Rebounds"] * 100
    stats2.append(reb_percentage)
    player_sats[player_name] = stats2
    return  player_sats

def stat_sf(player_stats_dict, player_sats):
    stats3 = []  
    player_name = player_stats_dict["Player_Name"]
    rpg = (player_stats_dict["Offensive_Rebounds"] + player_stats_dict["Defensive_Rebounds"]) / player_stats_dict["Games_Played"]
    stats3.append(rpg)
    spg = player_stats_dict["Steals"] / player_stats_dict["Games_Played"]
    stats3.append(spg)
    bpg = player_stats_dict["Blocks"] / player_stats_dict["Games_Played"]
    stats3.append(bpg)
    ppg = player_stats_dict["Total_Points"] / player_stats_dict["Games_Played"] if player_stats_dict["Games_Played"] > 0 else 0
    stats3.append(ppg)
    player_sats[player_name] = stats3
    return player_sats

def stat_pf(player_stats_dict, player_sats):
    stats4 = []
    player_name = player_stats_dict["Player_Name"]
    reb_percentage = (player_stats_dict["Offensive_Rebounds"] + player_stats_dict["Defensive_Rebounds"]) / player_stats_dict["Total_Rebounds"] * 100
    stats4.append(reb_percentage)
    blk_percentage = player_stats_dict["Blocks"] / (player_stats_dict["Blocks"] + player_stats_dict["Steals"]) * 100
    stats4.append(blk_percentage)
    player_sats[player_name] = stats4
    return  player_sats

def create_csv(player_sats):
    df = pd.DataFrame.from_dict(player_sats, orient="index", columns=["Stat1", "Stat2", "Stat3", "Stat4"])
    df.to_csv("player_stats.csv", index_label="Player_Name")


def clean_data(player_stats):
    for player, stats in player_stats.items():
        for key, value in stats.items():
            stats[key] = 0 if pd.isna(value) else value
    return player_stats

def process_players(player_stats_list):
    player_sats = {} 
    for player_stats in player_stats_list:
        position = player_stats.get("Position", "").strip()
        if position == "PG":
            player_sats = stat_pg(player_stats, player_sats)
        elif position == "SG":
            player_sats = stat_sg(player_stats, player_sats)
        elif position == "C":
            player_sats = stat_center(player_stats, player_sats)
        elif position == "PF":
            player_sats = stat_pf(player_stats, player_sats)
        elif position == "SF":
            player_sats = stat_sf(player_stats, player_sats)
    return player_sats


# if __name__ == "__main__":
#     file_path = "nba_stat.xlsx"