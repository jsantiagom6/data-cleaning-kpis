# -*- coding: utf-8 -*-
"""
Created on Fri Jun  6 17:58:29 2025

@author: PCASUS
"""


import streamlit as st
import pandas as pd
import plotly.express as px


# Load the cleaned e-commerce data
df = pd.read_csv("ecommerce_clean_data.csv", parse_dates=["order_date"])

# Sidebar filters
st.sidebar.header("Filter Data")
cities = st.sidebar.multiselect("Select Cities:", options=df["city"].unique(), default=df["city"].unique())
categories = st.sidebar.multiselect("Select Categories:", options=df["category"].unique(), default=df["category"].unique())
date_range = st.sidebar.date_input("Select Date Range:", [df["order_date"].min(), df["order_date"].max()])

# Apply filters
filtered_df = df[
    (df["city"].isin(cities)) &
    (df["category"].isin(categories)) &
    (df["order_date"] >= pd.to_datetime(date_range[0])) &
    (df["order_date"] <= pd.to_datetime(date_range[1]))
]

# Main Dashboard
st.title("📊 Advanced E-commerce Sales Dashboard")

# KPIs
total_sales = filtered_df["total"].sum()
total_orders = filtered_df["order_id"].nunique()
avg_order_value = total_sales / total_orders if total_orders else 0
top_category = filtered_df.groupby("category")["total"].sum().idxmax()

# Mostrar KPIs en horizontal
kpi_cols = st.columns(4)
kpi_cols[0].metric("Total Sales", f"${total_sales:,.2f}")
kpi_cols[1].metric("Total Orders", f"{total_orders}")
kpi_cols[2].metric("Average Order Value", f"${avg_order_value:,.2f}")
kpi_cols[3].metric("Top Category", top_category)

st.markdown("---")

# Sales over time
sales_trend = filtered_df.groupby("order_date")["total"].sum().reset_index()
fig1 = px.line(sales_trend, x="order_date", y="total", title="Sales Over Time")

# Sales by City
sales_by_city = filtered_df.groupby("city")["total"].sum().reset_index()
fig2 = px.bar(sales_by_city, x="city", y="total", title="Sales by City")

# Mostrar gráficas en dos columnas
graph_cols = st.columns(2)
graph_cols[0].plotly_chart(fig1, use_container_width=True)
graph_cols[1].plotly_chart(fig2, use_container_width=True)

# Sales by Category
sales_by_cat = filtered_df.groupby("category")["total"].sum().reset_index()
fig3 = px.pie(sales_by_cat, names="category", values="total", title="Sales by Category")

# Top 10 Products
top_products = filtered_df.groupby("product")["total"].sum().reset_index().sort_values(by="total", ascending=False).head(10)
fig4 = px.bar(top_products, x="product", y="total", title="Top 10 Products")

# Mostrar gráficas en dos columnas
graph_cols2 = st.columns(2)
graph_cols2[0].plotly_chart(fig3, use_container_width=True)
graph_cols2[1].plotly_chart(fig4, use_container_width=True)


