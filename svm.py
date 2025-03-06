import numpy as np
import pandas as pd
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler

# Load the Excel file
def prepare_data_svm(file_path):
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
    df_filtered = df[columns_needed]
    
    # Handle missing values by filling with column mean
    numeric_cols = df_filtered.drop(columns=["Player_Name"])
    df_filtered[numeric_cols.columns] = numeric_cols.fillna(numeric_cols.mean())
    
    return df_filtered

# Train SVM Model
def train_svm(df):
    player_names = df["Player_Name"]  # Store player names separately
    X = df.drop(columns=["Player_Name"])  # Features (without names)
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)  # Normalize the features
    
    y = np.random.rand(len(X))  # Placeholder target (random similarity scores)
    
    model = SVR(kernel='rbf')  # Radial basis function (RBF) kernel for smooth similarity prediction
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
    df = prepare_data_svm(file_path)
    model, scaler, player_names, X = train_svm(df)
    
    need = np.array([1, 300, 50, 120, 0.45, 40, 100, 0.4, 10, 20, 0.5, 0.55, 5, 10, 0.8, 5, 30, 40, 20, 10, 5, 5, 20, 100])
    nearest_players = find_nearest_players(model, scaler, player_names, X, need, top_n=3)
    
    print("Top 3 players closest to the need vector:", nearest_players)
