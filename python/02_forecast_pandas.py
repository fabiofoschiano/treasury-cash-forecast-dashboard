# 02_forecast_pandas.py
# Forecast daily cash in EUR using Pandas

import pandas as pd
import matplotlib.pyplot as plt

# Load CSVs
transactions = pd.read_csv("data/transactions.csv")
fx = pd.read_csv("data/fx_rates.csv")

# Convert USD transactions to EUR using FX rates
transactions = transactions.merge(
    fx[['date', 'rate']],
    on='date',
    how='left'
)

# If currency is USD, convert; if EUR, keep amount
transactions['amount_eur'] = transactions.apply(
    lambda row: row['amount'] / row['rate'] if row['currency'] == 'USD' else row['amount'],
    axis=1
)

# Compute daily net cash
daily_cash = transactions.groupby('date').apply(
    lambda df: df.loc[df['type']=='inflow', 'amount_eur'].sum() -
               df.loc[df['type']=='outflow', 'amount_eur'].sum()
).reset_index(name='net')

print("Daily Cash (EUR):")
print(daily_cash)

# 7-Day simple forecast using average daily net flow
avg_daily_flow = daily_cash['net'].mean()
last_date = pd.to_datetime(daily_cash['date'].max())
forecast_dates = pd.date_range(last_date + pd.Timedelta(days=1), periods=7)

forecast = pd.DataFrame({
    'date': forecast_dates,
    'forecast': [daily_cash['net'].iloc[-1] + avg_daily_flow * (i+1) for i in range(7)]
})

print("\n7-Day Forecast (EUR):")
print(forecast)

# Plot forecast
plt.figure(figsize=(10,5))
plt.plot(pd.to_datetime(daily_cash['date']), daily_cash['net'], marker='o', label='Actual')
plt.plot(forecast['date'], forecast['forecast'], marker='x', linestyle='--', label='Forecast')
plt.xlabel("Date")
plt.ylabel("EUR Amount")
plt.title("Treasury Cash Forecast (EUR)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("treasury_forecast.png")
plt.show()
print("Plot saved as treasury_forecast.png")
