import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from sklearn.preprocessing import StandardScaler

# Load the Excel file
def prepare_data_nn(file_path):
    xls = pd.ExcelFile(file_path)
    df = pd.read_excel(xls, sheet_name='Sheet1')
    
    columns_needed = [
        "Player_Name", "PPG", "APG", "SPG",	"BPG", "RPG", "TS%", "A/T Ratio", "EFG%", "3P%", "REB%"
    ]
    df_filtered = df[columns_needed]
    
    # Handle missing values by filling with column mean
    numeric_cols = df_filtered.drop(columns=["Player_Name"])
    df_filtered[numeric_cols.columns] = numeric_cols.fillna(numeric_cols.mean())
    
    return df_filtered

# Train Neural Network Model
def train_neural_network(df):
    player_names = df["Player_Name"]  # Store player names separately
    X = df.drop(columns=["Player_Name"])  # Features (without names)
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)  # Normalize the features
    
    y = np.random.rand(len(X))  # Placeholder target (random similarity scores)
    
    model = keras.Sequential([
        keras.layers.Dense(64, activation='relu', input_shape=(X.shape[1],)),
        keras.layers.Dense(32, activation='relu'),
        keras.layers.Dense(1, activation='linear')
    ])
    
    model.compile(optimizer='adam', loss='mse')
    model.fit(X_scaled, y, epochs=100, verbose=0, batch_size=8)
    
    return model, scaler, player_names, X

# Predict similarity to the need vector
def find_nearest_players_nn(model, scaler, player_names, X, need, top_n=3):
    need_scaled = scaler.transform([need])
    predictions = model.predict(X)
    
    player_scores = dict(zip(player_names, predictions.flatten()))
    nearest_players = sorted(player_scores, key=player_scores.get, reverse=True)[:top_n]
    
    return nearest_players

if __name__ == "__main__":
    file_path = "2025_scc_5a_nba_player_data_2023.xlsx"
    df = prepare_data_nn(file_path)
    model, scaler, player_names, X = train_neural_network(df)
    
    need = np.array([1, 300, 50, 120, 0.45, 40, 100, 0.4, 10, 20, 0.5, 0.55, 5, 10, 0.8, 5, 30, 40, 20, 10, 5, 5, 20, 100])
    nearest_players = find_nearest_players_nn(model, scaler, player_names, X, need, top_n=3)
    
    print("Top 3 players closest to the need vector:", nearest_players)
