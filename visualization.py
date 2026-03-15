from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from config import OUTPUT_DIR
from analysis import APPETIZER_CATEGORIES, MAIN_COURSE_CATEGORIES
from constants import COL_CATEGORY, COL_ITEM, COL_QTY, COL_TOTAL, COL_YEAR


def _save(fig: plt.Figure, name: str) -> None:
    out = Path(OUTPUT_DIR)
    out.mkdir(parents=True, exist_ok=True)
    fig.savefig(out / name, bbox_inches="tight")
    plt.close(fig)


def plot_sales_by_year(df: pd.DataFrame) -> None:
    sales = df.groupby(COL_YEAR)[COL_TOTAL].sum().sort_index()
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x=sales.index.astype(str), y=sales.values, ax=ax)
    for p in ax.patches:
        ax.text(p.get_x() + p.get_width() / 2.0, p.get_height(), f"₹{p.get_height():.0f}", ha="center", va="bottom")
    ax.set_xlabel("Year")
    ax.set_ylabel("Total Sales")
    ax.set_title("Total Sales by Year")
    _save(fig, "total_sales_by_year.png")


def plot_sales_by_category_pie(df: pd.DataFrame) -> None:
    sales = df.groupby(COL_CATEGORY)[COL_TOTAL].sum()
    fig, ax = plt.subplots(figsize=(10, 8))
    sales.plot(kind="pie", ax=ax, autopct="%1.1f%%", startangle=90)
    ax.set_ylabel("")
    ax.set_title("Sales Proportion by Category")
    _save(fig, "sales_by_category.png")


def plot_appetizer_vs_main_sales(df: pd.DataFrame) -> None:
    app_sales = df[df[COL_CATEGORY].isin(APPETIZER_CATEGORIES)][COL_TOTAL].sum()
    main_sales = df[df[COL_CATEGORY].isin(MAIN_COURSE_CATEGORIES)][COL_TOTAL].sum()
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.bar(["Appetizers", "Main Courses"], [app_sales, main_sales], color=["skyblue", "lightcoral"])
    ax.set_ylabel("Total Sales (₹)")
    ax.set_title("Appetizer vs Main Course Sales")
    _save(fig, "appetizer_vs_main_sales.png")


def plot_appetizer_vs_main_qty(df: pd.DataFrame) -> None:
    from analysis import appetizer_vs_main_qty
    app_qty, main_qty = appetizer_vs_main_qty(df)
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.bar(["Appetizers", "Main Courses"], [app_qty, main_qty], color=["skyblue", "lightcoral"])
    ax.set_ylabel("Total Qty")
    ax.set_title("Appetizer vs Main Course Quantity")
    _save(fig, "appetizer_vs_main_qty.png")


def plot_appetizer_vs_main_revenue_pie(df: pd.DataFrame) -> None:
    app_sales = df[df[COL_CATEGORY].isin(APPETIZER_CATEGORIES)][COL_TOTAL].sum()
    main_sales = df[df[COL_CATEGORY].isin(MAIN_COURSE_CATEGORIES)][COL_TOTAL].sum()
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.pie(
        [app_sales, main_sales],
        labels=["Appetizers", "Main Courses"],
        colors=["skyblue", "lightcoral"],
        autopct="%1.1f%%",
        startangle=90,
    )
    ax.set_title("Contribution of Appetizers vs Main Courses to Overall Revenue")
    ax.axis("equal")
    _save(fig, "appetizer_vs_main_revenue_pie.png")


def plot_top_alcoholic_qty(df: pd.DataFrame, n: int = 10) -> None:
    subset = df[df[COL_CATEGORY] == "Alcoholic Beverages"]
    if subset.empty:
        return
    top = subset.groupby(COL_ITEM)[COL_QTY].sum().nlargest(n)
    fig, ax = plt.subplots(figsize=(12, 6))
    top.plot(kind="bar", ax=ax, color="gold")
    ax.set_title(f"Top {n} Most Consumed Alcoholic Beverages")
    ax.set_xlabel("Item")
    ax.set_ylabel("Quantity")
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha="right")
    _save(fig, "top_alcoholic_qty.png")


def plot_bottom_alcoholic_qty(df: pd.DataFrame, n: int = 20) -> None:
    subset = df[df[COL_CATEGORY] == "Alcoholic Beverages"]
    if subset.empty:
        return
    bottom = subset.groupby(COL_ITEM)[COL_QTY].sum().nsmallest(n)
    fig, ax = plt.subplots(figsize=(12, 6))
    bottom.plot(kind="bar", ax=ax)
    ax.set_title(f"Bottom {n} Least Consumed Alcoholic Beverages")
    ax.set_xlabel("Item")
    ax.set_ylabel("Quantity")
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha="right")
    _save(fig, "bottom_alcoholic_qty.png")


def plot_top_items_by_category(df: pd.DataFrame, category: str, n: int = 10) -> None:
    subset = df[df[COL_CATEGORY] == category]
    if subset.empty:
        return
    top = subset.groupby(COL_ITEM)[COL_QTY].sum().nlargest(n)
    fig, ax = plt.subplots(figsize=(12, 6))
    top.plot(kind="bar", ax=ax)
    ax.set_title(f"Top {n} Most Consumed in {category}")
    ax.set_xlabel("Item")
    ax.set_ylabel("Quantity")
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha="right")
    safe = category.replace(" ", "_").replace("/", "_")
    _save(fig, f"top_qty_{safe}.png")


def plot_correlation_qty_sales(df: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(df[COL_QTY], df[COL_TOTAL], alpha=0.3)
    ax.set_xlabel("Quantity")
    ax.set_ylabel("Total Sales (₹)")
    ax.set_title("Correlation between Quantity and Total Sales")
    _save(fig, "correlation_qty_sales.png")


def run_all_visualizations(df: pd.DataFrame) -> None:
    plot_sales_by_year(df)
    plot_sales_by_category_pie(df)
    plot_appetizer_vs_main_sales(df)
    plot_appetizer_vs_main_qty(df)
    plot_appetizer_vs_main_revenue_pie(df)
    plot_top_alcoholic_qty(df, n=10)
    plot_bottom_alcoholic_qty(df, n=20)
    plot_correlation_qty_sales(df)
    for category in ["Cocktails", "Mocktails", "Juices and Beverages"]:
        plot_top_items_by_category(df, category, n=10)
    for category in [
        "Global Appetizers Veg",
        "Global Appetizers Non-veg",
        "Global Main Course Veg",
        "Global Main Course Non-veg",
        "Indian Appetizers Non-veg",
    ]:
        plot_top_items_by_category(df, category, n=10)
    print(f"Plots saved to {OUTPUT_DIR}")
