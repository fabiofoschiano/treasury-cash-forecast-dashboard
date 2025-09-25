import pandas as pd
import matplotlib.pyplot as plt

# Load your SQL/ETL output CSVs or dataframes
transactions = pd.read_csv("data/transactions.csv")
fx = pd.read_csv("data/fx_rates.csv")

# Convert USD → EUR
fx_dict = dict(zip(fx['date'], fx['rate']))
transactions['amount_eur'] = transactions.apply(
    lambda row: row['amount'] / fx_dict.get(row['date'], 1) if row['currency'] == 'USD' else row['amount'],
    axis=1
)

# Compute daily cash
daily_cash = transactions.groupby('date').apply(
    lambda df: df.loc[df['type']=='inflow', 'amount_eur'].sum() - df.loc[df['type']=='outflow', 'amount_eur'].sum()
).reset_index(name='net')

# Simple 7-day forecast
last_date = pd.to_datetime(daily_cash['date'].iloc[-1])
avg_daily_flow = daily_cash['net'].mean()
forecast_dates = [last_date + pd.Timedelta(days=i) for i in range(1, 8)]
forecast_values = [daily_cash['net'].iloc[-1] + avg_daily_flow * i for i in range(1, 8)]
forecast_df = pd.DataFrame({'date': forecast_dates, 'forecast': forecast_values})

# Plot
plt.figure(figsize=(10,5))
plt.bar(daily_cash['date'], daily_cash['net'], label='Daily Cash (EUR)')
plt.plot(forecast_df['date'].dt.strftime('%Y-%m-%d'), forecast_df['forecast'], color='orange', marker='o', label='7-Day Forecast')
plt.xticks(rotation=45)
plt.ylabel('EUR')
plt.title('Treasury Cash Forecast')
plt.legend()
plt.tight_layout()
plt.savefig('treasury_forecast_chart.png')
plt.show()
