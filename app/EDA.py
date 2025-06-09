import os

import pandas as pd
from data_preparation import load_data, prepare_usage_data

customers, cars, subs, usage, maintenance = load_data()
usage_full = prepare_usage_data(subs, usage, cars)

data = "../data/csv"
os.makedirs(data, exist_ok=True)


maintenance_full = maintenance.merge(cars, left_on="car_id",right_on="id",suffixes=('','_car'))

print('customers')
print(customers.columns)
print('cars')
print(cars.columns)
print('subs')
print(subs.columns)
print('usage')
print(usage.columns)
print('maintenance')
print(maintenance.columns)
print('usage_full')
print(usage_full.columns)
print("mainatenance full")
print(maintenance_full.columns)



kms_per_brand = usage_full.groupby("brand")["km_driven"].sum().sort_values(ascending=False)
avg_km_by_type = usage_full.groupby("type")["km_driven"].mean().sort_values(ascending=False)

subs["end_month"] = subs['end_date'].dt.to_period('M')
churn_by_month = subs.groupby("end_month").size()

avg_maint_cost_by_type = maintenance_full.groupby('type')["cost"].mean().sort_values(ascending=False)

monthly_km_trend = usage_full.groupby("month")["km_driven"].sum()

kms_by_customer = usage_full.groupby('customer_id')["km_driven"].sum().sort_values(ascending=False)

monthly_km_trend_by_customer = usage_full.groupby(['month','customer_id'])["km_driven"].sum()

maint_per_brand = maintenance_full.groupby('brand')['cost'].sum().sort_values(ascending=False)

subs["duration_days"] = (subs["end_date"] - subs["start_date"]).dt.days
avg_sub_duration = subs.groupby("customer_id")["duration_days"].mean().sort_values(ascending=False)

repeat_customers = subs["customer_id"].value_counts()
repeat_rate = (repeat_customers > 1).sum() / len(repeat_customers)

avg_duration = subs["duration_days"].mean()

subs_with_cars = subs.merge(cars, left_on='car_id',right_on="id",suffixes=("","_car"))
avg_duration_by_brand = subs_with_cars.groupby("brand")["duration_days"].mean().sort_values(ascending=False)

duration_distribution = subs["duration_days"].describe()

maintenance["month"] = maintenance["date"].dt.to_period("M")
monthly_maint_cost = maintenance.groupby("month")["cost"].sum()

top_maintenance = maintenance.sort_values("cost", ascending=False).head(5)

usage_by_sub = usage_full.groupby("subscription_id")["km_driven"].sum()
km_distribution = usage_by_sub.describe()

type_comparison = usage_full.groupby("type")["km_driven"].agg(["sum", "mean"])

kms_per_brand.to_csv(f"{data}/kms_per_brand.csv")
avg_km_by_type.to_csv(f"{data}/avg_km_by_type.csv")
churn_by_month.to_csv(f"{data}/churn_by_month.csv")
avg_maint_cost_by_type.to_csv(f"{data}/avg_maint_cost_by_type.csv")
monthly_km_trend.to_csv(f"{data}/monthly_km_trend.csv")
kms_by_customer.to_csv(f"{data}/kms_by_customer.csv")
monthly_km_trend_by_customer.to_csv(f"{data}/monthly_km_trend_by_customer.csv")
maint_per_brand.to_csv(f"{data}/maint_per_brand.csv")
avg_sub_duration.to_csv(f"{data}/avg_sub_duration.csv")
subs[["customer_id", "duration_days"]].to_csv(f"{data}/customer_duration_days.csv", index=False)
pd.Series({"repeat_rate": repeat_rate}).to_csv(f"{data}/repeat_rate.csv")
pd.Series({"avg_duration": avg_duration}).to_csv(f"{data}/avg_duration.csv")
avg_duration_by_brand.to_csv(f"{data}/avg_duration_by_brand.csv")
duration_distribution.to_csv(f"{data}/duration_distribution.csv")
monthly_maint_cost.to_csv(f"{data}/monthly_maint_cost.csv")
top_maintenance.to_csv(f"{data}/top_maintenance.csv", index=False)
usage_by_sub.to_csv(f"{data}/usage_by_sub.csv")
km_distribution.to_csv(f"{data}/km_distribution.csv")
type_comparison.to_csv(f"{data}/type_comparison.csv")