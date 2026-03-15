Output folder for BDM Project

After you run:
  python main.py

from the BDM_Project directory, the following appear here:
  - final_summary_table.docx  (category-wise summary)
  - *.png                      (all plots: sales by year, by category, appetizer vs main, top items, correlation)

If this folder is empty, run main.py with your Excel files in data/sales_data/ (or set DATA_DIR in config.py).
The script will print the full path to this folder when it runs.
