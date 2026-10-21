import os

import pandas as pd
import requests
from dotenv import load_dotenv


# 1. Load environment variables
load_dotenv()

api_key = os.getenv("EIA_API_KEY")


# 2. EIA API configuration
url = "https://api.eia.gov/v2/petroleum/pri/spt/data/"

params = {
    "api_key": api_key,
    "frequency": "daily",
    "data[0]": "value",
    "facets[series][]": "EER_EPJK_PF4_RGC_DPG",
    "start": "2022-01-01",
    "sort[0][column]": "period",
    "sort[0][direction]": "asc",
    "length": 5000
}


# 3. Extract data from EIA API
response = requests.get(url, params=params, timeout=30)

data = response.json()["response"]["data"]

df = pd.DataFrame(data)


# 4. Save raw data
df.to_csv(
    "data/raw/jet_fuel_daily_raw.csv",
    index=False
)

print("\nRaw Jet Fuel data saved successfully!")


# 5. Transform data
df["period"] = pd.to_datetime(df["period"])
df["value"] = pd.to_numeric(df["value"])

df_processed = df[
    [
        "period",
        "product-name",
        "series",
        "value",
        "units"
    ]
].copy()

df_processed = df_processed.rename(
    columns={
        "period": "date",
        "product-name": "product_name",
        "value": "price_usd_per_gallon"
    }
)


# 6. Save processed data
df_processed.to_csv(
    "data/processed/jet_fuel_daily_processed.csv",
    index=False
)

print("Processed Jet Fuel data saved successfully!")


# 7. Preview processed data
print("\nProcessed data:")
print(df_processed)