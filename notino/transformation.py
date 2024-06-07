import csv
from datetime import datetime

print("Processing...")

# Load the raw data
with open("notino_raw.csv", "r") as f:
    reader = csv.DictReader(f)
    data = list(reader)

# Add default values for country and currency
for row in data:
    row['Country'] = 'CZ'
    row['Currency'] = 'Kč'

# Add scraped_at column with current datetime
current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
for row in data:
    row['Scraped_at'] = current_datetime

# Calculate discount amount
for row in data:
    price = float(row['Price'])
    discount = float(row['Discount'])
    row['Discount_Amount'] = price + (price * (discount / 100))

# Export the transformed data
fieldnames = data[0].keys()
with open("notino_transformed.csv", "w", encoding="utf8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)

print("Successfully printed.")
