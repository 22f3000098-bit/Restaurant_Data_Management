# Visualization and analysis coverage

This file lists what the project generates versus the original notebook.

## Analysis (computed and/or exported)

| Notebook | Project | Where |
|----------|---------|--------|
| Combined sales DataFrame + preprocess | Yes | `data_loader.load_and_preprocess_sales()` |
| Category assignment (fuzzy + corrections) | Yes | `categorize.assign_and_correct_categories()` |
| Category value counts | Yes | Printed in `main` |
| Summary table (category × total/mean sales & qty, yearly) | Yes | `analysis.build_summary_table()` |
| Summary table as DOCX | Yes | `reports.save_summary_docx()` |
| Appetizer vs main course (sales) | Yes | `appetizer_vs_main_sales()` + plot |
| Appetizer vs main course (qty) | Yes | `appetizer_vs_main_qty()` + plot |
| Top 5 Appetizers / Main Courses by Sales | Yes | `top_items_by_sales()` + printed in `main` |
| Top 5 Appetizers / Main Courses by Qty | Yes | `top_items_by_qty()` + printed in `main` |
| Correlation (Qty vs Total Sales) | Yes | `qty_sales_correlation()` + plot + printed in `main` |
| Top N / bottom N by category (generic) | Yes | `top_items_by_qty()`, `bottom_items_by_qty()` + plots |
| `describe()` on combined_df | No | Can add `df.describe()` in `main` or use in a report if needed |

## Visualizations (plots saved to `output/`)

| Notebook | Project | Filename |
|----------|--------|----------|
| Total sales by year (bar) | Yes | `total_sales_by_year.png` |
| Sales proportion by category (pie) | Yes | `sales_by_category.png` |
| Appetizer vs main course sales (bar) | Yes | `appetizer_vs_main_sales.png` |
| Appetizer vs main course qty (bar) | Yes | `appetizer_vs_main_qty.png` |
| Appetizer vs main revenue contribution (pie) | Yes | `appetizer_vs_main_revenue_pie.png` |
| Top 10 alcoholic beverages (bar) | Yes | `top_alcoholic_qty.png` |
| Bottom 20 alcoholic beverages (bar) | Yes | `bottom_alcoholic_qty.png` |
| Top 10 Cocktails by qty | Yes | `top_qty_Cocktails.png` |
| Top 10 Mocktails by qty | Yes | `top_qty_Mocktails.png` |
| Top 10 Juices and Beverages by qty | Yes | `top_qty_Juices_and_Beverages.png` |
| Top 10 Global Appetizers Veg / Non-veg | Yes | `top_qty_Global_Appetizers_*.png` |
| Top 10 Global Main Course Veg / Non-veg | Yes | `top_qty_Global_Main_Course_*.png` |
| Top 10 Indian Appetizers Non-veg | Yes | `top_qty_Indian_Appetizers_Non-veg.png` |
| Correlation Qty vs Total Sales (scatter) | Yes | `correlation_qty_sales.png` |
| Monthly trend (line) for Food Veg/Non-veg | No | Notebook used "Food: Veg" categories; not in current menu. Can add if you introduce that mapping. |
| Chicken / Mutton / Seafood breakdown (non-veg) | No | Would need item-level rules or tags; can add as extra analysis if needed. |

## How to run everything

- **Full pipeline (all analyses + report + all plots):**  
  `python main.py`

- **Skip report or plots:**  
  `python main.py --no-report` or `python main.py --no-plots`

- **Add more category-specific top-N plots:**  
  In `visualization.run_all_visualizations()`, append to the list of categories passed to `plot_top_items_by_category()`.
