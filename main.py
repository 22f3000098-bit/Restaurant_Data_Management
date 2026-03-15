from __future__ import annotations

import argparse
import sys

from config import get_file_paths
from data_loader import load_and_preprocess_sales
from menu import MENU
from categorize import assign_and_correct_categories
from analysis import (
    APPETIZER_CATEGORIES,
    MAIN_COURSE_CATEGORIES,
    build_summary_table,
    top_items_by_sales,
    top_items_by_qty,
    qty_sales_correlation,
)
from reports import save_summary_docx
from visualization import run_all_visualizations
from constants import COL_CATEGORY


def main() -> None:
    parser = argparse.ArgumentParser(description="BDM Sales analysis pipeline")
    parser.add_argument("--no-report", action="store_true", help="Skip generating the DOCX summary report")
    parser.add_argument("--no-plots", action="store_true", help="Skip generating plots")
    parser.add_argument("--verbose", action="store_true", help="Print category corrections during categorization")
    args = parser.parse_args()

    file_paths = get_file_paths()
    if not file_paths:
        print("No Excel files found in data directory. Add files (e.g. Jan_2023.xlsx) and try again.")
        sys.exit(1)

    print("Loading and preprocessing sales data...")
    df = load_and_preprocess_sales()
    print(f"Loaded {len(df)} rows.")

    print("Assigning categories (fuzzy match + corrections)...")
    df = assign_and_correct_categories(df, MENU, verbose=args.verbose)
    print("Category value counts:")
    print(df[COL_CATEGORY].value_counts().head(15))

    summary = build_summary_table(df)
    print("\nSummary table (first 5 rows):")
    print(summary.head())

    corr = qty_sales_correlation(df)
    print(f"\nCorrelation (Qty. vs Total Sales): {corr:.3f}")

    print("\nTop 5 Appetizers by Sales:")
    print(top_items_by_sales(df, APPETIZER_CATEGORIES, n=5))
    print("\nTop 5 Main Courses by Sales:")
    print(top_items_by_sales(df, MAIN_COURSE_CATEGORIES, n=5))
    print("\nTop 5 Appetizers by Qty:")
    print(top_items_by_qty(df, APPETIZER_CATEGORIES, n=5))
    print("\nTop 5 Main Courses by Qty:")
    print(top_items_by_qty(df, MAIN_COURSE_CATEGORIES, n=5))

    if not args.no_report:
        path = save_summary_docx(summary)
        print(f"\nReport saved: {path}")

    if not args.no_plots:
        run_all_visualizations(df)

    print("\nDone.")


if __name__ == "__main__":
    main()
