import pandas as pd
from run import *

# Load player statistics
file_path = "player_stats_all.xlsx"
df = pd.read_excel(file_path, sheet_name='Sheet1')

team_players = get_top_players_for_teams(file_path)

# Aggregate stats for each team before adding new players
team_stats = df.groupby("Team").sum(numeric_only=True)

# Function to get player stats
def get_player_stats(player_name):
    return df[df["Player_Name"] == player_name].drop(columns=["Player_Name", "Team"]).sum(numeric_only=True)

# Calculate impact of adding players
impact_data = {}
average_impact = {}

for team, players in team_players.items():
    if team not in team_stats.index:
        continue  # Skip if the team is not in the original dataset
    
    original_stats = team_stats.loc[team]
    added_stats = sum([get_player_stats(player) for player in players], start=pd.Series(0, index=original_stats.index))

    new_stats = original_stats + added_stats
    percentage_change_per_stat = ((new_stats - original_stats) / original_stats) * 100  # Percentage change per stat

    # Calculate the average percentage change across all stats
    average_percentage_change = percentage_change_per_stat.mean()

    impact_data[team] = percentage_change_per_stat
    average_impact[team] = average_percentage_change

# Convert to DataFrame and display
impact_df = pd.DataFrame(impact_data).T
average_impact_df = pd.DataFrame.from_dict(average_impact, orient='index', columns=['Average Impact (%)'])





impact_df.to_csv("team_impact_analysis.csv", index=True)
average_impact_df.to_csv("overall_average_impact.csv", index=True)

print("Data saved to CSV files. Open them in Excel.")
