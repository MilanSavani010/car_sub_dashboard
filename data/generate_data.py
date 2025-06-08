import sqlite3
import random
from faker import Faker
import pandas as pd
from datetime import datetime, timedelta

DB = "../db/finn.db"

def generate_simulated_data():
    fake = Faker()
    conn = sqlite3.connect(DB)
    cur = conn.cursor()


    cur.executescript(
        """
        DROP TABLE IF EXISTS customers;
        DROP TABLE IF EXISTS cars;
        DROP TABLE IF EXISTS subscriptions;
        DROP TABLE IF EXISTS usage;
        DROP TABLE IF EXISTS maintenance;
    
        CREATE TABLE customers (
            id INTEGER PRIMARY KEY,
            region TEXT
        );
    
        CREATE TABLE cars (
            id INTEGER PRIMARY KEY,
            brand TEXT,
            model TEXT,
            type TEXT
        );
    
        CREATE TABLE subscriptions (
            id INTEGER PRIMARY KEY,
            customer_id INTEGER,
            car_id INTEGER,
            start_date TEXT,
            end_date TEXT
        );
    
        CREATE TABLE usage (
            id INTEGER PRIMARY KEY,
            subscription_id INTEGER,
            month TEXT,
            km_driven INTEGER
        );
    
        CREATE TABLE maintenance (
            id INTEGER PRIMARY KEY,
            car_id INTEGER,
            date TEXT,
            cost REAL
        );
    """
    )

    regions = ['Berlin', 'Munich', 'Frankfurt', 'Hamburg']
    brands_models = [
        ('Tesla', 'Model 3', 'EV'),
        ('BMW', 'X5', 'Hybrid'),
        ('VW', 'Golf', 'Gas'),
        ('Audi', 'A4', 'Gas'),
        ('Hyundai', 'Ioniq 5', 'EV'),
    ]

    # Insert customers
    customers = [(i, random.choice(regions)) for i in range(1, 101)]
    cur.executemany("INSERT INTO customers VALUES (?, ?)", customers)

    # Insert cars
    cars = [(i+1, brand, model, ctype) for i, (brand, model, ctype) in enumerate(brands_models)]
    cur.executemany("INSERT INTO cars VALUES (?, ?, ?, ?)", cars)


    subs = []
    for i in range(1, 151):
        cust_id = random.randint(1, 100)
        car_id = random.randint(1, 5)
        start = fake.date_between(start_date='-12m', end_date='-1m')
        duration_months = random.randint(3, 12)
        end = start + timedelta(days=30 * duration_months)
        subs.append((i, cust_id, car_id, start.isoformat(), end.isoformat()))

    cur.executemany("INSERT INTO subscriptions VALUES (?, ?, ?, ?, ?)", subs)

    # Insert usage
    usage_data = []
    for sub_id, _, _, start, end in subs:
        start_month = datetime.fromisoformat(start).replace(day=1)
        end_month = datetime.fromisoformat(end).replace(day=1)
        months = (end_month.year - start_month.year) * 12 + (end_month.month - start_month.month)
        for i in range(months + 1):
            month_date = (start_month + timedelta(days=30 * i)).strftime('%Y-%m')
            km = random.randint(500, 2000)
            usage_data.append((None, sub_id, month_date, km))

    cur.executemany("INSERT INTO usage VALUES (?, ?, ?, ?)", usage_data)

    # Insert maintenance
    maintenance_data = [
        (None, random.randint(1, 5), fake.date_between('-12m', 'today').isoformat(), round(random.uniform(100, 1000), 2))
        for _ in range(50)
    ]
    cur.executemany("INSERT INTO maintenance VALUES (?, ?, ?, ?)", maintenance_data)

    conn.commit()
    conn.close()

def main():
    generate_simulated_data()

if __name__ == '__main__':
    main()