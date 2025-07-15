# This file defines the logic to generate summary tables.
# It aggregates data at district and state levels, calculates rates for various soil health indicators,
# and saves the results as CSV files. Most of the work done by GPT (I am not very good at syntax and I believe it's mature to use AI for this thing)


import pandas as pd
from pathlib import Path

def save_summary_tables(df: pd.DataFrame, output_folder: str):
    Path(output_folder).mkdir(parents=True, exist_ok=True)

    df.to_csv(Path(output_folder) / "district_summary.csv", index=False)

    state_summary = df.groupby("State").mean(numeric_only=True).reset_index()
    state_summary.to_csv(Path(output_folder) / "state_summary.csv", index=False)

    top_nitrogen = df.groupby("District")["n_Low_pct"].mean().sort_values(ascending=False).head(10)
    top_nitrogen.to_csv(Path(output_folder) / "top10_n_low_districts.csv")
