# This code removes 'Block' and 'Village' columns from all CSV files in a specified directory
# and saves the cleaned files in a new directory that are to be merged.

import pandas as pd
from pathlib import Path

input_dir = Path(
    r"C:\Users\anujw\OneDrive\Desktop\DATA INTERN ISB\Code\Downloads\Anuj\District_Merged"
)
output_dir = input_dir.parent / "District_Merged_NoBlockVillage"
output_dir.mkdir(exist_ok=True)

for file in input_dir.glob("*.csv"):
    df = pd.read_csv(file)
    df = df.drop(columns=[col for col in ["Block", "Village"] if col in df.columns])
    df.to_csv(output_dir / file.name, index=False)
