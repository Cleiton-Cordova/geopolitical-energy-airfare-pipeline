
import requests
from pathlib import Path
from datetime import datetime, timedelta

# Define the project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Define the output directory
OUTPUT_DIR = PROJECT_ROOT / "data" / "raw" / "gdelt_batch"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Define the GDELT data source
BASE_URL = "https://data.gdeltproject.org/gdeltv2/"

# Define the starting timestamp
START_DATE = datetime(2025, 1, 1, 0, 0)

# Download four consecutive 15-minute files
for i in range(4):
    timestamp = START_DATE + timedelta(minutes=15 * i)
    filename = timestamp.strftime("%Y%m%d%H%M%S") + ".export.CSV.zip"

    file_path = OUTPUT_DIR / filename
    file_url = BASE_URL + filename

    # Skip files that have already been downloaded
    if file_path.exists():
        print("Using existing file:", filename)
        continue

    # Download the GDELT file
    try:
        response = requests.get(file_url, timeout=60)
        response.raise_for_status()

        with open(file_path, "wb") as file:
            file.write(response.content)

        print("Downloaded:", filename)

    except requests.RequestException as error:
        print("Download failed:", filename, error)

print("Batch extraction completed.")
