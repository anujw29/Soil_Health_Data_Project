# This is the main code that does EDA and generates reports.
# It loads the soil health data, processes it, generates summary tables.

from pathlib import Path

from load_data import load_soil_data
from outlier_filter import filter_outliers_by_group
from feature_engineering import add_features
from generate_tables import save_summary_tables
from generate_plots import make_plots
from generate_rankings import generate_top10_state_rankings
from generate_report_txt import write_txt_report

input_csv_path = r"C:\Users\anujw\OneDrive\Desktop\DATA INTERN ISB\Code\Downloads\Anuj\soil_health_master.csv"

def main() -> None:
    print("\nSTEP 1  Loading merged CSV")
    df_raw = load_soil_data(input_csv_path)

    print("\nSTEP 2  Outlier trimming")
    df_clean = filter_outliers_by_group(df_raw, group_col="District")

    Path("data_work").mkdir(exist_ok=True)
    df_clean.to_parquet("data_work/district_clean.parquet", index=False)
    
    print("\nSTEP 3  Feature engineering")
    df_feat = add_features(df_clean)

    print("\nSTEP 4  Writing summary CSVs")
    save_summary_tables(df_feat, output_folder="reports/tables")

    print("\nSTEP 5  Generating plots (standard + stacked)")
    make_plots(df_feat, out_dir="reports/plots")

    # Generate state-level rankings
    # This will create a CSV with top 10 districts per state based on the feature values
    print("\nSTEP 6  Generating Top 10 state-level rankings (macro + micro)")
    generate_top10_state_rankings(df_feat, out_dir="reports/plots/state_rankings")

    print("\nSTEP 7  Writing plain-text report")
    write_txt_report(df_feat, out_path="reports/report.txt")

    print("\n Pipeline complete — check the 'reports' folder.\n")

if __name__ == "__main__":
    main()
