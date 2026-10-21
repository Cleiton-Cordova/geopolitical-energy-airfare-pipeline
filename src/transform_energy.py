import pandas as pd



# Load processed energy datasets
brent = pd.read_csv(
    "data/processed/brent_daily_processed.csv",
    parse_dates=["date"],
)

jet_fuel = pd.read_csv(
    "data/processed/jet_fuel_daily_processed.csv",
    parse_dates=["date"],
)

print("\n===== BRENT =====")
print(brent.head())
print("\nShape:", brent.shape)
print("\nData types:")
print(brent.dtypes)

print("\n===== JET FUEL =====")
print(jet_fuel.head())
print("\nShape:", jet_fuel.shape)
print("\nData types:")
print(jet_fuel.dtypes)

# Convert daily energy prices to monthly averages

brent_monthly = (
    brent
    .set_index("date")["price_usd_per_barrel"]
    .resample("MS")
    .mean()
    .reset_index()
)

jet_fuel_monthly = (
    jet_fuel
    .set_index("date")["price_usd_per_gallon"]
    .resample("MS")
    .mean()
    .reset_index()
)

print("\n===== BRENT MONTHLY =====")
print(brent_monthly)

print("\n===== JET FUEL MONTHLY =====")
print(jet_fuel_monthly)


# Merge monthly Brent and Jet Fuel datasets

energy_monthly = pd.merge(
    brent_monthly,
    jet_fuel_monthly,
    on="date",
    how="inner",
)

print("\n===== ENERGY MONTHLY =====")
print(energy_monthly)

print("\nShape:", energy_monthly.shape)

print("\nMissing values:")
print(energy_monthly.isna().sum())


# Load monthly airfare dataset
airfare = pd.read_csv(
    "data/processed/airfare_hicp_processed.csv",
    parse_dates=["date"],
)

# Merge airfare with monthly energy prices
final_dataset = pd.merge(
    airfare,
    energy_monthly,
    on="date",
    how="inner",
)

print("\n===== FINAL INTEGRATED DATASET =====")
print(final_dataset)

print("\nShape:", final_dataset.shape)

print("\nMissing values:")
print(final_dataset.isna().sum())

print("\nDate range:")
print(final_dataset["date"].min(), "to", final_dataset["date"].max())

print("\nRows per country:")
print(final_dataset.groupby("country").size())


# Save transformed datasets

energy_monthly.to_csv(
    "data/processed/energy_monthly_processed.csv",
    index=False,
)

final_dataset.to_csv(
    "data/processed/energy_airfare_integrated.csv",
    index=False,
)

print("\nFiles saved successfully:")
print("- data/processed/energy_monthly_processed.csv")
print("- data/processed/energy_airfare_integrated.csv")