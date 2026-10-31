import plotly.express as px
import streamlit as st
from dashboard.common import setup, page_header, kpis, money, compact_money, empty_state
from src.analysis import monthly_trend, build_insights
_, df = setup("Executive Overview")
page_header("EXECUTIVE COMMAND CENTER", "Sales & profitability at a glance", "Track the commercial pulse and identify where performance is accelerating or leaking.")
if df.empty: empty_state(); st.stop()
m=kpis(df)
kpi_data = [
    ("Revenue", compact_money(m["revenue"])),
    ("Profit", compact_money(m["profit"])),
    ("Orders", f"{m['orders']:,}"),
    ("Avg. order value", money(m["aov"])),
    ("Profit margin", f"{m['margin']:.1%}")
]

for col, (label, value) in zip(st.columns(5), kpi_data):
    col.metric(label, value)
st.markdown(" ")
trend=monthly_trend(df)
left,right=st.columns([1.65,1])
with left:
    fig=px.line(trend,x="month_year",y=["sales","profit"],markers=True,template="plotly_dark",labels={"month_year":"Month","value":"Amount","variable":"Metric"},title="Revenue & profit trajectory")
    fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    legend_title_text="",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    margin=dict(l=10, r=10, t=75, b=15),
    height=380
)
    st.plotly_chart(fig,use_container_width=True)
with right:
    cat=df.groupby("category",as_index=False).sales.sum().sort_values("sales",ascending=False)
    fig=px.pie(cat,names="category",values="sales",hole=.68,template="plotly_dark",title="Revenue mix by category")
    fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=10, r=10, t=55, b=45),
    height=380,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.15,
        xanchor="center",
        x=0.5
    ),
    legend_title_text=""
)
    st.plotly_chart(fig,use_container_width=True)
left,right=st.columns(2)
with left:
    reg=df.groupby("region",as_index=False).profit.sum().sort_values("profit")
    fig=px.bar(reg,x="profit",y="region",orientation="h",color="profit",color_continuous_scale="Tealgrn",template="plotly_dark",title="Profit contribution by region",labels={"profit":"Profit","region":"Region"})
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",coloraxis_showscale=False,margin=dict(l=10,r=10,t=55,b=10),height=320)
    st.plotly_chart(fig,use_container_width=True)
with right:
    seg=df.groupby("segment",as_index=False).sales.sum()
    fig=px.bar(seg,x="segment",y="sales",color="segment",template="plotly_dark",title="Revenue by customer segment",labels={"sales":"Revenue","segment":"Segment"})
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",showlegend=False,margin=dict(l=10,r=10,t=55,b=10),height=320)
    st.plotly_chart(fig,use_container_width=True)
prod=df.groupby("product_name",as_index=False).sales.sum().nlargest(10,"sales").sort_values("sales")
fig=px.bar(prod,x="sales",y="product_name",orientation="h",template="plotly_dark",title="Top 10 products by revenue",labels={"sales":"Revenue","product_name":"Product"})
fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",margin=dict(l=10,r=10,t=55,b=10),height=420)
st.plotly_chart(fig,use_container_width=True)
st.markdown("### Signals worth investigating")
for insight in build_insights(df): st.markdown(f'<div class="insight">{insight}</div>',unsafe_allow_html=True)
