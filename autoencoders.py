import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from sklearn.preprocessing import StandardScaler

# Load the Excel file
def prepare_data_autoencoders(file_path):
    xls = pd.ExcelFile(file_path)
    df = pd.read_excel(xls, sheet_name='Sheet1')
    
    columns_needed = [
        "Player_Name", "PPG", "APG", "SPG",	"BPG", "RPG", "TS%", "A/T Ratio", "EFG%", "3P%", "REB%"
    ]
    df_filtered = df[columns_needed].copy()
    
    # Handle missing values
    numeric_cols = df_filtered.drop(columns=["Player_Name"])
    df_filtered.loc[:, numeric_cols.columns] = numeric_cols.fillna(numeric_cols.mean())
    
    return df_filtered

# Train Autoencoder
def train_autoencoder(df, encoding_dim=16, epochs=50, batch_size=8):
    player_names = df["Player_Name"]  # Store player names separately
    X = df.drop(columns=["Player_Name"]).values.astype("float32")
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    input_dim = X_scaled.shape[1]
    
    # Build autoencoder
    input_layer = keras.layers.Input(shape=(input_dim,))
    encoded = keras.layers.Dense(encoding_dim, activation='relu')(input_layer)
    decoded = keras.layers.Dense(input_dim, activation='linear')(encoded)
    
    autoencoder = keras.Model(input_layer, decoded)
    encoder = keras.Model(input_layer, encoded)  # Encoder to extract compressed representation
    
    autoencoder.compile(optimizer='adam', loss='mse')
    autoencoder.fit(X_scaled, X_scaled, epochs=epochs, batch_size=batch_size, verbose=1)
    
    return encoder, scaler, player_names, X_scaled

# Find similar players using autoencoder
def find_nearest_players_autoencoders(encoder, scaler, player_names, X, need, top_n=3):
    need_scaled = scaler.transform([need])
    need_encoded = encoder.predict(need_scaled)
    X_encoded = encoder.predict(X)
    
    # Compute Euclidean distances
    distances = np.linalg.norm(X_encoded - need_encoded, axis=1)
    nearest_indices = np.argsort(distances)[:top_n]
    
    nearest_players = [player_names.iloc[i] for i in nearest_indices]
    return nearest_players

if __name__ == "__main__":
    file_path = "2025_scc_5a_nba_player_data_2023.xlsx"
    df = prepare_data_autoencoders(file_path)
    encoder, scaler, player_names, X_scaled = train_autoencoder(df, encoding_dim=16, epochs=50, batch_size=8)
    
    need = np.array([0.24,0.5,0.72,0.5,0.5,0.5,0.5,0.5,0.5,0.5])
    nearest_players = find_nearest_players_autoencoders(encoder, scaler, player_names, X_scaled, need, top_n=3)
    
    print("Top 3 players closest to the need vector using Autoencoder:", nearest_players)
