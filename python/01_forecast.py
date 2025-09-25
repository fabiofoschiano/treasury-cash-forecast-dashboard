# 01_forecast.py
# Simple ETL & FX forecast example

# --- Read transactions CSV (quoted format) ---
transactions = []
with open('data/transactions.csv', 'r', encoding='utf-8-sig') as f:
    lines = f.read().splitlines()
    for line in lines[1:]:  # skip header
        line = line.strip('"')  # remove outer quotes
        parts = line.split(',')  # split inside quotes
        tx = {
            'id': parts[0],
            'date': parts[1],
            'amount': float(parts[2]),
            'currency': parts[3],
            'type': parts[4]
        }
        transactions.append(tx)

# --- Read FX rates CSV (quoted format) ---
fx_rates = []
with open('data/fx_rates.csv', 'r', encoding='utf-8-sig') as f:
    lines = f.read().splitlines()
    for line in lines[1:]:  # skip header
        line = line.strip('"')  # remove outer quotes
        parts = line.split(',')
        fx = {
            'id': parts[0],
            'date': parts[1],
            'currency': parts[2],
            'rate': float(parts[3])
        }
        fx_rates.append(fx)

# --- Convert all transactions to EUR ---
for tx in transactions:
    if tx["currency"] == "USD":
        rate = next(fx["rate"] for fx in fx_rates if fx["date"] == tx["date"])
        tx["amount_eur"] = tx["amount"] / rate
    else:
        tx["amount_eur"] = tx["amount"]

# --- Print forecast ---
print("Date       | EUR Amount | Type")
print("-------------------------------")
for tx in transactions:
    print(f"{tx['date']} | {tx['amount_eur']:.2f}     | {tx['type']}")

# --- Print forecast ---
print("Date       | EUR Amount | Type")
print("-------------------------------")
for tx in transactions:
    print(f"{tx['date']} | {tx['amount_eur']:.2f}     | {tx['type']}")

# --- Add this code here ---
# Compute daily net cash in EUR
from collections import defaultdict

daily_cash = defaultdict(float)
for tx in transactions:
    if tx['type'] == 'inflow':
        daily_cash[tx['date']] += tx['amount_eur']
    else:
        daily_cash[tx['date']] -= tx['amount_eur']

# Simple 7-day forecast assuming average daily net flow
dates = sorted(daily_cash.keys())
avg_daily_flow = sum(daily_cash[d] for d in dates) / len(dates)
last_date = dates[-1]

print("\nForecast for next 7 days (EUR):")
for i in range(1, 8):
    forecast_date = f"2025-01-{int(last_date.split('-')[2])+i:02d}"
    forecast_value = daily_cash[last_date] + avg_daily_flow * i
    print(f"{forecast_date} | {forecast_value:.2f}")

