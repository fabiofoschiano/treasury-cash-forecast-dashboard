import csv
import random
from datetime import datetime, timedelta

# Output CSV file
filename = "data/transactions.csv"

# Parameters
start_date = datetime(2025, 1, 1)
num_days = 15
currencies = ["EUR", "USD"]
types = ["inflow", "outflow"]

# Generate transactions
transactions = []
id_counter = 1
for i in range(num_days):
    date = (start_date + timedelta(days=i)).strftime("%Y-%m-%d")
    num_tx = random.randint(1, 3)  # 1–3 transactions per day
    for _ in range(num_tx):
        amount = random.randint(100, 2000)
        currency = random.choice(currencies)
        tx_type = random.choice(types)
        transactions.append([id_counter, date, amount, currency, tx_type])
        id_counter += 1

# Write CSV
with open(filename, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["id", "date", "amount", "currency", "type"])
    writer.writerows(transactions)

print(f"Generated {len(transactions)} transactions in {filename}")
