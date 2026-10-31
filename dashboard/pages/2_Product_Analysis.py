import plotly.express as px
import streamlit as st
from dashboard.common import setup,page_header,empty_state
_,df=setup("Product Analysis")
page_header("MERCHANDISING INTELLIGENCE","Product performance","Understand which categories, products and discount levels create value — and which erode margin.")
if df.empty: empty_state(); st.stop()
cat=df.groupby("category",as_index=False).agg(revenue=("sales","sum"),profit=("profit","sum"))
sub=df.groupby("sub_category",as_index=False).agg(revenue=("sales","sum"),profit=("profit","sum"))
prod=df.groupby("product_name",as_index=False).agg(revenue=("sales","sum"),profit=("profit","sum"))
a,b=st.columns(2)
with a:
 fig=px.bar(cat,x="category",y="revenue",color="profit",color_continuous_scale="Tealgrn",template="plotly_dark",title="Category revenue and profit")
 fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",margin=dict(t=55,b=10),height=350); st.plotly_chart(fig,use_container_width=True)
with b:
 fig=px.treemap(df,path=["category","sub_category"],values="sales",color="profit",color_continuous_scale="RdYlGn",template="plotly_dark",title="Category mix · revenue sized, profit colored")
 fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",margin=dict(t=55,b=10),height=350); st.plotly_chart(fig,use_container_width=True)
a,b=st.columns(2)
with a:
 top=prod.nlargest(10,"revenue").sort_values("revenue")
 fig=px.bar(top,x="revenue",y="product_name",orientation="h",template="plotly_dark",title="Top 10 products by revenue")
 fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",margin=dict(t=55,b=10),height=430); st.plotly_chart(fig,use_container_width=True)
with b:
 loss=prod.nsmallest(10,"profit").sort_values("profit")
 fig=px.bar(loss,x="profit",y="product_name",orientation="h",color="profit",color_continuous_scale="RdYlGn",template="plotly_dark",title="10 weakest products by cumulative profit")
 fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",coloraxis_showscale=False,margin=dict(t=55,b=10),height=430); st.plotly_chart(fig,use_container_width=True)
fig=px.scatter(df,x="discount",y="profit",color="category",size="sales",hover_data=["product_name","sub_category"],opacity=.68,template="plotly_dark",title="Discount vs. profit · each point is a transaction line",labels={"discount":"Discount rate","profit":"Profit"})
fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",margin=dict(t=55,b=10),height=430); st.plotly_chart(fig,use_container_width=True)
st.caption("Interpret discount/profit patterns as associations. Product mix, order size and other factors may also influence profit.")
