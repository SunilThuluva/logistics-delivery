
from pathlib import Path

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt


def create_charts(df, output_dir):
    """Generate charts and save them as PNG files."""

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Chart 1: Delivery performance
    if "delivery_performance" in df.columns:
        counts = df["delivery_performance"].value_counts()

        fig, ax = plt.subplots(figsize=(8, 5))
        counts.plot(kind="bar", ax=ax)

        ax.set_title("Delivery Performance")
        ax.set_xlabel("Performance")
        ax.set_ylabel("Number of Orders")
        fig.tight_layout()

        fig.savefig(
            output_dir / "delivery_performance.png",
            dpi=150
        )
        plt.close(fig)

    # Chart 2: Average cost by shipping mode
    if {
        "shipping_mode", "total_logistics_cost"
    }.issubset(df.columns):
        costs = df.groupby(
            "shipping_mode"
        )["total_logistics_cost"].mean().sort_values(
            ascending=False
        )

        fig, ax = plt.subplots(figsize=(8, 5))
        costs.plot(kind="bar", ax=ax)

        ax.set_title("Average Logistics Cost by Shipping Mode")
        ax.set_xlabel("Shipping Mode")
        ax.set_ylabel("Average Cost")
        fig.tight_layout()

        fig.savefig(
            output_dir / "cost_by_shipping_mode.png",
            dpi=150
        )
        plt.close(fig)

    # Chart 3: Average delay by delivery partner
    if {
        "delivery_partner", "delivery_delay_days"
    }.issubset(df.columns):
        delays = df.groupby(
            "delivery_partner"
        )["delivery_delay_days"].mean().sort_values(
            ascending=False
        )

        fig, ax = plt.subplots(figsize=(9, 5))
        delays.plot(kind="bar", ax=ax)

        ax.set_title("Average Delivery Delay by Partner")
        ax.set_xlabel("Delivery Partner")
        ax.set_ylabel("Average Delay in Days")
        fig.tight_layout()

        fig.savefig(
            output_dir / "delay_by_partner.png",
            dpi=150
        )
        plt.close(fig)