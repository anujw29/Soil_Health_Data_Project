# To combine district CSVs into a single file per district(I did this as I wanted to ensure that the code for combining works good and would not cause any futher errors)

import os
import pandas as pd

# Basic config
input_folder = r"C:\Users\anujw\OneDrive\Desktop\DATA INTERN ISB\Code\Downloads\Anuj\shlok"
output_folder  = r"C:\Users\anujw\OneDrive\Desktop\DATA INTERN ISB\Code\Downloads\Anuj\District_Merged"

os.makedirs(output_folder, exist_ok=True)        # create output folder if it doesn't exist

# This is to replace spaces and slashes with underscores to avoid path issues
def safe_name(name: str) -> str:
    return name.replace(" ", "_").replace("/", "_")

# Main code
for state in os.listdir(input_folder):
    state_path = os.path.join(input_folder, state)
    if not os.path.isdir(state_path):
        continue                            # Ignore files as we only want folders (states)

    for district in os.listdir(state_path):
        dist_path = os.path.join(state_path, district)
        if not os.path.isdir(dist_path):
            continue                        # Again, ignoring non-folder items inside state folders

        district_df = pd.DataFrame()

        # Read all CSV files for this district (we won’t modify them obviously)
        for fname in os.listdir(dist_path):
            if not fname.lower().endswith(".csv"):
                continue
            fpath = os.path.join(dist_path, fname)
            try:
                block_df = pd.read_csv(fpath)           
                block_df["State"]    = state
                block_df["District"] = district
                block_df["Block"]    = os.path.splitext(fname)[0]
                district_df = pd.concat([district_df, block_df], ignore_index=True)
            except Exception as e:
                print(f"Could not read {fpath}: {e}")

        # Save combined data for this district into one CSV
        if not district_df.empty:
            out_file = os.path.join(
                output_folder,
                f"{safe_name(state)}_{safe_name(district)}.csv"
            )
            district_df.to_csv(out_file, index=False)
            print(f"Created {out_file}  ({len(district_df):,} rows)")
        else:
            print(f"No CSVs found in {state}\\{district}")

print(" District consolidation finished.")
