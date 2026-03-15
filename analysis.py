from __future__ import annotations

import pandas as pd

from constants import (
    COL_CATEGORY,
    COL_ITEM,
    COL_QTY,
    COL_TOTAL,
    COL_YEAR,
    REQUIRED_COLUMNS_FOR_ANALYSIS,
)

APPETIZER_CATEGORIES = [
    "Global Appetizers Veg",
    "Global Appetizers Non-veg",
    "Indian Appetizers Veg",
    "Indian Appetizers Non-veg",
    "Side Dishes",
]
MAIN_COURSE_CATEGORIES = [
    "Global Main Course Veg",
    "Global Main Course Non-veg",
    "Indian Main Course Veg",
    "Indian Main Course Non-veg",
    "Sizzlers Veg",
    "Sizzlers Non-veg",
    "Pasta Veg",
    "Pasta Non-veg",
    "Pizza Veg",
    "Pizza Non-veg",
    "Indian Breads and Rice",
    "Biryani Veg",
    "Biryani Non-veg",
]


def build_summary_table(df: pd.DataFrame, years: list[int] | None = None) -> pd.DataFrame:
    if years is None:
        years = [2023, 2024]
    missing = [c for c in REQUIRED_COLUMNS_FOR_ANALYSIS if c not in df.columns]
    if missing:
        raise ValueError(f"DataFrame missing required columns: {missing}")
    work = df.copy()
    if COL_YEAR in work.columns:
        work = work[work[COL_YEAR].astype(int).isin(years)]
    summary = work.groupby(COL_CATEGORY).agg(
        Total_Sales=(COL_TOTAL, "sum"),
        Mean_Sales=(COL_TOTAL, "mean"),
        Total_Qty=(COL_QTY, "sum"),
        Mean_Qty=(COL_QTY, "mean"),
    ).reset_index()
    yearly = work.groupby([COL_CATEGORY, COL_YEAR])[[COL_TOTAL, COL_QTY]].sum().unstack()
    yearly.columns = [f"{col[0]}_{col[1]}" for col in yearly.columns]
    yearly = yearly.reset_index()
    return pd.merge(summary, yearly, on=COL_CATEGORY, how="left")


def appetizer_vs_main_sales(df: pd.DataFrame) -> tuple[float, float]:
    app_sales = df[df[COL_CATEGORY].isin(APPETIZER_CATEGORIES)][COL_TOTAL].sum()
    main_sales = df[df[COL_CATEGORY].isin(MAIN_COURSE_CATEGORIES)][COL_TOTAL].sum()
    return app_sales, main_sales


def top_items_by_sales(df: pd.DataFrame, category_list: list[str], n: int = 5) -> pd.Series:
    subset = df[df[COL_CATEGORY].isin(category_list)]
    return subset.groupby(COL_ITEM)[COL_TOTAL].sum().nlargest(n)


def top_items_by_qty(df: pd.DataFrame, category_list: list[str], n: int = 5) -> pd.Series:
    subset = df[df[COL_CATEGORY].isin(category_list)]
    return subset.groupby(COL_ITEM)[COL_QTY].sum().nlargest(n)


def bottom_items_by_qty(df: pd.DataFrame, category: str, n: int = 20) -> pd.Series:
    subset = df[df[COL_CATEGORY] == category]
    if subset.empty:
        return pd.Series(dtype=float)
    return subset.groupby(COL_ITEM)[COL_QTY].sum().nsmallest(n)


def appetizer_vs_main_qty(df: pd.DataFrame) -> tuple[float, float]:
    app_qty = df[df[COL_CATEGORY].isin(APPETIZER_CATEGORIES)][COL_QTY].sum()
    main_qty = df[df[COL_CATEGORY].isin(MAIN_COURSE_CATEGORIES)][COL_QTY].sum()
    return app_qty, main_qty


def qty_sales_correlation(df: pd.DataFrame) -> float:
    return df[COL_QTY].corr(df[COL_TOTAL])
