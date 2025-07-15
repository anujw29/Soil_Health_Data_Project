
import os
import json
import shutil
import re
from typing import Dict, List

#basic config
source_dir = r"C:\Users\anujw\OneDrive\Desktop\DATA INTERN ISB\Code\Downloads\Anuj\CSVs"
output_dir = r"C:\Users\anujw\OneDrive\Desktop\DATA INTERN ISB\Code\Downloads\Anuj\shlok"
json_path = r"C:\Users\anujw\OneDrive\Desktop\DATA INTERN ISB\Code\state_district_data.json"
log_path = os.path.join(output_dir, "unmatched_files.txt")
# This code organises CSV files into a State / District folder tree as given in the assignment description.

# Currently, file names look like in this format --> StateNameDistrictNameBlockName_number.csv and some use any mixture of upper/lowercase letters.

# So this code does the following
#   1) loads state‑district names from state_district_data.json
#   2) matches names case‑insensitively
#   3) builds output_folder/STATE/DISTRICT/
#   4) moves each CSV there
#   5) logs unmatched files



csv_folder = r"C:\Users\anujw\OneDrive\Desktop\DATA INTERN ISB\Code\Downloads\Anuj\CSVs"               # folder with raw CSVs
output_folder = r"C:\Users\anujw\OneDrive\Desktop\DATA INTERN ISB\Code\Downloads\Anuj\shlok"           # destination root(Shlok is my brother's name and I thought it would be a good name for the folder😅)
json_path  = r"C:\Users\anujw\OneDrive\Desktop\DATA INTERN ISB\Code\state_district_data.json"
unmatched_logpath   = os.path.join(output_folder, "unmatched_files.txt")

# Normalise text for easy matching
def normalise(text: str) -> str:
    text = text.upper()
    text = text.replace("&", "AND")
    text = re.sub(r"[^A-Z0-9]", "_", text)
    text = re.sub(r"__+", "_", text).strip("_")
    return text

#For loading state-district mapping from JSON
def load_state_district_map(json_file: str) -> Dict[str, List[str]]:
    with open(json_file, "r", encoding="utf-8") as fh:
        raw = json.load(fh)

    out: Dict[str, List[str]] = {}
    for state, districts in raw.items():
        n_state = normalise(state)
        out[n_state] = [normalise(d) for d in districts]
    return out

# For creating output folder if it doesn't exist
def make_folder_if_needed(path: str) -> None:
    os.makedirs(path, exist_ok=True)

# Remove trailing digits from filename as it had no significance for this task
def remove_number_tail(name: str) -> str:
    return re.sub(r"_\d+$", "", name)


# Main code for organising files
def organise_files() -> None:
    state_map = load_state_district_map(json_path)

    unmatched: List[str] = []
    matched_count = 0
    total_csv = 0

    make_folder_if_needed(output_folder)

    for fname in os.listdir(csv_folder):
        if not fname.lower().endswith(".csv"):
            continue

        total_csv += 1

        # Remove extension and trailing number
        root = fname[:-4]
        root = remove_number_tail(root)

        # Looking for an uppercase version for matching
        root_upper = root.upper()

        matched = False

        for norm_state, districts in state_map.items():
            if root_upper.startswith(norm_state):
                remainder_u = root_upper[len(norm_state):]

                for norm_district in districts:
                    if remainder_u.startswith(norm_district):
                        # Block is whatever remains in the original‑case root
                        block_part = root[len(norm_state) + len(norm_district):]
                        if not block_part:
                            unmatched.append(fname)
                            print(f"[SKIP] No block part in: {fname}") #This is to skip files that don't have a block part
                            matched = True
                            break

                        # Folders
                        state_dir    = os.path.join(output_folder, norm_state)
                        district_dir = os.path.join(state_dir, norm_district)
                        make_folder_if_needed(district_dir)

                        # Move file
                        src  = os.path.join(csv_folder, fname)
                        dest = os.path.join(district_dir, fname)
                        try:
                            shutil.move(src, dest)
                            print(f"[OK] {fname}  ->  {norm_state}/{norm_district}/")
                            matched_count += 1
                        except Exception as exc:
                            unmatched.append(fname)
                            print(f"[ERROR] Could not move {fname}: {exc}")

                        matched = True
                        break
                break  # state loop

        if not matched:
            unmatched.append(fname)
            print(f"[WARN] No match for: {fname}") # This is to log files that didn't match any state/district
            
   # Final summary
    print("\nSummary")
   
    print(f"Total CSV files examined : {total_csv}")
    print(f"Successfully organised   : {matched_count}")
    print(f"Unmatched / errors       : {len(unmatched)}")

    if unmatched:
        make_folder_if_needed(os.path.dirname(unmatched_logpath))
        with open(unmatched_logpath, "w", encoding="utf-8") as logf:
            logf.write("Unmatched or errored files:\n")
            for bad in unmatched:
                logf.write(f"{bad}\n")
        print(f"\nList of unmatched files written to:\n {unmatched_logpath}")
    else:
        print("\nAll files matched successfully.")


if __name__ == "__main__":
    organise_files()
