# Data Cleaning Pipeline  

This project provides a **reproducible data-cleaning pipeline** in Python using `pandas`.  

## 📂 Project Structure
- **clean_data.py** → Main script for cleaning datasets.  
- **requirements.txt** → Python dependencies.  
- **data/raw/** → Raw input CSV files.  
- **data/processed/** → Cleaned output CSV files.  

## ⚙️ What it does
- Loads raw CSV of customers.  
- Standardizes column names.  
- Drops duplicates.  
- Fixes missing values.  
- Exports a clean dataset to `data/processed/`.  

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the cleaning script
python clean_data.py --input data/raw/customers.csv --output data/processed/customers_clean.csv
```
