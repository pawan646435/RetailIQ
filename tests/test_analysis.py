import pandas as pd
from src.data_cleaning import clean_data
from src.analysis import kpis, customer_summary, build_insights


def sample():
    return pd.DataFrame({
        "Order ID": ["A", "A", "B"], "Order Date": ["2024-01-01", "2024-01-01", "2024-02-01"],
        "Ship Date": ["2024-01-03", "2024-01-03", "2024-02-04"], "Customer ID": ["C1", "C1", "C2"],
        "Customer Name": ["One", "One", "Two"], "Region": ["East", "East", "West"],
        "Category": ["Tech", "Tech", "Office"], "Sub-Category": ["Phones", "Phones", "Paper"],
        "Product Name": ["P1", "P1", "P2"], "Sales": [100, 50, 25], "Quantity": [1, 1, 1],
        "Discount": [0, .1, 0], "Profit": [20, -5, 5], "Ship Mode": ["Fast", "Fast", "Standard"]
    })


def test_cleaning_preserves_negative_profit_and_derives_fields():
    df, report = clean_data(sample())
    assert len(df) == 3
    assert (df.profit < 0).sum() == 1
    assert "month_year" in df and "shipping_duration" in df
    assert report["negative_profit_rows_retained"] == 1


def test_kpis_count_distinct_orders_not_rows():
    df, _ = clean_data(sample())
    result = kpis(df)
    assert result["orders"] == 2
    assert result["revenue"] == 175
    assert result["aov"] == 87.5


def test_customer_summary_classifies_repeat_customers():
    raw = sample()
    raw.loc[1, "Order ID"] = "A2"
    df, _ = clean_data(raw)
    summary = customer_summary(df)
    assert summary.loc[summary.customer_id == "C1", "customer_type"].iloc[0] == "Repeat"


def test_insights_handles_empty_data():
    assert "No records" in build_insights(pd.DataFrame())[0]
