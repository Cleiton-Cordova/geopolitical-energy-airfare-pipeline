
import pandas as pd
from pathlib import Path

# Define the project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Define the monthly GDELT dataset path
INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "gdelt_us_iran_monthly.csv"
)

# Load the monthly dataset
df = pd.read_csv(INPUT_FILE)

# Inspect the original date values before conversion
print("\nOriginal month values:")
print(df["month"].head(10).to_string(index=False))

print("\nOriginal month data type:")
print(df["month"].dtype)

# Convert dates using the day/month/year format
df["month"] = pd.to_datetime(
    df["month"],
    format="%d/%m/%Y",
    errors="coerce"
)

# Define the expected monthly date range
expected_months = pd.date_range(
    start="2022-01-01",
    end="2026-08-01",
    freq="MS"
)

# Check for missing and unexpected months
actual_months = pd.DatetimeIndex(df["month"].dropna())

missing_months = expected_months.difference(actual_months)
unexpected_months = actual_months.difference(expected_months)

# Check duplicate months
duplicate_months = df["month"].duplicated().sum()

# Check missing values
missing_values = df.isnull().sum()

# Validate numerical indicators
numeric_columns = [
    "conflict_events",
    "avg_goldstein",
    "total_mentions"
]

invalid_numeric_values = {}

for column in numeric_columns:
    numeric_values = pd.to_numeric(df[column], errors="coerce")
    invalid_numeric_values[column] = int(numeric_values.isna().sum())

# Display validation results
print("=== GDELT MONTHLY DATA VALIDATION ===")

print("\nTotal rows:", len(df))
print("Expected months:", len(expected_months))
print("Missing months:", len(missing_months))
print("Unexpected months:", len(unexpected_months))
print("Duplicate months:", duplicate_months)

print("\nMissing values:")
print(missing_values)

print("\nInvalid numeric values:")
print(invalid_numeric_values)

print("\nDate range:")
print("Earliest month:", df["month"].min())
print("Latest month:", df["month"].max())

print("\n=== VALIDATION COMPLETED ===")
