import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler

# Load the Excel file
def prepare_data_rf(file_path):
    xls = pd.ExcelFile(file_path)
    df = pd.read_excel(xls, sheet_name='Sheet1')
    
    columns_needed = [
        "Player_Name", "PPG", "APG", "SPG",	"BPG", "RPG", "TS%", "A/T Ratio", "EFG%", "3P%", "REB%", "BLK%", "DRTG", "USG%"
    ]
    df_filtered = df[columns_needed]
    return df_filtered

# Train Random Forest Model
def train_random_forest(df):
    player_names = df["Player_Name"]  # Store player names separately
    X = df.drop(columns=["Player_Name"])  # Features (without names)
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)  # Normalize the features
    
    y = np.random.rand(len(X))  # Placeholder target (random similarity scores)
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_scaled, y)
    
    return model, scaler, player_names, X

# Predict similarity to the need vector
def find_nearest_players(model, scaler, player_names, X, need, top_n=3):
    need_scaled = scaler.transform([need])
    predictions = model.predict(X)
    
    player_scores = dict(zip(player_names, predictions))
    nearest_players = sorted(player_scores, key=player_scores.get, reverse=True)[:top_n]
    
    return nearest_players

if __name__ == "__main__":
    file_path = "2025_scc_5a_nba_player_data_2023.xlsx"
    df = prepare_data_rf(file_path)
    model, scaler, player_names, X = train_random_forest(df)
    
    need = np.array([1, 300, 50, 120, 0.45, 40, 100, 0.4, 10, 20, 0.5, 0.55, 5, 10, 0.8, 5, 30, 40, 20, 10, 5, 5, 20, 100])
    nearest_players = find_nearest_players(model, scaler, player_names, X, need, top_n=3)
    
    print("Top 3 players closest to the need vector:", nearest_players)
