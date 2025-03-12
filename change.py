import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from run import *

# Load player statistics
file_path = "player_stats_all.xlsx"
df = pd.read_excel(file_path, sheet_name='Sheet1')

team_players = get_top_players_for_teams(file_path)

# Aggregate stats for each team before adding new players
team_stats = df.groupby("Team").sum(numeric_only=True)

# Function to get player stats
def get_player_stats(player_name):
    player_stats = df[df["Player_Name"] == player_name].drop(columns=["Player_Name", "Team"])
    player_stats = player_stats.sum(numeric_only=True)
    
    # Ensure all expected columns exist and missing ones are filled with 0
    return player_stats.reindex(team_stats.columns, fill_value=0)

# Calculate impact of adding players
impact_data = {}
average_impact = {}

for team, players in team_players.items():
    if team not in team_stats.index:
        continue  # Skip if the team is not in the original dataset
    
    original_stats = team_stats.loc[team]
    added_stats = sum([get_player_stats(player) for player in players], start=pd.Series(0, index=original_stats.index))

    new_stats = original_stats + added_stats
    percentage_change_per_stat = ((new_stats - original_stats) / original_stats.replace(0, np.nan)) * 100  
    percentage_change_per_stat.fillna(0, inplace=True)  # Convert NaN back to 0

    # Calculate the average percentage change across all stats
    average_percentage_change = percentage_change_per_stat.mean()

    impact_data[team] = percentage_change_per_stat
    average_impact[team] = average_percentage_change

# Convert to DataFrame and save results
impact_df = pd.DataFrame(impact_data).T
average_impact_df = pd.DataFrame.from_dict(average_impact, orient='index', columns=['Average Impact (%)'])

impact_df.to_csv("team_impact_analysis.csv", index=True)
average_impact_df.to_csv("overall_average_impact.csv", index=True)

# Filter for only the specified teams
selected_teams = ["MIL", "CLE", "BRK", "ATL", "MIN", "LAC", "SAC", "MEM"]
filtered_impact_df = impact_df.loc[selected_teams]
filtered_avg_impact_df = average_impact_df.loc[selected_teams]

# Plot impact per stat for the selected teams
plt.figure(figsize=(12, 6))
filtered_impact_df.plot(kind="bar", figsize=(14, 6), alpha=0.75, width=0.8)
plt.title("Percentage Impact on Team Stats After Adding New Players")
plt.ylabel("Percentage Change (%)")
plt.xlabel("Teams")
plt.xticks(rotation=45)
plt.legend(title="Stats", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(axis="y", linestyle="--", alpha=0.6)
plt.show()

# Plot average impact for the selected teams
plt.figure(figsize=(10, 5))
filtered_avg_impact_df.sort_values(by="Average Impact (%)", ascending=False).plot(kind="bar", legend=False, color='b', alpha=0.75)
plt.title("Average Impact Percentage on Team Performance")
plt.ylabel("Average Percentage Change (%)")
plt.xlabel("Teams")
plt.xticks(rotation=45)
plt.grid(axis="y", linestyle="--", alpha=0.6)
plt.show()

# Display the filtered impact DataFrame in a user-friendly way
print("\nFiltered Impact Analysis:")
print(filtered_impact_df)

print("\nData saved to CSV files. Open them in Excel.")
