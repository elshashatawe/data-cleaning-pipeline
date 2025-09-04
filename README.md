
# Data Cleaning Pipeline

A reproducible **data-cleaning pipeline** in Python using `pandas`.

![Pipeline Diagram](data_cleaning_diagram.png)

## What it does
- Standardizes column names (lowercase, snake_case).
- Strips whitespace from string columns.
- (Optional) Infers date-like columns and formats them as ISO (`YYYY-MM-DD`).
- Drops duplicates (by an id column if provided, else row duplicates).
- Fills missing values (0 for numeric, empty string for text).
- Exports a clean CSV.

## Quick start

```bash
# 1) Install dependencies (Python 3.8+)
pip install -r requirements.txt

# 2) Run the cleaning script
python clean_data.py --input data/raw/customers.csv --output data/processed/customers_clean.csv --id-col id --infer-dates
```

## Project structure
```
data-cleaning-pipeline/
├─ clean_data.py           # Main script (CLI)
├─ requirements.txt        # Dependencies
├─ README.md               # This file
├─ data_cleaning_diagram.png
└─ data/
   ├─ raw/
   │  └─ customers.csv     # Example input
   └─ processed/
      └─ customers_clean.csv (example output)
```

## Input format (`data/raw/customers.csv`)

Example:
```csv
id,Name,Email,Signup Date,City
1, Alice ,ALICE@example.com,2024-04-01 , Cairo
2,Bob,bob@example.com,2024/04/02, Giza
2,Bob,bob@example.com,2024/04/02, Giza   # Duplicate row by id
3,Charlie,,2024-04-03,Alexandria
4,,dina@example.com,03-04-2024,  Tanta
```

## Output (cleaned)
- Column names will be snake_case.
- Whitespace removed; emails remain lowercase after strip step.
- Dates inferred/formatted to `YYYY-MM-DD` if `--infer-dates` is used.
- Duplicates dropped by `--id-col id`.

```bash
python clean_data.py --input data/raw/customers.csv --output data/processed/customers_clean.csv --id-col id --infer-dates
```
