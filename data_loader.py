from __future__ import annotations

import pandas as pd

from config import get_file_paths
from constants import COL_ITEM, COL_MONTH, COL_SUB_CATEGORY, COL_YEAR, SUB_TOTAL_LABEL


def load_and_preprocess_sales() -> pd.DataFrame:
    file_paths = get_file_paths()
    if not file_paths:
        raise FileNotFoundError(
            "No sales Excel files found. Place files (e.g. Jan_2023.xlsx) in the data directory."
        )
    df_list = []
    for month_year, path in file_paths.items():
        df = pd.read_excel(path)
        if COL_MONTH not in df.columns:
            parts = month_year.split()
            df[COL_MONTH] = parts[0] if len(parts) >= 1 else ""
            df[COL_YEAR] = int(parts[1]) if len(parts) >= 2 else None
        df_list.append(df)
    combined_df = pd.concat(df_list, ignore_index=True)
    if COL_ITEM in combined_df.columns:
        combined_df[COL_ITEM] = combined_df[COL_ITEM].astype(str).str.strip().str.lower()
    if COL_SUB_CATEGORY in combined_df.columns:
        combined_df[COL_SUB_CATEGORY] = (
            combined_df[COL_SUB_CATEGORY].astype(str).str.strip().str.lower()
        )
        combined_df = combined_df[combined_df[COL_SUB_CATEGORY] != SUB_TOTAL_LABEL]
    if COL_ITEM in combined_df.columns:
        combined_df = combined_df[
            combined_df[COL_ITEM].notna() & (combined_df[COL_ITEM] != "")
        ]
    if COL_YEAR in combined_df.columns:
        combined_df[COL_YEAR] = (
            pd.to_numeric(combined_df[COL_YEAR], errors="coerce").fillna(0).astype(int)
        )
    return combined_df
