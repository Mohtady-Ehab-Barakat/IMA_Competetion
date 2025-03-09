import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def calculate_team_needs(file_path):
    # Load the Excel file
    xls = pd.ExcelFile(file_path)
    
    # Load the first sheet into a dataframe
    df = xls.parse('Sheet1')
    
    # Group by Team and sum the stats
    team_stats = df.groupby("Team").sum(numeric_only=True)
    
    # Normalize the stats using MinMaxScaler
    scaler = MinMaxScaler()
    normalized_stats = pd.DataFrame(scaler.fit_transform(team_stats), 
                                    columns=team_stats.columns, 
                                    index=team_stats.index)
    
    # Calculate 1 minus each number to represent the need
    needed_stats = 1 - normalized_stats
    
    # Convert to dictionary
    team_dict = {team: stats.tolist() for team, stats in needed_stats.iterrows()}
    keys_to_keep = {"MIL", "CLE", "BRK", "ATL", "MIN", "LAC", "SAC", "MEM"}
    filtered_dict = {key: team_dict[key] for key in keys_to_keep if key in team_dict}

    
    return filtered_dict

if __name__ == "__main__":
    file_path = "player_stats_all.xlsx"
    teams_needs = calculate_team_needs(file_path)
    print(teams_needs)
