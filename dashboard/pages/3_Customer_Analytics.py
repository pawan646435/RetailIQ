import plotly.express as px
import streamlit as st
from dashboard.common import setup,page_header,empty_state
from src.analysis import customer_summary
_,df=setup("Customer Analytics")
page_header("CUSTOMER INTELLIGENCE","Customer analytics","Explore customer value, repeat purchasing and revenue concentration.")
if df.empty: empty_state(); st.stop()
c=customer_summary(df)
repeat=c.groupby("customer_type",as_index=False).agg(customers=("customer_id","count"),revenue=("revenue","sum"))
a,b=st.columns(2)
with a:
 fig=px.pie(repeat,names="customer_type",values="customers",hole=.65,template="plotly_dark",title="Customer mix · repeat vs one-time")
 fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",margin=dict(t=55,b=10),height=350); st.plotly_chart(fig,use_container_width=True)
with b:
 seg=df.groupby("segment",as_index=False).sales.sum()
 fig=px.pie(seg,names="segment",values="sales",hole=.65,template="plotly_dark",title="Revenue contribution by segment")
 fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",margin=dict(t=55,b=10),height=350); st.plotly_chart(fig,use_container_width=True)
top=c.head(10).sort_values("revenue")
fig=px.bar(top,x="revenue",y="customer_name",orientation="h",color="revenue",color_continuous_scale="Tealgrn",template="plotly_dark",title="Top 10 customers by revenue",labels={"revenue":"Revenue","customer_name":"Customer"})
fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",coloraxis_showscale=False,margin=dict(t=55,b=10),height=430); st.plotly_chart(fig,use_container_width=True)
st.markdown("### Customer value table")
st.dataframe(c[["customer_name","revenue","profit","orders","customer_type","revenue_share"]].head(25).style.format({"revenue":"${:,.2f}","profit":"${:,.2f}","revenue_share":"{:.1%}"}),use_container_width=True,hide_index=True)
