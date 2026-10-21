import pandas as pd


DATA_PATH = "data/processed/energy_airfare_integrated.csv"

df = pd.read_csv(
    DATA_PATH,
    parse_dates=["date"],
)

print("===== INTEGRATED DATASET VALIDATION =====")

print("\nShape:")
print(df.shape)

print("\nColumns:")
print(df.columns.tolist())

print("\nData types:")
print(df.dtypes)

print("\nMissing values:")
print(df.isna().sum())

print("\nDuplicate rows:")
print(df.duplicated().sum())

print("\nDate range:")
print(df["date"].min(), "to", df["date"].max())

print("\nRows per country:")
print(df.groupby("country").size())

print("\nDescriptive statistics:")
print(
    df[
        [
            "airfare_index",
            "price_usd_per_barrel",
            "price_usd_per_gallon",
        ]
    ].describe()
)