# THis code removes outliers within each group and I came to the 12% threshold after some trial and error. As I have tweaked with the quartile values, now it gives me almost 90% of original data)
import pandas as pd


# Default columns to use for outlier filtering
DEFAULT_KEY_COLUMNS = [ "n_Low", "p_Low", "k_Low", "OC_Low",
    "Fe_Deficient", "Zn_Deficient", "Mn_Deficient",
    "Cu_Deficient", "B_Deficient", "S_Deficient"]


def trim_by_percentile(group: pd.DataFrame, cols: list[str], low_q=0.01, high_q=0.99):
    """
    For each numeric column, remove rows outside the [low_q, high_q] range.
    The final mask keeps only rows inside range for all columns.
    """
    keep_mask = pd.Series(True, index=group.index)

    for col in cols:
        lower = group[col].quantile(low_q)
        upper = group[col].quantile(high_q)
        col_mask = group[col].between(lower, upper, inclusive="both")
        keep_mask &= col_mask

    trimmed_group = group[keep_mask]

    if len(group) > 0:
        dropped_pct = (len(group) - len(trimmed_group)) / len(group) * 100
        print(f"   Trimmed {group.name:<25} -> kept {len(trimmed_group):>4} rows "
              f"({dropped_pct:4.1f}% dropped)")
    return trimmed_group


def filter_outliers_by_group(
    df: pd.DataFrame,
    group_col: str,
    key_cols: list[str] = None,
    max_drop_frac: float = 0.12
) -> pd.DataFrame:
    """
    Applies group-wise outlier filtering on selected columns.
    Ensures that no more than `max_drop_frac` of total rows are dropped.
    """

    print(f"> Removing outliers grouped by '{group_col}' …")

    if key_cols is None:
        key_cols = DEFAULT_KEY_COLUMNS

    original_len = len(df)

    # Group-wise trimming
    cleaned_df = (
        df.groupby(group_col, group_keys=False)
        .apply(trim_by_percentile, cols=key_cols)
        .reset_index(drop=True)
    )

    new_len = len(cleaned_df)
    fraction_removed = (original_len - new_len) / original_len

    if fraction_removed > max_drop_frac:
        raise ValueError(
            f"Outlier filtering removed {fraction_removed:.2%} (>10%). "
            f"Try using fewer or less variable columns for filtering."
        )

    print(f"   Final rows after trimming: {new_len:,} "
          f"({(new_len/original_len):.2%} of original)")

    return cleaned_df
