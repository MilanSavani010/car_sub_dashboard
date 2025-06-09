import streamlit as st
import pandas as pd
import plotly.express as px

data = "../data/csv"

# Load data from CSVs
kms_per_brand = pd.read_csv(f"{data}/kms_per_brand.csv", index_col=0)
avg_km_by_type = pd.read_csv(f"{data}/avg_km_by_type.csv", index_col=0)
churn_by_month = pd.read_csv(f"{data}/churn_by_month.csv", index_col=0)
avg_maint_cost_by_type = pd.read_csv(f"{data}/avg_maint_cost_by_type.csv", index_col=0)
monthly_km_trend = pd.read_csv(f"{data}/monthly_km_trend.csv", index_col=0)
kms_by_customer = pd.read_csv(f"{data}/kms_by_customer.csv", index_col=0)
monthly_km_trend_by_customer = pd.read_csv(f"{data}/monthly_km_trend_by_customer.csv")
maint_per_brand = pd.read_csv(f"{data}/maint_per_brand.csv", index_col=0)
avg_sub_duration = pd.read_csv(f"{data}/avg_sub_duration.csv", index_col=0)
duration_days = pd.read_csv(f"{data}/customer_duration_days.csv")
repeat_rate = pd.read_csv(f"{data}/repeat_rate.csv", index_col=0)
avg_duration = pd.read_csv(f"{data}/avg_duration.csv", index_col=0)
avg_duration_by_brand = pd.read_csv(f"{data}/avg_duration_by_brand.csv", index_col=0)
duration_distribution = pd.read_csv(f"{data}/duration_distribution.csv")
monthly_maint_cost = pd.read_csv(f"{data}/monthly_maint_cost.csv", index_col=0)
top_maintenance = pd.read_csv(f"{data}/top_maintenance.csv")
usage_by_sub = pd.read_csv(f"{data}/usage_by_sub.csv", index_col=0)
km_distribution = pd.read_csv(f"{data}/km_distribution.csv")
type_comparison = pd.read_csv(f"{data}/type_comparison.csv")

# Sidebar filters
st.sidebar.header("Filters")
selected_month = st.sidebar.selectbox("Select Month for Trends", monthly_km_trend.index.astype(str).tolist())

# Streamlit dashboard
st.title(" FINN Data Analytics Dashboard")

# Overview KPIs
st.markdown("### Overview Metrics")
col1, col2 = st.columns(2)
col1.metric("Repeat Customer Rate", f"{repeat_rate.iloc[0,0]*100:.2f}%")
col2.metric("Avg Subscription Duration", f"{avg_duration.iloc[0,0]:.1f} days")

# Usage Insights
st.markdown("---")
st.markdown("###  Usage Insights")

with st.expander("Total KM Driven by Brand"):
    st.plotly_chart(px.bar(kms_per_brand, x=kms_per_brand.index, y="km_driven", title="KM per Brand", labels={'km_driven': 'Kilometers Driven'}))

with st.expander("Average KM by Car Type"):
    st.plotly_chart(px.bar(avg_km_by_type, x=avg_km_by_type.index, y="km_driven", title="Avg KM by Car Type"))

with st.expander("Monthly KM Trend"):
    monthly_km_trend.index = monthly_km_trend.index.astype(str)
    fig = px.line(monthly_km_trend, x=monthly_km_trend.index, y="km_driven", title="Monthly KM Trend")
    fig.add_vline(x=selected_month, line_width=2, line_dash="dash", line_color="green")
    st.plotly_chart(fig)

# Subscription Analytics
st.markdown("---")
st.markdown("###  Subscription Analytics")

with st.expander("Churn by Month"):
    churn_by_month.index = churn_by_month.index.astype(str)
    st.plotly_chart(px.line(churn_by_month, x=churn_by_month.index, y="0", title="Churn by Month"))

with st.expander("Avg Subscription Duration by Brand"):
    st.plotly_chart(px.bar(avg_duration_by_brand, x=avg_duration_by_brand.index, y="duration_days", title="Avg Duration by Brand"))

with st.expander("Subscription Duration Distribution"):
    st.write(duration_distribution)
    st.plotly_chart(px.histogram(duration_days, x="duration_days", nbins=30, title="Subscription Duration Histogram"))

# Maintenance Insights
st.markdown("---")
st.markdown("### Maintenance Analysis")

with st.expander("Monthly Maintenance Cost"):
    monthly_maint_cost.index = monthly_maint_cost.index.astype(str)
    st.plotly_chart(px.line(monthly_maint_cost, x=monthly_maint_cost.index, y="cost", title="Monthly Maintenance Cost"))

with st.expander("Avg Maintenance Cost by Car Type"):
    st.plotly_chart(px.bar(avg_maint_cost_by_type, x=avg_maint_cost_by_type.index, y="cost", title="Avg Maintenance Cost by Type"))

with st.expander("Maintenance Cost by Brand"):
    st.plotly_chart(px.bar(maint_per_brand, x=maint_per_brand.index, y="cost", title="Maintenance Cost per Brand"))

with st.expander("Top 5 Maintenance Cases"):
    st.dataframe(top_maintenance)

# KM Distribution
st.markdown("---")
st.markdown("### Kilometer Distribution")
with st.expander("KM Driven per Subscription"):
    st.plotly_chart(px.box(usage_by_sub, y="km_driven", title="KM Driven Distribution"))
