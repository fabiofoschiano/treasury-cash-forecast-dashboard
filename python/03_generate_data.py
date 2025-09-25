# 03_generate_data.py
# Generate a larger synthetic transactions dataset

import pandas as pd
import numpy as np

# Generate dates for January 2025
dates = pd.date_range("2025-01-01", "2025-01-30")

# Possible currencies and transaction types
currencies = ["USD", "EUR"]
types = ["inflow", "outflow"]

rows = []
for d in dates:
    for _ in range(np.random.randint(1, 4)):  # 1–3 transactions per day
        rows.append({
            "id": len(rows) + 1,
            "date": d.strftime("%Y-%m-%d"),
            "amount": round(np.random.randint(100, 2000), 2),
            "currency": np.random.choice(currencies),
            "type": np.random.choice(types)
        })

# Create DataFrame and save as CSV
transactions = pd.DataFrame(rows)
transactions.to_csv("data/transactions.csv", index=False)
print("Expanded transactions dataset created!")
