# To combine all district CSVs into a single master dataset
# This code will read all CSV files from the yhe input folder, combine them, and saves the result

import pandas as pd
from pathlib import Path

# Set input directory
input_folder = Path(r"C:\Users\anujw\OneDrive\Desktop\DATA INTERN ISB\Code\Downloads\Anuj\District_Merged_NoBlockVillage")
output_folder = Path("soil_health_master.csv")
output_pkl = Path("soil_health_master.pkl") #Using pickle format for faster loading(one of my senior's suggested this)

# Combine all CSVs
master_df = pd.DataFrame()

for file in input_folder.glob("*.csv"):
    df = pd.read_csv(file)
    df["source_file"] = file.name  # Added this just in case we need to trace back agar kabhi jarurat padti hai
    master_df = pd.concat([master_df, df], ignore_index=True)

# Save to both formats
master_df.to_csv(output_folder, index=False)
master_df.to_pickle(output_pkl)

print("Combined master dataset shape:", master_df.shape)
print("Saved as:", output_folder, "and", output_pkl)
