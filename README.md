**Treasury Cash Forecast Dashboard**

This project demonstrates treasury analytics using Python, SQL, and Power BI/Tableau. It generates synthetic cash transactions and FX rates, calculates daily cash balances, and produces a simple 7-day cash forecast in EUR.

**Project Structure**

data/

transactions.csv – synthetic transactions

fx_rates.csv – FX rates

python/

01_forecast.py – basic CSV-based ETL & forecast

02_forecast_pandas.py – pandas-based ETL & forecast

03_forecast_sql.py – SQL-based ETL & forecast

03_generate_data.py – generate synthetic transactions in SQLite

04_forecast_chart.py – plot daily cash and forecast

04_generate_fx.py – generate synthetic FX rates

generate_transactions.py – generate synthetic transactions

sql/ – SQL scripts (optional)
powerbi/ – Power BI dashboards (treasury_forecast.pbix)
tableau/ – Tableau dashboards
treasury_forecast.db – SQLite database

**How to Run**

**Generate synthetic data:**

python python/generate_transactions.py
python python/04_generate_fx.py


**Run ETL and forecasting scripts:**

python python/01_forecast.py
python python/02_forecast_pandas.py
python python/03_forecast_sql.py
python python/04_forecast_chart.py


**Outputs:**

Daily cash balances in EUR

7-day simple forecast in EUR

Plots saved as treasury_forecast.png
