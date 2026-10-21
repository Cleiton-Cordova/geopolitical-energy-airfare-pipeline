
import requests
import zipfile
import pandas as pd
from pathlib import Path

# Define the project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Define the output directory for raw data
OUTPUT_DIR = PROJECT_ROOT / "data" / "raw"
ZIP_FILE = OUTPUT_DIR / "gdelt_events_sample.zip"

# Define the GDELT 2.0 Events historical data source
BASE_URL = "https://data.gdeltproject.org/gdeltv2/"

# Define the sample file from January 1, 2025
SAMPLE_FILE = "20250101000000.export.CSV.zip"
SAMPLE_URL = BASE_URL + SAMPLE_FILE

print("Sample URL:", SAMPLE_URL)

# Create the output directory if it does not exist
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Download the sample file only if it does not already exist
if not ZIP_FILE.exists():
    response = requests.get(SAMPLE_URL, timeout=60)
    response.raise_for_status()

    with open(ZIP_FILE, "wb") as file:
        file.write(response.content)

    print("File downloaded:", ZIP_FILE)
else:
    print("Using existing file:", ZIP_FILE)

# Open the ZIP file and inspect its structure
with zipfile.ZipFile(ZIP_FILE, "r") as zip_file:
    filenames = zip_file.namelist()

    print("Files inside ZIP:", filenames)

    # Read the first row to inspect the dataset structure
    with zip_file.open(filenames[0]) as csv_file:
        first_row = csv_file.readline().decode("utf-8")
        columns = first_row.strip().split("\t")

        print("Number of columns:", len(columns))
        print("First 10 values:", columns[:10])

    # Read GDELT events from the ZIP archive
    with zip_file.open(filenames[0]) as csv_file:
        df = pd.read_csv(
            csv_file,
            sep="\t",
            header=None,
            low_memory=False
        )

# Assign descriptive names to the relevant GDELT columns
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

# Display the dataset preview
print("\nGDELT dataset preview:")
print(
    df[
        [
            "event_date",
            "actor1_country",
            "actor2_country",
            "event_code",
            "event_root_code"
        ]
    ].head()
)

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

# Display the US-Iran events
print("\nTotal events:", len(df))
print("US-Iran events:", len(us_iran_events))

print("\nFirst US-Iran events:")
print(
    us_iran_events[
        [
            "event_date",
            "actor1_country",
            "actor2_country",
            "event_code",
            "event_root_code",
            "quad_class",
            "goldstein_scale",
            "num_mentions",
            "source_url"
        ]
    ].to_string(index=False)
)

# Count events by CAMEO root category
event_categories = (
    df["event_root_code"]
    .value_counts()
    .sort_index()
)

print("\nEvents by CAMEO root category:")
print(event_categories)

# Define CAMEO root codes associated with conflict
CONFLICT_ROOT_CODES = set(range(13, 21))

# Filter US-Iran events classified as conflict
us_iran_conflicts = us_iran_events[
    us_iran_events["event_root_code"].isin(CONFLICT_ROOT_CODES)
]

# Display the filtered conflict events
print("\nUS-Iran conflict events:", len(us_iran_conflicts))

print(
    us_iran_conflicts[
        [
            "event_date",
            "actor1_country",
            "actor2_country",
            "event_code",
            "event_root_code",
            "goldstein_scale",
            "num_mentions",
            "source_url"
        ]
    ].to_string(index=False)
)
