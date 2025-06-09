import pandas as pd
import sqlite3
import os

DB = "../db/finn.db"


def load_data(db_path=DB):
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database not found at: {db_path}")

    conn = sqlite3.connect(db_path)
    customers = pd.read_sql("SELECT * FROM customers", conn)
    cars = pd.read_sql("SELECT * FROM cars", conn)
    subs = pd.read_sql("SELECT * FROM subscriptions", conn, parse_dates=["start_date", "end_date"])
    usage = pd.read_sql("SELECT * FROM usage", conn)
    maintenance = pd.read_sql("SELECT * FROM maintenance", conn, parse_dates=["date"])
    conn.close()

    # basic cleaning of data
    # remove duplicates
    customers.drop_duplicates(inplace=True)
    cars.drop_duplicates(inplace=True)
    subs.drop_duplicates(inplace=True)
    usage.drop_duplicates(inplace=True)
    maintenance.drop_duplicates(inplace=True)

    # remove missing values
    subs = subs.dropna(subset=["customer_id", "car_id", "start_date", "end_date"])
    usage = usage.dropna(subset=["subscription_id", "month", "km_driven"])
    maintenance = maintenance.dropna(subset=["car_id", "date", "cost"])

    # Ensure correct data types
    usage["km_driven"] = pd.to_numeric(usage["km_driven"], errors="coerce").fillna(0)
    maintenance["cost"] = pd.to_numeric(maintenance["cost"], errors="coerce").fillna(0)

    # Remove invalid values
    usage = usage[usage["km_driven"] >= 0]
    maintenance = maintenance[maintenance["cost"] >= 0]

    return customers, cars, subs, usage, maintenance

def prepare_usage_data(subs,usage,cars):
    # usage is left table
    # subs is right table
    # join with comparison of subscription_id (in usage) and id (in subs) table
    usage_full = usage.merge(subs, left_on="subscription_id", right_on="id", suffixes=('', '_sub'))
    usage_full = usage_full.merge(cars,left_on="car_id",right_on="id",suffixes=('','_car'))
    # conversion of month to datetime format
    usage_full['year_month'] = pd.to_datetime(usage_full['month'] + "-01", errors='coerce')
    usage_full = usage_full.dropna(subset=['year_month'])  # Drop rows with bad dates
    return usage_full

