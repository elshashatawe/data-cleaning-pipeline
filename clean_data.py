
#!/usr/bin/env python3
"""
clean_data.py
A small, reproducible data cleaning pipeline using pandas.

Usage
-----
python clean_data.py --input data/raw/customers.csv --output data/processed/customers_clean.csv \
    [--id-col id] [--infer-dates]

What it does
------------
- Loads a CSV file
- Standardizes column names (lowercase, snake_case, trimmed)
- Strips leading/trailing whitespace from string columns
- Optionally converts date-like columns to ISO format
- Drops duplicate rows (by an id column if provided, else full row duplicates)
- Fills missing values (empty string for object columns, 0 for numeric columns)
- Exports a clean CSV

This script is intentionally lightweight and dependency-light (pandas only).
"""

import argparse
import re
import sys
from typing import Optional, List

import pandas as pd


def to_snake_case(name: str) -> str:
    name = name.strip()
    name = re.sub(r"[^\w\s]", "", name)  # remove punctuation
    name = re.sub(r"\s+", "_", name)     # spaces => underscore
    return name.lower()


def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [to_snake_case(c) for c in df.columns]
    return df


def strip_strings(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    for col in df.select_dtypes(include=["object", "string"]).columns:
        df[col] = df[col].astype(str).str.strip()
    return df


def infer_and_format_dates(df: pd.DataFrame, sample_n: int = 200) -> pd.DataFrame:
    """
    Try to parse columns that look like dates (by name or by sample parsing).
    Convert successfully parsed columns to ISO (YYYY-MM-DD).
    """
    df = df.copy()
    candidates: List[str] = []
    for col in df.columns:
        if "date" in col or "dt" in col:
            candidates.append(col)

    # If no obvious candidates by name, inspect a small sample of columns to see if most values parse as dates.
    for col in df.columns:
        if col in candidates:
            continue
        series = df[col].dropna().astype(str)
        if series.empty:
            continue
        sample = series.sample(min(sample_n, len(series)), random_state=42)
        try:
            parsed = pd.to_datetime(sample, errors="coerce", utc=False, dayfirst=False)
            # if a majority parse as dates, treat as date column
            if parsed.notna().mean() >= 0.7:
                candidates.append(col)
        except Exception:
            pass

    for col in candidates:
        try:
            parsed = pd.to_datetime(df[col], errors="coerce", utc=False, dayfirst=False)
            # keep original if almost nothing parsed
            if parsed.notna().mean() < 0.3:
                continue
            df[col] = parsed.dt.date.astype("string")  # ISO yyyy-mm-dd
        except Exception:
            # ignore columns that fail
            pass

    return df


def fill_missing(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            df[col] = df[col].fillna(0)
        else:
            df[col] = df[col].fillna("")
    return df


def drop_duplicates(df: pd.DataFrame, id_col: Optional[str] = None) -> pd.DataFrame:
    df = df.copy()
    if id_col and id_col in df.columns:
        return df.drop_duplicates(subset=[id_col], keep="first")
    return df.drop_duplicates(keep="first")


def clean_pipeline(input_path: str, output_path: str, id_col: Optional[str], infer_dates: bool) -> None:
    print(f"[INFO] Loading: {input_path}")
    df = pd.read_csv(input_path)

    print("[INFO] Standardizing columns...")
    df = standardize_columns(df)

    print("[INFO] Stripping strings...")
    df = strip_strings(df)

    if infer_dates:
        print("[INFO] Inferring and formatting date columns...")
        df = infer_and_format_dates(df)

    print("[INFO] Dropping duplicates...")
    df = drop_duplicates(df, id_col=id_col)

    print("[INFO] Filling missing values...")
    df = fill_missing(df)

    print(f"[INFO] Saving cleaned data to: {output_path}")
    # Ensure parent dirs exist
    import os
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print("[DONE]")


def parse_args(argv=None):
    p = argparse.ArgumentParser(description="Simple data cleaning pipeline")
    p.add_argument("--input", required=True, help="Path to raw input CSV")
    p.add_argument("--output", required=True, help="Path to output cleaned CSV")
    p.add_argument("--id-col", default=None, help="Optional ID column used to drop duplicates")
    p.add_argument("--infer-dates", action="store_true", help="Infer/format date-like columns to ISO")
    return p.parse_args(argv)


if __name__ == "__main__":
    args = parse_args()
    clean_pipeline(args.input, args.output, id_col=args.id_col, infer_dates=args.infer_dates)
