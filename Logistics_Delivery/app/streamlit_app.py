
from pathlib import Path
import sys

import pandas as pd
import streamlit as st

# Find the main project folder
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.data_loader import load_data, CLEAN_DATA_PATH
from src.data_cleaner import clean_data
from src.business_analysis import generate_kpis

st.set_page_config(
    page_title="Logistics Delivery Analytics",
    page_icon="🚚",
    layout="wide"
)

st.title("🚚 Logistics Delivery Performance & Cost Analytics")
st.write(
    "Analyze delivery delays, shipping costs, delivery partners "
    "and customer ratings."
)


@st.cache_data
def get_data():
    if CLEAN_DATA_PATH.exists():
        return pd.read_csv(CLEAN_DATA_PATH)

    return clean_data(load_data())


try:
    df = get_data()
except Exception as error:
    st.error(f"Unable to load the dataset: {error}")
    st.info("Check that data/raw/logistics_data.csv exists.")
    st.stop()


# Sidebar filters
st.sidebar.header("Filter Orders")

filtered_df = df.copy()

for column in ["warehouse", "shipping_mode", "delivery_partner"]:
    if column in filtered_df.columns:
        options = sorted(
            filtered_df[column].dropna().astype(str).unique()
        )

        selected = st.sidebar.multiselect(
            column.replace("_", " ").title(),
            options,
            default=options
        )

        filtered_df = filtered_df[
            filtered_df[column].astype(str).isin(selected)
        ]


# KPI cards
kpis = generate_kpis(filtered_df)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Orders", f"{kpis['total_orders']:,}")
col2.metric("Delayed Orders", f"{kpis['delayed_orders']:,}")
col3.metric("Delay Rate", f"{kpis['delay_rate_pct']}%")
col4.metric(
    "Total Logistics Cost",
    f"{kpis['total_logistics_cost']:,.2f}"
)

col5, col6, col7 = st.columns(3)

col5.metric("On-Time Rate", f"{kpis['on_time_rate_pct']}%")
col6.metric(
    "Average Order Cost",
    f"{kpis['average_order_cost']:,.2f}"
)

rating = kpis["average_customer_rating"]
col7.metric(
    "Average Customer Rating",
    "N/A" if rating is None else rating
)


# Delivery performance chart
st.subheader("Delivery Performance")

if "delivery_performance" in filtered_df.columns:
    performance = filtered_df["delivery_performance"].value_counts()
    st.bar_chart(performance)
else:
    st.warning("Delivery performance column is unavailable.")


# Cost and delay charts
left, right = st.columns(2)

with left:
    st.subheader("Average Cost by Shipping Mode")

    if {"shipping_mode", "total_logistics_cost"}.issubset(
        filtered_df.columns
    ):
        costs = filtered_df.groupby(
            "shipping_mode"
        )["total_logistics_cost"].mean()

        st.bar_chart(costs)
    else:
        st.info("Required shipping cost columns are unavailable.")

with right:
    st.subheader("Average Delay by Delivery Partner")

    if {"delivery_partner", "delivery_delay_days"}.issubset(
        filtered_df.columns
    ):
        delays = filtered_df.groupby(
            "delivery_partner"
        )["delivery_delay_days"].mean()

        st.bar_chart(delays)
    else:
        st.info("Required delivery delay columns are unavailable.")


# Display and download data
st.subheader("Order Details")

st.dataframe(filtered_df, use_container_width=True)

st.download_button(
    label="Download Filtered Data",
    data=filtered_df.to_csv(index=False).encode("utf-8"),
    file_name="logistics_filtered_data.csv",
    mime="text/csv"
)