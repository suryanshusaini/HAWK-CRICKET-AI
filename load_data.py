import os
import yaml
import pandas as pd

# --- Configuration ---
DATA_FOLDER = 'data'

# --- Main Script ---
try:
    all_files = [f for f in os.listdir(DATA_FOLDER) if f.endswith('.yaml')]
    print(f"Found {len(all_files)} match files to process.")
except FileNotFoundError:
    print(f"Error: The folder '{DATA_FOLDER}' was not found.")
    exit()

all_deliveries_data = []

for i, filename in enumerate(all_files):
    match_id = os.path.splitext(filename)[0]
    if (i + 1) % 100 == 0:  # Print progress every 100 files
        print(f"Processing file {i+1}/{len(all_files)}: {filename}")

    try:
        with open(os.path.join(DATA_FOLDER, filename), 'r') as f:
            data = yaml.safe_load(f)

        if 'innings' not in data:
            continue

        for innings_item in data.get('innings', []):
            innings_name = list(innings_item.keys())[0]
            innings_details = innings_item[innings_name]
            team_batting = innings_details.get('team')
            
            deliveries_data = innings_details.get('deliveries', [])

            # --- FINAL ROBUST LOGIC ---
            # This handles BOTH list and dictionary formats for the deliveries.
            deliveries_to_process = []
            if isinstance(deliveries_data, list):
                for item in deliveries_data:
                    if isinstance(item, dict):
                        deliveries_to_process.extend(item.items())
            elif isinstance(deliveries_data, dict):
                deliveries_to_process = deliveries_data.items()
            # --- END OF FIX ---

            for over, ball_details in deliveries_to_process:
                batsman = ball_details.get('batsman')
                bowler = ball_details.get('bowler')
                runs = ball_details.get('runs', {}).get('batsman', 0)
                total_runs = ball_details.get('runs', {}).get('total', 0)
                
                wicket_info = ball_details.get('wicket')
                if wicket_info:
                    is_wicket = 1
                    player_out = wicket_info.get('player_out')
                    kind_of_wicket = wicket_info.get('kind')
                else:
                    is_wicket = 0
                    player_out = None
                    kind_of_wicket = None

                all_deliveries_data.append({
                    'match_id': match_id,
                    'batting_team': team_batting,
                    'over': over,
                    'batsman': batsman,
                    'bowler': bowler,
                    'runs_scored': runs,
                    'total_runs_on_ball': total_runs,
                    'is_wicket': is_wicket,
                    'player_out': player_out,
                    'kind_of_wicket': kind_of_wicket
                })

    except Exception as e:
        print(f"  - Skipped file {filename} due to error: {e}")

df = pd.DataFrame(all_deliveries_data)

print("\n--- Data Processing Complete ---")
print(f"Successfully created a DataFrame with {len(df)} rows and {len(df.columns)} columns.")
if not df.empty:
    print("\nFirst 5 rows of the new dataset:")
    print(df.head())

output_csv_path = 'all_matches_deliveries.csv'
df.to_csv(output_csv_path, index=False)
print(f"\nDataFrame saved to '{output_csv_path}'")
