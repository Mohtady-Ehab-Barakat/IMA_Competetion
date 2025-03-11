import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Load the Excel file
def prepare_data_kmeans(file_path):
    xls = pd.ExcelFile(file_path)
    df = pd.read_excel(xls, sheet_name='Sheet1')
    
    columns_needed = [
        "Player_Name", "PPG", "APG", "SPG",	"BPG", "RPG", "TS%", "A/T Ratio", "EFG%", "3P%", "REB%", "BLK%", "DRTG", "USG%"
    ]
    df_filtered = df[columns_needed]
    
    # Handle missing values by filling with column mean
    numeric_cols = df_filtered.drop(columns=["Player_Name"])
    df_filtered[numeric_cols.columns] = numeric_cols.fillna(numeric_cols.mean())
    
    return df_filtered

# Train K-Means Clustering Model
def train_kmeans(df, n_clusters=5):
    player_names = df["Player_Name"]  # Store player names separately
    X = df.drop(columns=["Player_Name"])  # Features (without names)
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)  # Normalize the features
    
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    kmeans.fit(X_scaled)
    
    return kmeans, scaler, player_names, X

# Find the nearest players within the same cluster
def find_nearest_players_kmeans(kmeans, scaler, player_names, X, need, top_n=3):
    need_scaled = scaler.transform([need])
    cluster_label = kmeans.predict(need_scaled)[0]
    
    # Get all players in the same cluster
    cluster_players = [player_names[i] for i in range(len(player_names)) if kmeans.labels_[i] == cluster_label]
    
    return cluster_players[:top_n]  # Return top N players from the same cluster

if __name__ == "__main__":
    file_path = "2025_scc_5a_nba_player_data_2023.xlsx"
    df = prepare_data_kmeans(file_path)
    kmeans, scaler, player_names, X = train_kmeans(df, n_clusters=5)
    
    need = np.array([1, 300, 50, 120, 0.45, 40, 100, 0.4, 10, 20, 0.5, 0.55, 5, 10, 0.8, 5, 30, 40, 20, 10, 5, 5, 20, 100])
    nearest_players = find_nearest_players_kmeans(kmeans, scaler, player_names, X, need, top_n=3)
    
    print("Top 3 players closest to the need vector within the same cluster:", nearest_players)