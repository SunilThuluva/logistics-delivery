
from pathlib import Path

from src.data_loader import load_data, save_data, PROJECT_ROOT
from src.data_cleaner import clean_data
from src.business_analysis import generate_kpis, group_summary
from src.visualization import create_charts


def main():
    # Step 1: Load the original CSV
    raw_df = load_data()
    print("Original dataset shape:", raw_df.shape)

    # Step 2: Clean the data
    cleaned_df = clean_data(raw_df)

    # Step 3: Save cleaned data
    clean_path = save_data(cleaned_df)

    # Step 4: Create output folder
    output_dir = PROJECT_ROOT / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Step 5: Calculate business KPIs
    kpis = generate_kpis(cleaned_df)

    report_path = output_dir / "kpi_summary.txt"
    report_path.write_text(
        "\n".join(f"{key}: {value}" for key, value in kpis.items()),
        encoding="utf-8"
    )

    print("\nBUSINESS KPIs")
    for name, value in kpis.items():
        print(f"{name}: {value}")

    # Step 6: Create category-wise summaries
    categories = [
        "shipping_mode",
        "delivery_partner",
        "warehouse",
        "product_category"
    ]

    for column in categories:
        if column in cleaned_df.columns:
            summary = group_summary(cleaned_df, column)
            summary.to_csv(
                output_dir / f"summary_by_{column}.csv",
                index=False
            )

    # Step 7: Generate charts
    create_charts(cleaned_df, output_dir / "charts")

    print("\nPipeline completed successfully!")
    print("Cleaned data:", clean_path)
    print("Reports and charts:", output_dir)


if __name__ == "__main__":
    main()