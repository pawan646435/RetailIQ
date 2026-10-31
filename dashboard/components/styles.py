import streamlit as st


def inject_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');
    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
    .stApp { background: radial-gradient(circle at 80% 0%, #172b4d 0, #0b1220 38%, #080d18 100%); color: #e8eef9; }
    [data-testid="stSidebar"] { background: #0b1424; border-right: 1px solid #1d2b42; }
    [data-testid="stSidebar"] * { color: #d8e2f2; }
    h1,h2,h3 { font-family: 'Manrope', sans-serif !important; letter-spacing: -0.04em; }
    h1 { font-weight: 800 !important; color: #f4f7ff; }
    h2,h3 { color: #eaf0fb; }
    [data-testid="stMetric"] { background: linear-gradient(145deg, #17243a, #111c2e); border: 1px solid #273a55; padding: 18px 20px; border-radius: 16px; box-shadow: 0 10px 30px rgba(0,0,0,.16); }
    [data-testid="stMetricLabel"] { color: #91a4c2 !important; font-size: .82rem; }
    [data-testid="stMetricValue"] { color: #f4f7ff !important; font-family: 'Manrope', sans-serif; font-weight: 800; }
    [data-testid="stMetricDelta"] { font-size: .78rem; }
    div[data-testid="stPlotlyChart"] { background: #111c2e; border: 1px solid #243650; border-radius: 16px; padding: 8px; }
    .eyebrow { color:#58d6c7; font-size:.72rem; font-weight:700; letter-spacing:.16em; text-transform:uppercase; }
    .subtle { color:#91a4c2; }
    .insight { background:linear-gradient(110deg,#14263c,#111c2e); border:1px solid #29425e; border-left:3px solid #58d6c7; border-radius:12px; padding:13px 16px; margin:8px 0; color:#dce7f7; }
    .stTabs [data-baseweb="tab"] { color:#aebed4; }
    
    /* Dashboard polish */

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1500px;
    }

    [data-testid="stMetric"] {
        transition: transform 0.2s ease, border-color 0.2s ease;
    }

    [data-testid="stMetric"]:hover {
        transform: translateY(-3px);
        border-color: #58d6c7;
    }

    div[data-testid="stPlotlyChart"] {
        transition: border-color 0.2s ease;
    }

    div[data-testid="stPlotlyChart"]:hover {
        border-color: #58d6c7;
    }

    .stButton button {
        border-radius: 10px;
    }

    hr {
        border-color: #243650;
    }
    </style>
    """, unsafe_allow_html=True)
