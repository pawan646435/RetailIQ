from pathlib import Path
import sys
import pandas as pd
import streamlit as st
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.data_loader import load_raw_data, PROCESSED_DIR
from src.data_cleaning import clean_data
from src.analysis import kpis, build_insights
from dashboard.components.styles import inject_css

@st.cache_data(show_spinner="Preparing your analytics workspace…")
def get_data():
    processed = PROCESSED_DIR / "superstore_cleaned.csv"
    if processed.exists():
        return pd.read_csv(processed, parse_dates=["order_date", "ship_date", "month_year"])
    raw = load_raw_data()
    cleaned, _ = clean_data(raw)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    cleaned.to_csv(processed, index=False)
    return cleaned

def setup(page_title: str):
    inject_css()
    st.sidebar.markdown('<div class="eyebrow">RETAIL INTELLIGENCE</div>', unsafe_allow_html=True)
    st.sidebar.title("RetailIQ")
    st.sidebar.caption("E-commerce performance suite")
    try:
        df = get_data()
    except Exception as exc:
        st.error(str(exc))
        st.info("Download the official Sample Superstore dataset and place its CSV/XLSX file in `data/raw/`, then rerun the app.")
        st.stop()
    st.sidebar.divider()
    dates = pd.to_datetime(df.order_date)
    start, end = dates.min().date(), dates.max().date()
    date_range = st.sidebar.date_input("Order date range", value=(start, end), min_value=start, max_value=end)
    regions = sorted(df.region.dropna().unique()) if "region" in df else []
    cats = sorted(df.category.dropna().unique()) if "category" in df else []
    segments = sorted(df.segment.dropna().unique()) if "segment" in df else []
    ships = sorted(df.ship_mode.dropna().unique()) if "ship_mode" in df else []
    region = st.sidebar.multiselect("Region", regions, default=regions)
    category = st.sidebar.multiselect("Category", cats, default=cats)
    segment = st.sidebar.multiselect("Customer segment", segments, default=segments)
    ship = st.sidebar.multiselect("Ship mode", ships, default=ships)
    if isinstance(date_range, tuple) and len(date_range) == 2:
        d1, d2 = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1]) + pd.Timedelta(days=1) - pd.Timedelta(microseconds=1)
        mask = df.order_date.between(d1, d2)
    else: mask = pd.Series(True, index=df.index)
    for col, vals in [("region",region),("category",category),("segment",segment),("ship_mode",ship)]:
        if col in df: mask &= df[col].isin(vals)
    filtered = df.loc[mask].copy()
    st.sidebar.divider()
    st.sidebar.caption(f"{len(filtered):,} line items · {filtered.order_id.nunique():,} orders")
    return df, filtered

def page_header(kicker, title, subtitle):
    st.markdown(f'<div class="eyebrow">{kicker}</div>', unsafe_allow_html=True)
    st.title(title)
    st.markdown(f'<p class="subtle">{subtitle}</p>', unsafe_allow_html=True)

def money(v): return f"${v:,.0f}"
def compact_money(value):
    value = float(value)

    if abs(value) >= 1_000_000_000:
        return f"${value / 1_000_000_000:.2f}B"
    elif abs(value) >= 1_000_000:
        return f"${value / 1_000_000:.2f}M"
    elif abs(value) >= 1_000:
        return f"${value / 1_000:.1f}K"
    else:
        return f"${value:,.0f}"

def empty_state(): st.info("No records match the current filters. Broaden the date range or select additional filter values.")
