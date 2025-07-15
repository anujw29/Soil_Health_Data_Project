# I gave the feature engg code to GPT and asked to generate this code as it was pretty syntax oriented and no logic involved. So, this is not my original code.

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

def make_plots(df: pd.DataFrame, out_dir: str) -> None:
    Path(out_dir).mkdir(parents=True, exist_ok=True)

    macro = ['n', 'p', 'k', 'OC']
    micro = ['Zn', 'Fe', 'Mn', 'Cu', 'S', 'B']

    df_grouped = df.groupby("State").mean(numeric_only=True).reset_index()

    for n in macro:
        for level in ['Low', 'Medium', 'High']:
            col = f"{n}_{level}_pct"
            if col in df_grouped.columns:
                plt.figure(figsize=(12, 6))
                sns.barplot(data=df_grouped, y="State", x=col, palette="viridis")
                plt.title(f"{n.upper()} - {level} % by State")
                plt.tight_layout()
                plt.savefig(Path(out_dir) / f"{n}_{level}.png")
                plt.close()

    for n in micro:
        for typ in ['Suff_pct', 'Def_pct']:
            col = f"{n}_{typ}"
            if col in df_grouped.columns:
                plt.figure(figsize=(12, 6))
                sns.barplot(data=df_grouped, y="State", x=col, palette="magma")
                plt.title(f"{n.upper()} - {typ.replace('_', ' ')} by State")
                plt.tight_layout()
                plt.savefig(Path(out_dir) / f"{n}_{typ}.png")
                plt.close()
