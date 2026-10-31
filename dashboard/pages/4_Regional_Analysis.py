import plotly.express as px
import streamlit as st
from dashboard.common import setup,page_header,empty_state
_,df=setup("Regional Analysis")
page_header("GEOGRAPHIC PERFORMANCE","Regional analysis","Compare revenue, profit, state-level contribution and fulfillment mix.")
if df.empty: empty_state(); st.stop()
reg=df.groupby("region",as_index=False).agg(revenue=("sales","sum"),profit=("profit","sum"))
a,b=st.columns(2)
with a:
 fig=px.bar(reg,x="region",y="revenue",color="profit",color_continuous_scale="RdYlGn",template="plotly_dark",title="Regional revenue colored by profit")
 fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",margin=dict(t=55,b=10),height=350); st.plotly_chart(fig,use_container_width=True)
with b:
 ship=df.groupby("ship_mode",as_index=False).sales.sum()
 fig=px.pie(ship,names="ship_mode",values="sales",hole=.65,template="plotly_dark",title="Shipping mode revenue mix")
 fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",margin=dict(t=55,b=10),height=350); st.plotly_chart(fig,use_container_width=True)
 state=df.groupby("state/province",as_index=False).agg(
    revenue=("sales","sum"),
    profit=("profit","sum"),
    orders=("order_id","nunique")
).nlargest(15,"revenue").sort_values("revenue")
fig=px.bar(
    state,
    x="revenue",
    y="state/province",
    orientation="h",
    color="profit",
    color_continuous_scale="RdYlGn",
    template="plotly_dark",
    title="Top 15 states by revenue",
    hover_data=["orders"]
)
fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",margin=dict(t=55,b=10),height=500); st.plotly_chart(fig,use_container_width=True)
trend=df.groupby(["month_year","region"],as_index=False).sales.sum()
fig=px.line(trend,x="month_year",y="sales",color="region",markers=True,template="plotly_dark",title="Monthly revenue trend by region",labels={"month_year":"Month","sales":"Revenue"})
fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",margin=dict(t=55,b=10),height=400); st.plotly_chart(fig,use_container_width=True)
