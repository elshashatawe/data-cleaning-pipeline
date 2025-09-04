import pandas as pd
import argparse
import os

def clean_data(input_path, output_path):
    # Load data
    df = pd.read_csv(input_path)

    # Standardize column names
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

    # Drop duplicates
    df = df.drop_duplicates()

    # Handle missing values (drop rows with all NaN, fill others with defaults)
    df = df.dropna(how='all')
    df = df.fillna({'age': 0})  # Example: fill missing ages with 0

    # Save cleaned data
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"✅ Cleaned data saved to {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clean raw CSV data.")
    parser.add_argument("--input", required=True, help="Path to input raw CSV file")
    parser.add_argument("--output", required=True, help="Path to save cleaned CSV file")
    args = parser.parse_args()

    clean_data(args.input, args.output)
