
import numpy as np
import pandas as pd


DATE_COLUMNS = [
    "order_date",
    "dispatch_date",
    "expected_delivery_date",
    "actual_delivery_date"
]

NUMERIC_COLUMNS = [
    "distance_km",
    "quantity",
    "weight_kg",
    "shipping_cost",
    "fuel_cost",
    "warehouse_processing_hours",
    "customer_rating"
]


def clean_data(df):
    """Clean records and calculate delivery and cost features."""
    data = df.copy()

    # Standardize column names
    data.columns = [
        str(column).strip().lower().replace(" ", "_")
        for column in data.columns
    ]

    # Remove unnecessary spaces in text values
    for column in data.select_dtypes(include=["object"]).columns:
        data[column] = data[column].map(
            lambda value: value.strip()
            if isinstance(value, str) else value
        )

        data[column] = data[column].replace(
            {"": np.nan, "NA": np.nan, "N/A": np.nan}
        )

    # Convert date columns
    for column in DATE_COLUMNS:
        if column in data.columns:
            data[column] = pd.to_datetime(
                data[column], errors="coerce"
            )

    # Convert numeric columns
    for column in NUMERIC_COLUMNS:
        if column in data.columns:
            data[column] = pd.to_numeric(
                data[column], errors="coerce"
            )

    # Remove duplicate orders
    if "order_id" in data.columns:
        data = data.drop_duplicates(
            subset=["order_id"], keep="first"
        )
        data = data.dropna(subset=["order_id"])
    else:
        data = data.drop_duplicates()

    # Invalid negative measurements become missing
    for column in [
        "distance_km", "quantity", "weight_kg",
        "shipping_cost", "fuel_cost",
        "warehouse_processing_hours"
    ]:
        if column in data.columns:
            data.loc[data[column] < 0, column] = np.nan

    # Calculate delivery delay
    if {
        "actual_delivery_date",
        "expected_delivery_date"
    }.issubset(data.columns):
        data["delivery_delay_days"] = (
            data["actual_delivery_date"]
            - data["expected_delivery_date"]
        ).dt.days
    else:
        data["delivery_delay_days"] = np.nan

    # Calculate total logistics cost
    if {
        "shipping_cost", "fuel_cost"
    }.issubset(data.columns):
        data["total_logistics_cost"] = (
            data["shipping_cost"].fillna(0)
            + data["fuel_cost"].fillna(0)
        )
    else:
        data["total_logistics_cost"] = np.nan

    # Cost per kilometre
    if {
        "total_logistics_cost", "distance_km"
    }.issubset(data.columns):
        distance = data["distance_km"].replace(0, np.nan)

        data["cost_per_km"] = (
            data["total_logistics_cost"] / distance
        )
    else:
        data["cost_per_km"] = np.nan

    # Calculate order-to-delivery duration
    if {
        "order_date", "actual_delivery_date"
    }.issubset(data.columns):
        data["order_to_delivery_days"] = (
            data["actual_delivery_date"] - data["order_date"]
        ).dt.days
    else:
        data["order_to_delivery_days"] = np.nan

    # Classify delivery performance
    if "delivery_delay_days" in data.columns:
        delay = data["delivery_delay_days"]

        data["delivery_performance"] = np.select(
            [
                delay.isna(),
                delay > 0,
                delay == 0
            ],
            [
                "Unknown",
                "Delayed",
                "On Time"
            ],
            default="Early"
        )

    # Standardize damage and return flags
    for column in ["damage_flag", "return_flag"]:
        if column in data.columns:
            data[column] = (
                data[column].astype("string").str.strip().str.title()
            )

    return data.reset_index(drop=True)