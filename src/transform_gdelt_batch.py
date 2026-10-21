
import zipfile
import pandas as pd
from pathlib import Path

# Define the project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Define the directory containing downloaded GDELT files
INPUT_DIR = PROJECT_ROOT / "data" / "raw" / "gdelt_batch"

# Find all downloaded ZIP files
zip_files = sorted(INPUT_DIR.glob("*.export.CSV.zip"))

print("ZIP files found:", len(zip_files))

# Store DataFrames from each file
dataframes = []

for zip_path in zip_files:
    # Open each ZIP archive
    with zipfile.ZipFile(zip_path, "r") as zip_file:
        with zip_file.open(zip_file.namelist()[0]) as csv_file:
            df = pd.read_csv(
                csv_file,
                sep="\t",
                header=None,
                low_memory=False
            )

    # Rename relevant GDELT columns
    df = df.rename(columns={
        0: "global_event_id",
        1: "event_date",
        7: "actor1_country",
        17: "actor2_country",
        26: "event_code",
        28: "event_root_code",
        29: "quad_class",
        30: "goldstein_scale",
        31: "num_mentions",
        60: "source_url"
    })

    # Select events involving the United States and Iran
    us_iran_events = df[
        (
            (df["actor1_country"] == "USA") &
            (df["actor2_country"] == "IRN")
        ) |
        (
            (df["actor1_country"] == "IRN") &
            (df["actor2_country"] == "USA")
        )
    ]

    dataframes.append(us_iran_events)

# Combine the filtered events from all files
if dataframes:
    combined_df = pd.concat(dataframes, ignore_index=True)

    # Remove duplicate event records
    combined_df = combined_df.drop_duplicates(
        subset=["global_event_id"]
    )

    print("Total US-Iran events:", len(combined_df))

    # Filter conflict-related CAMEO categories
    conflict_df = combined_df[
        combined_df["event_root_code"].between(13, 20)
    ]

    print("US-Iran conflict events:", len(conflict_df))

    print(
        conflict_df[
            [
                "event_date",
                "actor1_country",
                "actor2_country",
                "event_code",
                "event_root_code",
                "goldstein_scale",
                "num_mentions"
            ]
        ].head(10).to_string(index=False)
    )
else:
    print("No ZIP files found.")

# Validate the combined GDELT dataset
if dataframes:
    print("\nData quality checks:")

    print(
        "Duplicate event IDs:",
        combined_df["global_event_id"].duplicated().sum()
    )

    print(
        "Missing event dates:",
        combined_df["event_date"].isna().sum()
    )

    print(
        "Missing country codes:",
        combined_df[
            ["actor1_country", "actor2_country"]
        ].isna().sum().sum()
    )

    print(
        "Event date range:",
        combined_df["event_date"].min(),
        "to",
        combined_df["event_date"].max()
    )
    
# Convert event dates to datetime
conflict_df = conflict_df.copy()

conflict_df["event_date"] = pd.to_datetime(
    conflict_df["event_date"].astype(str),
    format="%Y%m%d",
    errors="coerce"
)

# Create the monthly reference date
conflict_df["date"] = (
    conflict_df["event_date"]
    .dt.to_period("M")
    .dt.to_timestamp()
)

# Aggregate conflict events by month
monthly_conflicts = (
    conflict_df.groupby("date")
    .agg(
        conflict_events=("global_event_id", "nunique"),
        total_mentions=("num_mentions", "sum"),
        avg_goldstein=("goldstein_scale", "mean")
    )
    .reset_index()
)

print("\nMonthly US-Iran conflict summary:")
print(monthly_conflicts)