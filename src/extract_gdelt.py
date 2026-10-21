import requests
import time
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_FILE = PROJECT_ROOT / "data" / "raw" / "gdelt_iran_test.json"

BASE_URL = "https://api.gdeltproject.org/api/v2/doc/doc"

params = {
    "query": "Iran",
    "mode": "TimelineVol",
    "format": "json",
    "timespan": "1week"
}
response = requests.get(
    BASE_URL,
    params=params,
    timeout=30,
    headers={"User-Agent": "EnergyAirfareResearch/1.0"}
)

if response.status_code == 429:
    print("Rate limit reached. Waiting 10 seconds...")
    time.sleep(10)

    response = requests.get(
        BASE_URL,
        params=params,
        timeout=30,
        headers={"User-Agent": "EnergyAirfareResearch/1.0"}
    )

print("Status code:", response.status_code)
print("URL:", response.url)

print("Retry-After:", response.headers.get("Retry-After"))
print("Response:", response.text[:500])

if response.status_code == 200:
    data = response.json()

    print("JSON keys:", data.keys())
    print("Number of series:", len(data["timeline"]))
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    print("Data saved to:", OUTPUT_FILE)