import json
import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
INPUT_FILE = PROJECT_ROOT / "data" / "raw" / "gdelt_iran_test.json"

with open(INPUT_FILE, "r", encoding="utf-8") as file:
    data = json.load(file)

print("JSON keys:", data.keys())

records = data["timeline"][0]["data"]

df = pd.DataFrame(records)

print(df.head())
print("Shape:", df.shape)

df["date"] = pd.to_datetime(
    df["date"],
    format="%Y%m%dT%H%M%SZ",
    utc=True
)

print(df.head())
print(df.dtypes)

df["month"] = df["date"].dt.to_period("M")

print(df[["date", "month", "value"]].head())

monthly_df = (
    df.groupby("month")
    .agg(
        gdelt_avg_volume=("value", "mean"),
        observations=("value", "count")
    )
    .reset_index()
)

print(monthly_df)

monthly_df["date"] = monthly_df["month"].dt.to_timestamp()

monthly_df = monthly_df[
    ["date", "gdelt_avg_volume", "observations"]
]

print(monthly_df)

OUTPUT_FILE = PROJECT_ROOT / "data" / "processed" / "gdelt_monthly_test.csv"

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

monthly_df.to_csv(OUTPUT_FILE, index=False)

print("CSV saved to:", OUTPUT_FILE)