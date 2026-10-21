from datetime import datetime, timedelta

# Define the starting timestamp
start_date = datetime(2025, 1, 1, 0, 0)

# Generate four consecutive 15-minute timestamps
for i in range(4):
    timestamp = start_date + timedelta(minutes=15 * i)

    filename = timestamp.strftime("%Y%m%d%H%M%S") + ".export.CSV.zip"

    print(filename)