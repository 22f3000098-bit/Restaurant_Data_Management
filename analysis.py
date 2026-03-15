from __future__ import annotations

import re
from typing import Any

import pandas as pd
from fuzzywuzzy import fuzz

from constants import COL_CATEGORY, COL_ITEM, UNKNOWN_CATEGORY


def _normalize_item(s: str, drop_volume: bool = False) -> str:
    s = str(s).lower().strip().replace(".", "")
    s = re.sub(r"\bnip\b", "", s).strip()
    if drop_volume:
        s = re.sub(r"\b\d+\s*(ml|l|oz|cl)\b", "", s).strip()
    return s


def _build_normalized_menu_pairs(menu: dict[str, list]) -> list[tuple[str, str]]:
    return [
        (_normalize_item(m), cat)
        for cat, items in menu.items()
        for m in items
    ]


def _build_exact_match_map(menu: dict[str, list]) -> dict[str, str]:
    return {
        _normalize_item(m): cat
        for cat, items in menu.items()
        for m in items
    }


def categorize_item(
    item: Any, menu: dict[str, list], threshold: int = 80,
    normalized_pairs: list[tuple[str, str]] | None = None,
) -> str:
    norm_item = _normalize_item(item)
    pairs = normalized_pairs if normalized_pairs is not None else _build_normalized_menu_pairs(menu)
    best_match_category = UNKNOWN_CATEGORY
    best_match_score = 0
    for menu_norm, category in pairs:
        score = fuzz.ratio(norm_item, menu_norm)
        if score >= threshold and score > best_match_score:
            best_match_category = category
            best_match_score = score
    return best_match_category


def correct_categories(df: pd.DataFrame, menu: dict[str, list], verbose: bool = False) -> pd.DataFrame:
    exact = _build_exact_match_map(menu)
    for index, row in df.iterrows():
        norm = _normalize_item(row[COL_ITEM], drop_volume=True)
        correct_cat = exact.get(norm)
        if correct_cat is not None and row[COL_CATEGORY] != correct_cat:
            if verbose:
                print(f"Corrected '{row[COL_ITEM]}' from '{row[COL_CATEGORY]}' to '{correct_cat}'")
            df.loc[index, COL_CATEGORY] = correct_cat
    return df


def assign_and_correct_categories(
    df: pd.DataFrame, menu: dict[str, list], threshold: int = 80, verbose: bool = False
) -> pd.DataFrame:
    df = df.copy()
    pairs = _build_normalized_menu_pairs(menu)
    df[COL_CATEGORY] = df[COL_ITEM].apply(
        lambda x: categorize_item(x, menu, threshold, normalized_pairs=pairs)
    )
    correct_categories(df, menu, verbose=verbose)
    return df
