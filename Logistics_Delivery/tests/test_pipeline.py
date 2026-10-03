
import pandas as pd

from src.data_cleaner import clean_data
from src.business_analysis import generate_kpis


def sample_data():
    return pd.DataFrame({
        "order_id": ["A1", "A2", "A2"],
        "order_date": [
            "2025-01-01", "2025-01-01", "2025-01-01"
        ],
        "expected_delivery_date": [
            "2025-01-03", "2025-01-03", "2025-01-03"
        ],
        "actual_delivery_date": [
            "2025-01-05", "2025-01-03", "2025-01-03"
        ],
        "shipping_cost": [100, 200, 200],
        "fuel_cost": [10, 20, 20],
        "distance_km": [50, 100, 100],
        "customer_rating": [3, 5, 5],
        "damage_flag": ["No", "Yes", "Yes"],
        "return_flag": ["No", "No", "No"]
    })


def test_duplicate_orders_are_removed():
    result = clean_data(sample_data())

    assert len(result) == 2
    assert result["order_id"].is_unique


def test_delivery_delay_calculation():
    result = clean_data(sample_data())

    first_order = result[result["order_id"] == "A1"].iloc[0]

    assert first_order["delivery_delay_days"] == 2


def test_total_logistics_cost():
    result = clean_data(sample_data())

    first_order = result[result["order_id"] == "A1"].iloc[0]

    assert first_order["total_logistics_cost"] == 110


def test_kpi_order_count():
    result = clean_data(sample_data())
    kpis = generate_kpis(result)

    assert kpis["total_orders"] == 2
    assert kpis["delayed_orders"] == 1


def test_zero_distance_cost_per_km():
    data = sample_data().iloc[:1].copy()
    data["distance_km"] = 0

    result = clean_data(data)

    assert pd.isna(result.loc[0, "cost_per_km"])