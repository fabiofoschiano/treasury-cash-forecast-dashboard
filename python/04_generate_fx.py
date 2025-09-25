# 04_generate_fx.py
# Generate synthetic daily USD → EUR FX rates

import pandas as pd
import numpy as np

# Dates for January 2025
dates = pd.date_range("2025-01-01", "2025-01-30")

rows = []
for i, d in enumerate(dates, start=1):
    # Generate a rate between 1.05 and 1.15, with small random daily changes
    rate = round(1.05 + np.random.rand() * 0.10, 4)
    rows.append({
        "id": i,
        "date": d.strftime("%Y-%m-%d"),
        "currency": "USD",
        "rate": rate
    })

# Create DataFrame and save as CSV
fx_rates = pd.DataFrame(rows)
fx_rates.to_csv("data/fx_rates.csv", index=False)
print("FX rates dataset created!")
