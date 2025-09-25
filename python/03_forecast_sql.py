# 03_forecast_sql.py
# Treasury cash forecast using Python + SQL (SQLite)

import pandas as pd
import sqlite3

# Load CSVs
transactions = pd.read_csv("data/transactions.csv")
fx_rates = pd.read_csv("data/fx_rates.csv")

# Connect to in-memory SQLite database
conn = sqlite3.connect(":memory:")

# Write tables to SQLite
transactions.to_sql("transactions", conn, index=False, if_exists="replace")
fx_rates.to_sql("fx_rates", conn, index=False, if_exists="replace")

# Build FX dictionary
fx_dict = pd.Series(fx_rates.rate.values, index=fx_rates.date).to_dict()

# Convert amounts to EUR safely
def convert_to_eur(row):
    if row["currency"] == "USD":
        # Use FX rate for date if available, otherwise last available rate
        rate = fx_dict.get(row["date"], list(fx_dict.values())[-1])
        return row["amount"] / rate
    else:
        return row["amount"]

transactions["amount_eur"] = transactions.apply(convert_to_eur, axis=1)

# Compute daily net cash
transactions["net"] = transactions.apply(
    lambda row: row["amount_eur"] if row["type"] == "inflow" else -row["amount_eur"],
    axis=1
)
daily_cash = transactions.groupby("date")[["net"]].sum().reset_index()

print("Daily Cash (EUR):")
print(daily_cash)

# Simple 7-day forecast
avg_daily_flow = daily_cash["net"].mean()
last_date = pd.to_datetime(daily_cash["date"].max())

forecast = []
for i in range(1, 8):
    forecast_date = last_date + pd.Timedelta(days=i)
    forecast_value = daily_cash["net"].iloc[-1] + avg_daily_flow * i
    forecast.append({"date": forecast_date.strftime("%Y-%m-%d"), "forecast": forecast_value})

forecast_df = pd.DataFrame(forecast)

print("\n7-Day Forecast (EUR):")
print(forecast_df)
