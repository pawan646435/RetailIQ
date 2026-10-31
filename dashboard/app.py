import sys
from pathlib import Path

# Add project root to Python path
ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
from dashboard.components.styles import inject_css
st.set_page_config(page_title="RetailIQ | E-commerce Intelligence", page_icon="📊", layout="wide", initial_sidebar_state="expanded")
inject_css()
st.sidebar.markdown('<div class="eyebrow">RETAIL INTELLIGENCE</div>', unsafe_allow_html=True)
st.sidebar.title("RetailIQ")
st.sidebar.caption("E-commerce performance suite")
st.title("RetailIQ")
st.markdown("### E-commerce Sales & Profitability Analytics")
st.markdown("Explore commercial performance through four connected views: executive overview, product intelligence, customer analytics and regional performance.")
st.info("Choose a page from the sidebar to begin. Use the shared filters on each page to focus the analysis.")
st.caption("Sample Superstore is fictional educational data. All metrics and insights are computed from the source dataset.")
