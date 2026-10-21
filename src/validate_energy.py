import pandas as pd


# 1. Load processed datasets
brent = pd.read_csv(
    "data/processed/brent_daily_processed.csv",
    parse_dates=["date"]
)

jet_fuel = pd.read_csv(
    "data/processed/jet_fuel_daily_processed.csv",
    parse_dates=["date"]
)


# 2. Validation function
def validate_dataset(name, df):
    print(f"\n===== {name} =====")

    print(f"Rows: {len(df)}")

    print(f"Missing values: {df.isnull().sum().sum()}")

    print(f"Duplicate rows: {df.duplicated().sum()}")

    print(f"Start date: {df['date'].min().date()}")

    print(f"End date: {df['date'].max().date()}")


# 3. Validate datasets
validate_dataset("BRENT", brent)
validate_dataset("JET FUEL", jet_fuel)