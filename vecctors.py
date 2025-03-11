import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


# player1 = np.array([5, -9, 2, 5])
# player2 = np.array([3, 2, 8, -9])

# distance = np.linalg.norm(player1 - player2)
# print(distance)


# Load the Excel file
def prepare_data(file_path):
    xls = pd.ExcelFile(file_path)

    # Load the first sheet into a DataFrame
    df = pd.read_excel(xls, sheet_name='Sheet1')

    # Selecting relevant columns
    columns_needed = [
        "Player_Name", "PPG", "APG", "SPG",	"BPG", "RPG", "TS%", "A/T Ratio", "EFG%", "3P%", "REB%", "BLK%", "DRTG", "USG%"
    ]

    # Filtering the dataframe to only needed columns
    df_filtered = df[columns_needed]

    # Creating the dictionary
    player_stats_dict = df_filtered.set_index("Player_Name").T.to_dict()

    return player_stats_dict

# Clean the data
def clean_data(player_stats_dict):
    for player, stats in player_stats_dict.items():
        for key, value in stats.items():
            if pd.isna(value):  # Check if value is NaN
                stats[key] = 0  # Replace with 0 or a reasonable default
    return player_stats_dict

def calculate_distance(player_stats_dict,need):
    player_distances = {}
    for player, stats in player_stats_dict.items():
        player_vector = np.array(list(stats.values()))  # Convert player's stats to a NumPy array
        distance = np.linalg.norm(player_vector - need)  # Calculate Euclidean distance
        player_distances[player] = distance

    return player_distances

def get_nearest_players(player_distances, n):
    nearest_players = sorted(player_distances, key=player_distances.get)[:n]
    return nearest_players

def calculate_cosine_similarity(player_stats_dict, need):
    need_vector = need.reshape(1, -1)  # Reshape for compatibility
    player_similarities = {}

    for player, stats in player_stats_dict.items():
        player_vector = np.array(list(stats.values())).reshape(1, -1)
        similarity = cosine_similarity(player_vector, need_vector)[0][0]
        player_similarities[player] = similarity

    return player_similarities

def calculate_manhattan_distance(player_stats_dict, need):
    player_distances = {}
    
    for player, stats in player_stats_dict.items():
        player_vector = np.array(list(stats.values()))
        distance = np.sum(np.abs(player_vector - need))
        player_distances[player] = distance

    return player_distances

# Get players with highest similarity (instead of lowest distance)
def get_most_similar_players(player_similarities, n):
    return sorted(player_similarities, key=player_similarities.get, reverse=True)[:n]


def calculate_weighted_distance(player_stats_dict, need, weights):
    player_distances = {}
    
    for player, stats in player_stats_dict.items():
        player_vector = np.array(list(stats.values()))
        weighted_diff = weights * (player_vector - need)
        distance = np.linalg.norm(weighted_diff)
        player_distances[player] = distance

    return player_distances

if __name__== "__main__":
    weights = np.array([1, 0.5, 0.8, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1.5, 1, 1, 2, 1, 1, 1, 1.2, 1.2, 1.5, 1, 0.8])
    need = np.array([1, 300, 50, 120, 0.45, 40, 100, 0.4, 10, 20, 0.5, 0.55, 5, 10, 0.8, 5, 30, 40, 20, 10, 5, 5, 20, 100])
    file_path = "2025_scc_5a_nba_player_data_2023.xlsx"
    player_stats_dict = prepare_data(file_path)
    player_stats_dict = clean_data(player_stats_dict)
    player_distances = calculate_distance(player_stats_dict,need)
    nearest_players_distance = get_nearest_players(player_distances, 3)
    player_similarities = calculate_cosine_similarity(player_stats_dict, need)
    nearest_players_cosign_similarity = get_most_similar_players(player_similarities, 3)
    player_manhattan_distances = calculate_manhattan_distance(player_stats_dict, need)
    nearest_players_manhattan = get_nearest_players(player_manhattan_distances, 3)
    player_weighted_distances = calculate_weighted_distance(player_stats_dict, need, weights)
    nearest_players_weighted_euclidean = get_nearest_players(player_weighted_distances, 3)
    print("Top 3 players closest to the need vector using Euclidean distance:", nearest_players_distance)
    print("Top 3 players closest to the need vector using Cosine similarity:", nearest_players_cosign_similarity)
    print("Top 3 players closest to the need vector using Manhattan distance:", nearest_players_manhattan)
    print("Top 3 players closest to the need vector using Weighted Euclidean distance:", nearest_players_weighted_euclidean)    
