from __future__ import annotations

import argparse
import sys

from config import DATA_DIR, OUTPUT_DIR, get_file_paths
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
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Output folder: {OUTPUT_DIR.resolve()}\n")

    parser = argparse.ArgumentParser(description="BDM Sales analysis pipeline")
    parser.add_argument("--no-report", action="store_true", help="Skip generating the DOCX summary report")
    parser.add_argument("--no-plots", action="store_true", help="Skip generating plots")
    parser.add_argument("--verbose", action="store_true", help="Print category corrections during categorization")
    args = parser.parse_args()

    file_paths = get_file_paths()
    if not file_paths:
        print(f"No Excel files found. Looked in: {DATA_DIR.resolve()}")
        print("Add files (e.g. Jan_2023.xlsx) there, or edit DATA_DIR in config.py if they are elsewhere.")
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
        print(f"\nReport saved: {path.resolve()}")

    if not args.no_plots:
        run_all_visualizations(df)

    if list(OUTPUT_DIR.iterdir()):
        print("\nOutput files:")
        for f in sorted(OUTPUT_DIR.iterdir()):
            print(f"  {f.name}")
    print("\nDone.")


if __name__ == "__main__":
    main()
