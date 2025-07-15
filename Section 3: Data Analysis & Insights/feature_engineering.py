# This code performs feature engineering and calculates things like nutrient percentages.
import pandas as pd
import numpy as np

# Nutrient groups
MACRO  = ["n", "p", "k", "OC"]          
MICRO  = ["Zn", "Fe", "Mn", "Cu", "B", "S"]   
PH_LV  = ["Alkaline", "Neutral", "Acidic"]   
EC_LV  = ["NonSaline", "Saline", "HighlySaline"] 

# This function calculates the percentage of a numerator over a denominator, handling division by zero
def _pct(num: pd.Series, denom: pd.Series) -> pd.Series:
    return np.where(denom == 0, np.nan, 100 * num / denom)


def add_features(df_raw: pd.DataFrame) -> pd.DataFrame:
    
    df = df_raw.copy()

    # Macro nutrients
    # Calculate percentages for High/Medium/Low counts
    for n in MACRO:
        cols = [f"{n}_{lvl}" for lvl in ("High", "Medium", "Low")]
        if all(c in df.columns for c in cols):
            total = df[cols].sum(axis=1)
            for lvl in ("High", "Medium", "Low"):
                df[f"{n}_{lvl}_pct"] = _pct(df[f"{n}_{lvl}"], total)
        else:
            print(f"[SKIP] {n.upper()} counts missing -> {cols}")

    # Micro nutrients
    for n in MICRO:
        # So this is basically checking if the columns for sufficient and deficient nutrients exist(not needed but, when I was taking some suggestions from ChatGPT it suggested me this)
        pairs = [
            (f"{n}_Suff", f"{n}_Def"),
            (f"{n}_Sufficient", f"{n}_Deficient"),
        ]
        for suff_col, def_col in pairs:
            if suff_col in df.columns and def_col in df.columns:
                total = df[suff_col] + df[def_col]
                df[f"{n}_Suff_pct"] = _pct(df[suff_col], total)
                df[f"{n}_Def_pct"]  = _pct(df[def_col],  total)
                break   # stop at first matching pair

    # This is optional, but if pH and EC levels are present, calculate their percentages, I did it so that they can be included in the final report later
    if all(f"pH_{lvl}" in df.columns for lvl in PH_LV):
        total = df[[f"pH_{lvl}" for lvl in PH_LV]].sum(axis=1)
        for lvl in PH_LV:
            df[f"pH_{lvl}_pct"] = _pct(df[f"pH_{lvl}"], total)

    if all(f"EC_{lvl}" in df.columns for lvl in EC_LV):
        total = df[[f"EC_{lvl}" for lvl in EC_LV]].sum(axis=1)
        for lvl in EC_LV:
            df[f"EC_{lvl}_pct"] = _pct(df[f"EC_{lvl}"], total)

    return df
