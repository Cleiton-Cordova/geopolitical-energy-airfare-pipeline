import pandas as pd
import requests

url = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/prc_hicp_minr"

params = {
    "lang": "en",
    "freq": "M",
    "unit": "I25",
    "coicop18": "CP0733",
    "geo": ["DE", "ES", "FR", "IT", "NL"],
    "sinceTimePeriod": "2022-01",
    "untilTimePeriod": "2026-08",
}

response = requests.get(url, params=params, timeout=30)

print("Status code:", response.status_code)
print(response.url)

data = response.json()

print("\nDataset label:")
print(data.get("label"))

print("\nDimensions:")
print(data.get("id"))

print("\nDataset size:")
print(data.get("size"))

print("\nNumber of observations:")
print(len(data.get("value", {})))

# Convert Eurostat JSON-stat response to a DataFrame

geo_dimension = data["dimension"]["geo"]["category"]
time_dimension = data["dimension"]["time"]["category"]

geo_index = geo_dimension["index"]
geo_labels = geo_dimension["label"]

time_index = time_dimension["index"]

rows = []

for geo_code, geo_position in geo_index.items():
    for time_period, time_position in time_index.items():

        # JSON-stat stores values in a flattened array.
        value_position = (
            geo_position * len(time_index)
            + time_position
        )

        value = data["value"].get(str(value_position))

        rows.append(
            {
                "date": time_period,
                "country_code": geo_code,
                "country": geo_labels[geo_code],
                "airfare_index": value,
            }
        )

df = pd.DataFrame(rows)

print("\nAirfare DataFrame:")
print(df)

print("\nData types:")
print(df.dtypes)

# Convert date to datetime
df["date"] = pd.to_datetime(df["date"], format="%Y-%m")

# Validate the dataset
print("\nValidation:")
print("Rows:", len(df))
print("Missing values:", df.isna().sum().sum())
print("Duplicate rows:", df.duplicated().sum())
print("Start date:", df["date"].min())
print("End date:", df["date"].max())

# Save raw data
df.to_csv(
    "data/raw/airfare_hicp_raw.csv",
    index=False
)

print("\nRaw airfare data saved successfully!")

# Create processed dataset
df_processed = df[
    [
        "date",
        "country_code",
        "country",
        "airfare_index",
    ]
].copy()

df_processed.to_csv(
    "data/processed/airfare_hicp_processed.csv",
    index=False
)

print("Processed airfare data saved successfully!")

print("\nProcessed data:")
print(df_processed)