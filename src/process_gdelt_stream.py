
import zipfile
import pandas as pd
from pathlib import Path

# Define the project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Define the directory containing GDELT ZIP files
INPUT_DIR = PROJECT_ROOT / "data" / "raw" / "gdelt_batch"

# Find all downloaded GDELT ZIP files
ZIP_FILES = sorted(INPUT_DIR.glob("*.export.CSV.zip"))

print("ZIP files found:", len(ZIP_FILES))

# Define the relevant GDELT column positions
COLUMN_NAMES = {
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
}

# Define conflict-related CAMEO root codes
CONFLICT_ROOT_CODES = set(range(13, 21))

# Store filtered records from all files
filtered_chunks = []
total_records = 0

# Process each downloaded GDELT ZIP file
for zip_path in ZIP_FILES:
    print("Processing:", zip_path.name)

    # Open the ZIP archive without extracting it
    with zipfile.ZipFile(zip_path, "r") as zip_file:
        csv_filename = zip_file.namelist()[0]

        with zip_file.open(csv_filename) as csv_file:

            # Read the CSV in chunks of 500 rows
            for chunk in pd.read_csv(
                csv_file,
                sep="\t",
                header=None,
                usecols=list(COLUMN_NAMES.keys()),
                chunksize=500
            ):
                total_records += len(chunk)

                # Rename the selected columns
                chunk = chunk.rename(columns=COLUMN_NAMES)

                # Identify events involving the United States and Iran
                country_filter = (
                    (
                        (chunk["actor1_country"] == "USA") &
                        (chunk["actor2_country"] == "IRN")
                    ) |
                    (
                        (chunk["actor1_country"] == "IRN") &
                        (chunk["actor2_country"] == "USA")
                    )
                )

                # Identify conflict-related events
                conflict_filter = chunk["event_root_code"].isin(
                    CONFLICT_ROOT_CODES
                )

                # Keep only relevant records
                filtered_chunk = chunk[
                    country_filter & conflict_filter
                ].copy()

                if not filtered_chunk.empty:
                    filtered_chunks.append(filtered_chunk)

# Combine filtered records from all files
if filtered_chunks:
    filtered_df = pd.concat(
        filtered_chunks,
        ignore_index=True
    )

    # Remove duplicate events across files
    filtered_df = filtered_df.drop_duplicates(
        subset=["global_event_id"]
    )
else:
    filtered_df = pd.DataFrame(
        columns=list(COLUMN_NAMES.values())
    )

# Display processing results
print("\nTotal records processed:", total_records)
print("Unique US-Iran conflict events:", len(filtered_df))

print("\nFiltered events:")
print(filtered_df.to_string(index=False))


# Define the output directory
OUTPUT_DIR = PROJECT_ROOT / "data" / "processed"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Define the output CSV file
OUTPUT_FILE = OUTPUT_DIR / "gdelt_us_iran_conflicts_test.csv"

# Save unique conflict events to CSV
filtered_df.to_csv(OUTPUT_FILE, index=False)

print("\nProcessed data saved to:", OUTPUT_FILE)
