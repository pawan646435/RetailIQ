
from pathlib import Path

import pandas as pd

from src.analysis import (
    kpis,
    monthly_trend,
    customer_summary,
    build_insights,
)
from src.visualizations import save_eda_charts


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "processed" / "superstore_cleaned.csv"
REPORT_DIR = ROOT / "reports"

REPORT_DIR.mkdir(parents=True, exist_ok=True)


def main():
    print("\n" + "=" * 55)
    print("          RETAILIQ - EXPLORATORY DATA ANALYSIS")
    print("=" * 55)

    # 1. Load cleaned dataset
    df = pd.read_csv(DATA_PATH)

    print(f"\nDataset shape: {df.shape}")

    # 2. Overall KPIs
    metrics = kpis(df)

    print("\n--- BUSINESS PERFORMANCE ---")
    for key, value in metrics.items():
        print(f"{key.upper():20}: {value:,.2f}")

    # 3. Category analysis
    print("\n--- CATEGORY PERFORMANCE ---")
    category = (
        df.groupby("category")
        .agg(
            sales=("sales", "sum"),
            profit=("profit", "sum"),
        )
        .sort_values("sales", ascending=False)
    )
    print(category.to_string())

    category.to_csv(REPORT_DIR / "category_analysis.csv")

    # 4. Top 10 products
    print("\n--- TOP 10 PRODUCTS BY REVENUE ---")
    top_products = (
        df.groupby("product_name")["sales"]
        .sum()
        .nlargest(10)
    )
    print(top_products.to_string())

    top_products.to_csv(REPORT_DIR / "top_products.csv")

    # 5. Regional analysis
    print("\n--- REGIONAL PERFORMANCE ---")
    regional = (
        df.groupby("region")
        .agg(
            sales=("sales", "sum"),
            profit=("profit", "sum"),
        )
        .sort_values("sales", ascending=False)
    )
    print(regional.to_string())

    regional.to_csv(REPORT_DIR / "regional_analysis.csv")

    # 6. Customer analysis
    customers = customer_summary(df)

    print("\n--- CUSTOMER ANALYSIS ---")
    print(f"Total customers: {len(customers)}")
    print(
        customers["customer_type"]
        .value_counts()
        .to_string()
    )

    customers.to_csv(
        REPORT_DIR / "customer_analysis.csv",
        index=False,
    )

    # 7. Monthly trend
    monthly = monthly_trend(df)

    monthly.to_csv(
        REPORT_DIR / "monthly_trends.csv",
        index=False,
    )

    # 8. Dynamic business insights
    insights = build_insights(df)

    print("\n--- BUSINESS INSIGHTS ---")
    for i, insight in enumerate(insights, 1):
        print(f"{i}. {insight}")

    # 9. Save charts
    charts = save_eda_charts(df, REPORT_DIR / "figures")

    print("\n--- GENERATED CHARTS ---")
    for chart in charts:
        print(chart)

    print("\nEDA COMPLETED SUCCESSFULLY!")
    print(f"Reports saved in: {REPORT_DIR}")


if __name__ == "__main__":
    main()
