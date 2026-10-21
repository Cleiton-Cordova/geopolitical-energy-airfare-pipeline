
import pandas as pd
from pathlib import Path

# Define the project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Define the processed CSV file
INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "gdelt_us_iran_conflicts_test.csv"
)

# Load the processed dataset
df = pd.read_csv(INPUT_FILE)

print("=== GDELT DATA QUALITY VALIDATION ===")

# Check the total number of records
print("\nTotal records:", len(df))

# Check missing values
print("\nMissing values:")
print(df.isnull().sum())

# Check duplicate event identifiers
duplicate_count = df["global_event_id"].duplicated().sum()
print("\nDuplicate event IDs:", duplicate_count)

# Validate event dates
event_dates = pd.to_datetime(
    df["event_date"].astype(str),
    format="%Y%m%d",
    errors="coerce"
)

invalid_dates = event_dates.isna().sum()
print("Invalid event dates:", invalid_dates)

# Check the date range
print("\nEarliest event date:", event_dates.min())
print("Latest event date:", event_dates.max())

# Validate country pairs
valid_countries = (
    (
        (df["actor1_country"] == "USA") &
        (df["actor2_country"] == "IRN")
    ) |
    (
        (df["actor1_country"] == "IRN") &
        (df["actor2_country"] == "USA")
    )
)

print("Invalid country pairs:", (~valid_countries).sum())

# Validate conflict root codes
valid_conflicts = df["event_root_code"].isin(range(13, 21))
print("Invalid conflict codes:", (~valid_conflicts).sum())

# Display the validation summary
print("\n=== VALIDATION COMPLETED ===")
