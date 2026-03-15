from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "output"

MONTH_YEAR_TO_FILE: dict[str, str] = {
    "January 2023": "Jan_2023.xlsx",
    "February 2023": "Feb_2023.xlsx",
    "March 2023": "Mar_2023.xlsx",
    "April 2023": "Apr_2023.xlsx",
    "May 2023": "May_2023.xlsx",
    "June 2023": "Jun_2023.xlsx",
    "July 2023": "Jul_2023.xlsx",
    "August 2023": "Aug_2023.xlsx",
    "September 2023": "Sep_2023.xlsx",
    "October 2023": "Oct_2023.xlsx",
    "November 2023": "Nov_2023.xlsx",
    "December 2023": "Dec_2023.xlsx",
    "January 2024": "Jan_2024.xlsx",
    "February 2024": "Feb_2024.xlsx",
    "March 2024": "Mar_2024.xlsx",
    "April 2024": "Apr_2024.xlsx",
    "May 2024": "May_2024.xlsx",
    "June 2024": "Jun_2024.xlsx",
    "July 2024": "Jul_2024.xlsx",
    "August 2024": "Aug_2024.xlsx",
    "September 2024": "Sep_2024.xlsx",
    "October 2024": "Oct_2024.xlsx",
    "November 2024": "Nov_2024.xlsx",
    "December 2024": "Dec_2024.xlsx",
}


def get_file_paths() -> dict[str, Path]:
    return {
        month_year: DATA_DIR / filename
        for month_year, filename in MONTH_YEAR_TO_FILE.items()
        if (DATA_DIR / filename).exists()
    }
