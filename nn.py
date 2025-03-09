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
        "Player_Name", "PPG", "APG", "SPG", "BPG", "RPG", "TS%", "A/T Ratio", "EFG%", "3P%", "REB%"
    ]
    df_filtered = df[columns_needed].copy()  # Explicitly make a copy
    
    # Handle missing values by filling with column mean
    numeric_cols = df_filtered.drop(columns=["Player_Name"])
    df_filtered.loc[:, numeric_cols.columns] = numeric_cols.fillna(numeric_cols.mean()).copy()
    
    return df_filtered

# Train Neural Network Model
def train_neural_network(df):
    player_names = df["Player_Name"]  # Store player names separately
    X = df.drop(columns=["Player_Name"])  # Features (without names)
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)  # Normalize the features
    
    if X_scaled.shape[0] == 0:
        raise ValueError("Training data is empty after processing. Check the dataset.")

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
    need_df = pd.DataFrame([need], columns=X.columns)  # Ensure correct structure
    need_scaled = scaler.transform(need_df)
    
    predictions = model.predict(X)
    player_scores = dict(zip(player_names, predictions.flatten()))
    nearest_players = sorted(player_scores, key=player_scores.get, reverse=True)[:top_n]
    
    return nearest_players

if __name__ == "__main__":
    file_path = "player_stats_all.xlsx"
    df = prepare_data_nn(file_path)
    model, scaler, player_names, X = train_neural_network(df)
    
    need = np.array([0.24, 0.5, 0.72, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5])
    nearest_players = find_nearest_players_nn(model, scaler, player_names, X, need, top_n=3)
    
    print("Top 3 players closest to the need vector:", nearest_players)
