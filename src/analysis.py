import pandas as pd
import numpy as np


def kpis(df: pd.DataFrame) -> dict:
    sales = df.sales.sum() if not df.empty else 0
    profit = df.profit.sum() if not df.empty else 0
    orders = df.order_id.nunique() if not df.empty else 0
    return {"revenue": sales, "profit": profit, "orders": orders,
            "aov": sales / orders if orders else 0,
            "margin": profit / sales if sales else 0,
            "customers": df.customer_id.nunique() if not df.empty and "customer_id" in df else 0}


def monthly_trend(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty: return pd.DataFrame(columns=["month_year", "sales", "profit"])
    return df.groupby("month_year", as_index=False).agg(sales=("sales", "sum"), profit=("profit", "sum")).sort_values("month_year")


def customer_summary(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty: return pd.DataFrame()
    x = df.groupby(["customer_id", "customer_name"], dropna=False).agg(
        revenue=("sales", "sum"), orders=("order_id", "nunique"), profit=("profit", "sum")).reset_index()
    x["customer_type"] = np.where(x.orders > 1, "Repeat", "One-time")
    x["revenue_share"] = x.revenue / x.revenue.sum() if x.revenue.sum() else 0
    return x.sort_values("revenue", ascending=False)


def build_insights(df: pd.DataFrame) -> list[str]:
    if df.empty: return ["No records match the selected filters. Adjust the filters to explore the data."]
    insights = []
    cat = df.groupby("category").sales.sum().sort_values(ascending=False)
    reg = df.groupby("region").profit.sum().sort_values(ascending=False)
    seg = df.groupby("segment").sales.sum().sort_values(ascending=False)
    product = df.groupby("product_name").profit.sum().sort_values()
    if len(cat): insights.append(f"{cat.index[0]} leads category revenue with {cat.iloc[0]:,.0f} in sales.")
    if len(reg): insights.append(f"{reg.index[0]} is the most profitable region ({reg.iloc[0]:,.0f} profit).")
    if len(seg): insights.append(f"{seg.index[0]} contributes the highest segment revenue ({seg.iloc[0]:,.0f}).")
    if len(product) and product.iloc[0] < 0: insights.append(f"{product.index[0]} has the largest cumulative product loss ({product.iloc[0]:,.0f}).")
    corr = df[["discount", "profit"]].corr().iloc[0, 1] if len(df) > 1 else np.nan
    if pd.notna(corr):
        insights.append(f"Discount and profit have a {('negative' if corr < 0 else 'positive')} correlation (r = {corr:.2f}); this is association, not proof of causation.")
    trend = monthly_trend(df)
    if len(trend) >= 2:
        prev, curr = trend.sales.iloc[-2], trend.sales.iloc[-1]
        change = (curr - prev) / abs(prev) * 100 if prev else np.nan
        if pd.notna(change): insights.append(f"Latest month revenue changed {change:+.1f}% versus the preceding month.")
    return insights
