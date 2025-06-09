import os

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from app.data_preparation import load_data, prepare_usage_data

# Set seaborn style
sns.set(style="whitegrid")

# Load & prep data
customers, cars, subs, usage, maintenance = load_data()
usage_full = prepare_usage_data(subs, usage, cars)
maintenance_full = maintenance.merge(cars, left_on="car_id",right_on="id",suffixes=('','_car'))

# ----- 1. KM driven by brand -----
# Create output directory
output_dir = "../data/plots"
os.makedirs(output_dir, exist_ok=True)

def save_plot(fig, filename):
    fig.savefig(os.path.join(output_dir, filename), bbox_inches='tight')
    plt.close(fig)

# Plot functions
def plot_kms_per_brand():
    data = usage_full.groupby("brand")["km_driven"].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(10, 6))
    data.plot(kind="bar", ax=ax, color='skyblue', title="Total KM Driven per Brand")
    ax.set_ylabel("KM Driven")
    ax.set_xlabel("Brand")
    save_plot(fig, "kms_per_brand.png")

def plot_avg_km_by_type():
    data = usage_full.groupby("type")["km_driven"].mean().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(8, 6))
    data.plot(kind="bar", ax=ax, color='green', title="Average KM Driven by Type")
    ax.set_ylabel("Average KM")
    ax.set_xlabel("Type")
    save_plot(fig, "avg_km_by_type.png")

def plot_churn_by_month():
    subs["end_month"] = subs["end_date"].dt.to_period('M')
    data = subs.groupby("end_month").size()
    fig, ax = plt.subplots(figsize=(10, 6))
    data.plot(ax=ax, marker='o', title="Subscription Churn by Month")
    ax.set_ylabel("Churn Count")
    ax.set_xlabel("Month")
    save_plot(fig, "churn_by_month.png")

def plot_avg_maint_cost_by_type():
    data = maintenance_full.groupby('type')["cost"].mean().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(8, 6))
    data.plot(kind="bar", ax=ax, color='red', title="Average Maintenance Cost by Car Type")
    ax.set_ylabel("€ Cost")
    ax.set_xlabel("Car Type")
    save_plot(fig, "avg_maint_cost_by_type.png")

def plot_monthly_km_trend():
    data = usage_full.groupby("month")["km_driven"].sum()
    fig, ax = plt.subplots(figsize=(10, 6))
    data.plot(ax=ax, marker='o', title="Monthly KM Driven Trend")
    ax.set_ylabel("KM Driven")
    ax.set_xlabel("Month")
    save_plot(fig, "monthly_km_trend.png")

def plot_kms_by_customer():
    data = usage_full.groupby('customer_id')["km_driven"].sum().sort_values(ascending=False).head(20)
    fig, ax = plt.subplots(figsize=(12, 6))
    data.plot(kind="bar", ax=ax, title="Top 20 Customers by KM Driven", color='purple')
    ax.set_ylabel("KM Driven")
    ax.set_xlabel("Customer ID")
    save_plot(fig, "kms_by_customer.png")

def plot_maint_per_brand():
    data = maintenance_full.groupby('brand')['cost'].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(10, 6))
    data.plot(kind="bar", ax=ax, color='orange', title="Total Maintenance Cost per Brand")
    ax.set_ylabel("€ Cost")
    ax.set_xlabel("Brand")
    save_plot(fig, "maint_per_brand.png")

def plot_avg_duration_by_brand():
    subs["duration_days"] = (subs["end_date"] - subs["start_date"]).dt.days
    subs_with_cars = subs.merge(cars, left_on='car_id', right_on="id", suffixes=("","_car"))
    data = subs_with_cars.groupby("brand")["duration_days"].mean().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(10, 6))
    data.plot(kind="bar", ax=ax, color='teal', title="Average Subscription Duration by Brand")
    ax.set_ylabel("Duration (Days)")
    ax.set_xlabel("Brand")
    save_plot(fig, "avg_duration_by_brand.png")

def plot_monthly_maint_cost():
    maintenance["month"] = maintenance["date"].dt.to_period("M")
    data = maintenance.groupby("month")["cost"]
    fig, ax = plt.subplots(figsize=(10, 6))
    data.plot(ax=ax, marker='o', color='darkred', title="Monthly Maintenance Cost")
    ax.set_ylabel("€ Cost")
    ax.set_xlabel("Month")
    save_plot(fig, "monthly_maint_cost.png")



def plot_km_distribution():
    usage_by_sub = usage_full.groupby("subscription_id")["km_driven"].sum()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(usage_by_sub, bins=30, kde=True, ax=ax, color='cornflowerblue')
    ax.set_title("Distribution of KM Driven per Subscription")
    ax.set_xlabel("KM Driven")
    save_plot(fig, "km_distribution.png")

def plot_type_comparison():
    data = usage_full.groupby("type")["km_driven"].agg(["sum", "mean"])
    fig, ax = plt.subplots(figsize=(10, 6))
    data.plot(kind="bar", ax=ax, title="Total and Average KM Driven by Type")
    ax.set_ylabel("KM")
    save_plot(fig, "type_comparison.png")

if __name__ == '__main__':
    # Generate all plots
    plot_kms_per_brand()
    plot_avg_km_by_type()
    plot_churn_by_month()
    plot_avg_maint_cost_by_type()
    plot_monthly_km_trend()
    plot_kms_by_customer()
    plot_maint_per_brand()
    plot_avg_duration_by_brand()
    plot_monthly_maint_cost()
    plot_km_distribution()
    plot_type_comparison()
