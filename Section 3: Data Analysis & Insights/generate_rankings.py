# This code generates top 10 state rankings for macro and micro nutrients
#Most of the syntax in this code is AI generated.

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from pathlib import Path

sns.set_style("whitegrid")
plt.rcParams.update({"font.size": 10})

MACRO  = ["n", "p", "k", "OC"]
MICRO  = ["Fe", "Zn", "Mn", "Cu", "B", "S"]

def _plot(df_top, x_col, y_col, title, save_path):
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(data=df_top, x=x_col, y=y_col, palette="viridis", ax=ax)
    ax.set_title(title, fontsize=13)
    ax.set_xlabel(x_col.replace("_", " ").replace("pct", "%"))
    ax.set_ylabel("")
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:.1f}%"))
    ax.grid(True, axis='x', linestyle='--', alpha=0.4)
    plt.tight_layout()
    fig.savefig(save_path, dpi=300)
    plt.close(fig)
# This function generates top 10 state rankings for macro and micro nutrients
# It creates bar plots and saves them along with CSV files containing the rankings.
def generate_top10_state_rankings(df: pd.DataFrame, out_dir: str) -> None:
    out_dir   = Path(out_dir)
    plots_dir = out_dir
    csv_dir   = Path(str(out_dir).replace("plots", "tables"))
    plots_dir.mkdir(parents=True, exist_ok=True)
    csv_dir.mkdir(parents=True,  exist_ok=True)

    state_avg = df.groupby("State").mean(numeric_only=True).reset_index()

    # This is for Macro nutrients
    for n in MACRO:
        for level in ("High", "Low"):
            col = f"{n}_{level}_pct"
            if col not in state_avg.columns:
                continue
            top10 = state_avg.sort_values(col, ascending=False).head(10)
            fname = f"{n}_{level}".lower()
            _plot(
                top10, col, "State",
                title=f"Top 10 States by {n.upper()} {level} %",
                save_path=plots_dir / f"{fname}.png"
            )
            top10[["State", col]].to_csv(csv_dir / f"{fname}.csv", index=False)

    # This is for Micro nutrients
    for n in MICRO:
        for label in ("Suff", "Def"):
            col = f"{n}_{label}_pct"
            if col not in state_avg.columns:
                continue
            top10 = state_avg.sort_values(col, ascending=False).head(10)
            fname = f"{n}_{label}".lower()
            nice_label = "Sufficient" if label == "Suff" else "Deficient"
            _plot(
                top10, col, "State",
                title=f"Top 10 States by {nice_label} {n.upper()} %",
                save_path=plots_dir / f"{fname}.png"
            )
            top10[["State", col]].to_csv(csv_dir / f"{fname}.csv", index=False)
