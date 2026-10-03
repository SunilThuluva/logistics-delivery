
import pandas as pd


def generate_kpis(df):
    """Calculate the main logistics business metrics."""

    total_orders = len(df)

    if "delivery_delay_days" in df.columns:
        delay = df["delivery_delay_days"]
        known = delay.notna().sum()

        delayed = int((delay > 0).sum())
        on_time = int((delay == 0).sum())

        delay_rate = (
            delayed / known * 100 if known else 0
        )
        on_time_rate = (
            on_time / known * 100 if known else 0
        )
    else:
        delayed = 0
        on_time = 0
        delay_rate = 0
        on_time_rate = 0

    total_cost = (
        float(df["total_logistics_cost"].sum())
        if "total_logistics_cost" in df.columns
        else 0.0
    )

    average_rating = (
        df["customer_rating"].mean()
        if "customer_rating" in df.columns
        else float("nan")
    )

    damaged = (
        int(
            df["damage_flag"].astype("string")
            .str.lower().eq("yes").sum()
        )
        if "damage_flag" in df.columns
        else 0
    )

    returned = (
        int(
            df["return_flag"].astype("string")
            .str.lower().eq("yes").sum()
        )
        if "return_flag" in df.columns
        else 0
    )

    return {
        "total_orders": int(total_orders),
        "delayed_orders": delayed,
        "on_time_orders": on_time,
        "delay_rate_pct": round(delay_rate, 2),
        "on_time_rate_pct": round(on_time_rate, 2),
        "total_logistics_cost": round(total_cost, 2),
        "average_order_cost": round(
            total_cost / total_orders, 2
        ) if total_orders else 0,
        "average_customer_rating": (
            round(float(average_rating), 2)
            if pd.notna(average_rating)
            else None
        ),
        "damaged_orders": damaged,
        "returned_orders": returned
    }


def group_summary(df, group_col):
    """Summarize cost and delivery delays by category."""

    if group_col not in df.columns:
        raise KeyError(f"Column '{group_col}' does not exist.")

    if "order_id" in df.columns:
        order_counts = ("order_id", "count")
    else:
        order_counts = (group_col, "size")

    summary = df.groupby(
        group_col, dropna=False
    ).agg(
        orders=order_counts,
        average_total_cost=("total_logistics_cost", "mean"),
        average_delay_days=("delivery_delay_days", "mean"),
        delayed_orders=(
            "delivery_delay_days",
            lambda values: int((values > 0).sum())
        )
    ).reset_index()

    summary["delay_rate_pct"] = (
        summary["delayed_orders"]
        / summary["orders"].replace(0, float("nan"))
        * 100
    ).fillna(0).round(2)

    return summary.sort_values(
        "orders", ascending=False
    )