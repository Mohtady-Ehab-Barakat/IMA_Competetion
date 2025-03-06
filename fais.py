import faiss
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

def prepare_data_fais(file_path):
    xls = pd.ExcelFile(file_path)
    df = pd.read_excel(xls, sheet_name='Sheet1')

    columns_needed = [
        "Player_Name", "Games_Started", "Minutes_Played", "Field_Goals_Made",
        "Field_Goals_Attempted", "FG_percentage", "Three_Pointers_Made",
        "Three_Pointers_Attempted", "Three_Pointers_Percentage", "Two_Pointers_Made",
        "Two_Pointers_Attempted", "Two_Pointers_Percentage", "Effective_Field_Goal_Percentage",
        "Free_Throws_Made", "Free_Throws_Attempted", "Free_Throws_Percentage", "Offensive_Rebounds",
        "Defensive_Rebounds", "Total_Rebounds", "Assists", "Steals", "Blocks", "Turnovers",
        "Personal_Fouls", "Total_Points"
    ]

    df_filtered = df[columns_needed].copy()  # Avoid modifying the original DataFrame

    # Handle missing values correctly
    numeric_cols = df_filtered.drop(columns=["Player_Name"])
    df_filtered.loc[:, numeric_cols.columns] = numeric_cols.fillna(numeric_cols.mean())

    return df_filtered

def train_faiss(df):
    player_names = df["Player_Name"]
    X = df.drop(columns=["Player_Name"]).values.astype("float32")

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X).astype("float32")

    dimension = X_scaled.shape[1]
    index = faiss.IndexFlatL2(dimension)  # L2 distance for similarity search
    index.add(X_scaled)  # Add player data to the FAISS index

    return index, scaler, player_names, X_scaled

def find_nearest_players_fais(index, scaler, player_names, X, need, top_n=3):
    need_scaled = scaler.transform([need]).astype("float32")
    distances, indices = index.search(need_scaled, top_n)

    nearest_players = [player_names.iloc[i] for i in indices[0]]
    return nearest_players

if __name__ == "__main__":
    file_path = "2025_scc_5a_nba_player_data_2023.xlsx"
    df = prepare_data_fais(file_path)
    index, scaler, player_names, X_scaled = train_faiss(df)

    need = np.array([1, 300, 50, 120, 0.45, 40, 100, 0.4, 10, 20, 0.5, 0.55, 5, 10, 0.8, 5, 30, 40, 20, 10, 5, 5, 20, 100])
    nearest_players = find_nearest_players_fais(index, scaler, player_names, X_scaled, need, top_n=3)

    print("Top 3 players closest to the need vector using FAISS:", nearest_players)
