# From your mind to your plate: Exploring consumption behaviour of food and beverage in a casual dining restaurant

**BDM Capstone · IIT Madras Online BS Degree**

This repository contains the analysis pipeline and visualisations for a study of two years of sales data (Jan 2023–Dec 2024) from a casual dining restaurant under **XYZ Hospitality** (XYZ Bistro and Bar / XYZ Lounge). The goal is to uncover item-level performance, ordering patterns, and category-wise trends to support menu optimisation, promotions, and inventory decisions.

---

## What this code does

- **Data:** Merges monthly POS (PetPooja) Excel exports into a single dataset, cleans and standardises item names, and maps each item to a menu category using fuzzy matching against a master menu.
- **Analysis:** Builds category-wise summary statistics (sales, quantity, yearly breakdown), appetiser vs main-course comparisons, top/bottom items by category, and correlation between quantity and revenue.
- **Outputs:** Saves a summary table as DOCX, and a set of plots (sales by year, by category, appetiser vs main, top alcoholic/cocktails/mocktails/juices, correlation scatter) to the `output/` folder.

---

## Data and context

- **Source:** PetPooja POS; monthly files with item name, quantity, total amount, type (e.g. dine-in), and month/year.
- **Menu:** A structured menu (categories → items) is used to assign a single **Category** to every transaction line so analysis can be done at category and item level.
- **Scope:** Descriptive statistics and visualisations only in this repo; the full report also covers order-wise mapping over time, market basket analysis (e.g. Apriori), network graphs of co-ordered items, and channel-wise distribution—those parts use order-level data and are outside this codebase.

---

## How to run

```bash
cd BDM_Project
pip install -r requirements.txt
# Place monthly Excel files (e.g. Jan_2023.xlsx … Dec_2024.xlsx) in data/
python main.py
```

Use `--no-report` or `--no-plots` to skip DOCX or plots. See `VISUALIZATION_AND_ANALYSIS_COVERAGE.md` for the full list of analyses and figures.

---

## Project structure

| Path | Purpose |
|------|--------|
| `config.py` | Data and output paths; month-to-filename mapping |
| `data_loader.py` | Load and preprocess monthly Excel files |
| `menu.py` | Master menu (category → items) for categorisation |
| `categorize.py` | Fuzzy matching and category assignment/correction |
| `analysis.py` | Summary table, appetiser vs main, top/bottom items, correlation |
| `reports.py` | Export summary table to DOCX |
| `visualization.py` | All plots (year, category, appetiser vs main, top-by-category, correlation) |
| `main.py` | End-to-end pipeline entry point |
| `data/` | Input Excel files (not in repo) |
| `output/` | Generated DOCX and PNGs |

---

## Key takeaways (from the full report)

- **Time:** Order volume grew from 2023 to 2024; average order value shifted—opportunity for combos and value offers.
- **Categories:** Alcoholic beverages, global/Indian appetisers (non-veg), side dishes, and mocktails drive volume and revenue; juices and beverages lead by order count.
- **Basket behaviour:** Strong pairings (e.g. chakli & Budweiser, masala papad & Blenders Pride, main course + bread/rice) suggest targeted combos and upsells.
- **Channel:** Dine-in (restaurant + lounge) dominates over delivery; the code’s “Type” field can support channel-wise analysis if present in the data.

---

*Final report: “From your mind to your plate…” — BDM Capstone, IIT Madras. This code supports the descriptive and category-level analysis described there.*
