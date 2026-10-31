import pandas as pd
import numpy as np

COLUMN_MAP = {
    "Row ID": "row_id", "Order ID": "order_id", "Order Date": "order_date",
    "Ship Date": "ship_date", "Ship Mode": "ship_mode", "Customer ID": "customer_id",
    "Customer Name": "customer_name", "Segment": "segment", "Country": "country",
    "City": "city", "State": "state", "Postal Code": "postal_code", "Region": "region",
    "Product ID": "product_id", "Category": "category", "Sub-Category": "sub_category",
    "Product Name": "product_name", "Sales": "sales", "Quantity": "quantity",
    "Discount": "discount", "Profit": "profit"
}
REQUIRED = ["order_id", "order_date", "ship_date", "customer_id", "region", "category", "sales", "quantity", "discount", "profit"]


def clean_data(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Standardize and validate rows without silently dropping suspicious records."""
    out = df.copy()
    out.columns = [str(c).strip() for c in out.columns]
    out = out.rename(columns=COLUMN_MAP)
    out.columns = [c.strip().lower().replace(" ", "_") for c in out.columns]
    missing_cols = [c for c in REQUIRED if c not in out.columns]
    if missing_cols:
        raise ValueError(f"Dataset is missing required columns: {missing_cols}")

    report = {"rows_before": len(out), "duplicate_rows": int(out.duplicated().sum()),
              "missing_before": out.isna().sum().to_dict()}
    # Exact duplicate transaction lines are removed; no business rows are removed for negative profit.
    out = out.drop_duplicates().copy()
    out["order_date"] = pd.to_datetime(out["order_date"], errors="coerce")
    out["ship_date"] = pd.to_datetime(out["ship_date"], errors="coerce")
    for col in ["sales", "profit", "quantity", "discount"]:
        out[col] = pd.to_numeric(out[col], errors="coerce")

    # Retain rows with negative profit (valid losses); exclude only rows that cannot be analyzed.
    invalid_key = out["order_id"].isna() | out["order_date"].isna() | out["sales"].isna() | out["profit"].isna()
    report["invalid_core_rows_removed"] = int(invalid_key.sum())
    out = out.loc[~invalid_key].copy()
    out["quantity"] = out["quantity"].fillna(0)
    out["discount"] = out["discount"].fillna(0)
    # Flag unusual values for review; retain them rather than silently deleting potentially valid returns/adjustments.
    report["negative_sales_rows_retained"] = int(out["sales"].lt(0).sum())
    report["nonpositive_quantity_rows_retained"] = int(out["quantity"].le(0).sum())
    report["discount_out_of_range_rows_retained"] = int((~out["discount"].between(0, 1)).sum())
    report["negative_shipping_duration_rows_retained"] = int(((out["ship_date"] - out["order_date"]).dt.days < 0).sum())
    out["order_year"] = out["order_date"].dt.year
    out["order_month"] = out["order_date"].dt.month
    out["month_year"] = out["order_date"].dt.to_period("M").dt.to_timestamp()
    out["profit_margin"] = np.where(out["sales"].ne(0), out["profit"] / out["sales"], np.nan)
    out["shipping_duration"] = (out["ship_date"] - out["order_date"]).dt.days
    out["order_value"] = out.groupby("order_id")["sales"].transform("sum")
    out["is_loss"] = out["profit"] < 0
    out["discount_band"] = pd.cut(out["discount"], bins=[-0.001, 0, .1, .2, .3, .5, 1],
                                  labels=["0%", "1–10%", "11–20%", "21–30%", "31–50%", "Above 50%"])
    report["rows_after"] = len(out)
    report["missing_after"] = out.isna().sum().to_dict()
    report["negative_profit_rows_retained"] = int(out["profit"].lt(0).sum())
    return out.reset_index(drop=True), report
