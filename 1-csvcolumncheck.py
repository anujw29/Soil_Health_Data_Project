import os
import pandas as pd

# Raw file's path. I also used this code after I removed the Block and Village column just to ensure if there is no error.
folder_path = r"C:\Users\anujw\OneDrive\Desktop\DATA INTERN ISB\Code\Downloads\Anuj\District_Merged_NoBlockVillage"

# Get a list of all CSV files in the folder
csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

if not csv_files:
    print("Empty folder. Nothing to check.")
else:
    # Read the first CSV file to get reference columns
    first_file = csv_files[0]
    reference_df = pd.read_csv(os.path.join(folder_path, first_file))
    reference_columns = set(reference_df.columns)
    print(f"Reference columns (from {first_file}): {list(reference_columns)}")

    # Initialize a flag to track if all files have the same columns
    columns_match = True
    column_diff = {}

    # Let's see if this one matches our baseline
    for csv_file in csv_files[1:]:
        df = pd.read_csv(os.path.join(folder_path, csv_file))
        current_columns = set(df.columns)
        
        # Check if columns match the reference
        if current_columns != reference_columns:
            columns_match = False
            # Find differences
            missing_columns = reference_columns - current_columns
            extra_columns = current_columns - reference_columns
            column_diff[csv_file] = {
                'missing_columns': missing_columns,
                'extra_columns': extra_columns
            }

    # Final results
    if columns_match:
        print("All CSV files have the same columns.")
    else:
        print("Some CSV files have different columns. Details:")
        for file, diff in column_diff.items():
            print(f"\nFile: {file}")
            if diff['missing_columns']:
                print(f"  Missing columns: {list(diff['missing_columns'])}")
            if diff['extra_columns']:
                print(f"  Extra columns: {list(diff['extra_columns'])}")
