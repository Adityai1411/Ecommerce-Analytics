import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import os

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="E-commerce Analytics Dashboard",
    layout="wide"
)

# -----------------------------
# Load data (robust path)
# -----------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "ecommerce.db")

conn = sqlite3.connect(DB_PATH)
df = pd.read_sql("SELECT * FROM sales", conn)
conn.close()

# -----------------------------
# TITLE (VISIBLE IMMEDIATELY)
# -----------------------------
st.title("🛒 E-commerce Revenue, Customer & Product Analytics")
st.markdown(
    "An end-to-end business analytics dashboard built on real transactional data."
)

# -----------------------------
# KPI SECTION (ABOVE THE FOLD)
# -----------------------------
st.subheader("📊 Key Business KPIs")

total_revenue = df["revenue"].sum()

aov = (
    df.groupby("invoice_no")["revenue"]
    .sum()
    .mean()
)

total_customers = df["customer_id"].nunique()

returning_customers = (
    df.groupby("customer_id")["invoice_no"]
    .nunique()
    .gt(1)
    .sum()
)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Revenue (£)", f"{total_revenue:,.2f}")
col2.metric("Average Order Value (£)", f"{aov:,.2f}")
col3.metric("Total Customers", total_customers)
col4.metric("Returning Customers", returning_customers)

# -----------------------------
# Monthly Revenue Trend
# -----------------------------
st.subheader("📈 Monthly Revenue Trend")

monthly_rev = (
    df.groupby("order_month")["revenue"]
    .sum()
    .reset_index()
)

fig_month = px.line(
    monthly_rev,
    x="order_month",
    y="revenue",
    markers=True,
    title="Revenue Growth Over Time"
)
st.plotly_chart(fig_month, use_container_width=True)

# -----------------------------
# Top Customers (CLV)
# -----------------------------
st.subheader("👥 Top Customers by Lifetime Value")

top_customers = (
    df.groupby("customer_id")["revenue"]
    .sum()
    .reset_index()
    .sort_values(by="revenue", ascending=False)
    .head(10)
)

fig_cust = px.bar(
    top_customers,
    x="customer_id",
    y="revenue",
    title="Top 10 Customers by CLV"
)
st.plotly_chart(fig_cust, use_container_width=True)

# -----------------------------
# Top Products
# -----------------------------
st.subheader("📦 Top Products by Revenue")

top_products = (
    df.groupby("description")["revenue"]
    .sum()
    .reset_index()
    .sort_values(by="revenue", ascending=False)
    .head(10)
)

fig_prod = px.bar(
    top_products,
    x="revenue",
    y="description",
    orientation="h",
    title="Top 10 Products by Revenue"
)
st.plotly_chart(fig_prod, use_container_width=True)

# -----------------------------
# Revenue by Country
# -----------------------------
st.subheader("🌍 Revenue by Country")

country_rev = (
    df.groupby("country")["revenue"]
    .sum()
    .reset_index()
    .sort_values(by="revenue", ascending=False)
)

fig_country = px.bar(
    country_rev.head(10),
    x="country",
    y="revenue",
    title="Top Countries by Revenue"
)
st.plotly_chart(fig_country, use_container_width=True)
