import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__),".."))
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.styles import apply_styles, sidebar_nav, sec, ins, sel_cards, pl, P1, P2, P3, P4, P5, P6, MIXED

st.set_page_config(page_title="Multivariate Analysis", page_icon="🔥", layout="wide")
apply_styles()
sidebar_nav()

@st.cache_data
def load():
    df = pd.read_csv("data/supply_chain_cleaned.csv")
    df.columns = df.columns.str.strip().str.lower()
    return df
df = load()

st.markdown("""
<div class='hero' style='padding:28px 36px'>
    <h1 style='font-size:1.7rem'>🔥 Multivariate Analysis</h1>
    <p>Understanding complex interactions between multiple variables simultaneously</p>
</div>""", unsafe_allow_html=True)

OPTIONS = ["🌡️ Correlation Heatmap","💹 Profit vs Sales by Market",
           "🚚 Shipping Days vs Profit","📂 Category × Market × Profit",
           "👥 Segment × Market × Sales"]
with st.sidebar:
    st.markdown("<div class='nav-lbl'>Analysis</div>", unsafe_allow_html=True)
    choice = st.radio("", OPTIONS, label_visibility="collapsed")
# st.markdown(sel_cards(OPTIONS, choice), unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
if choice == OPTIONS[0]:
    st.markdown(sec("🌡️","Correlation Heatmap"), unsafe_allow_html=True)
    num_df = df[['sales','order profit per order','benefit per order','sales per customer',
                 'order item discount','order item discount rate','order item product price',
                 'order item profit ratio','days for shipping (real)',
                 'days for shipment (scheduled)','delay','late_delivery_risk',
                 'profit_margin','order item quantity','order item total']].dropna()
    corr = num_df.corr().round(3)

    fig = go.Figure(data=go.Heatmap(
        z=corr.values, x=corr.columns.tolist(), y=corr.columns.tolist(),
        colorscale=[[0,'#7E22CE'],[0.5,'#0F172A'],[1,'#0EA5E9']],
        zmin=-1, zmax=1,
        text=corr.values.round(2), texttemplate='%{text}',
        textfont=dict(size=9, color='#E2E8F0'),
        hovertemplate='%{x}<br>%{y}<br>r = %{z:.3f}<extra></extra>'))
    fig.update_layout(title='Correlation Matrix — Custom Purple-Blue Scale',
                      xaxis=dict(tickangle=-45, tickfont=dict(color='#CBD5E1',size=10)),
                      yaxis=dict(tickfont=dict(color='#CBD5E1',size=10)))
    pl(fig,580)
    st.plotly_chart(fig, use_container_width=True)

    pairs = []
    cols = corr.columns.tolist()
    for i in range(len(cols)):
        for j in range(i+1,len(cols)):
            r = corr.iloc[i,j]
            if abs(r)>0.3:
                pairs.append({'Variable 1':cols[i],'Variable 2':cols[j],'Correlation':round(r,3)})
    cdf = pd.DataFrame(pairs).sort_values('Correlation',key=abs,ascending=False)
    st.markdown("#### 📋 Strong Correlations (|r| > 0.3)")
    st.dataframe(cdf, use_container_width=True, hide_index=True)
    st.markdown(ins("obs","Observation","<b>Discount Rate and Profit have a clear negative correlation</b> — as discounts increase, profit decreases. Real Shipping Days and Delay are strongly positively correlated. Late Delivery Risk and Delay are nearly perfectly correlated."), unsafe_allow_html=True)
    st.markdown(ins("impact","Business Impact","The negative correlation between Discount Rate and Profit mathematically confirms that <b>every percentage point of discount directly reduces profit</b>. The Shipping Days–Delay correlation means delivery performance cannot improve without addressing shipping speed at the carrier level."), unsafe_allow_html=True)
    st.markdown(ins("rec","Recommendation","Use correlation data to build a profit prediction model: input discount rate and shipping mode, output expected profit per order. Rule: no discount above 8% unless the order is above $500 AND the customer has placed 3+ previous orders."), unsafe_allow_html=True)

elif choice == OPTIONS[1]:
    st.markdown(sec("💹","Profit vs Sales — By Market"), unsafe_allow_html=True)
    sample = df.sample(4000, random_state=42)
    c1,c2 = st.columns(2)
    with c1:
        fig = px.scatter(sample, x='sales', y='order profit per order',
                         color='market', opacity=0.55,
                         color_discrete_sequence=P6,
                         title='Profit vs Sales — Colored by Market',
                         labels={'sales':'Sales ($)','order profit per order':'Profit ($)'})
        fig.add_hline(y=0,line_dash='dash',line_color='#F87171',
                      annotation_text='Break-Even',annotation_font_color='#FCA5A5')
        fig.update_traces(hovertemplate='Market: %{fullData.name}<br>Sales: $%{x:,.0f}<br>Profit: $%{y:,.0f}<extra></extra>')
        pl(fig)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        ma = df.groupby('market').agg(
            Avg_Sales=('sales','mean'),Avg_Profit=('order profit per order','mean'),
            Orders=('order id','count')).reset_index().round(2)
        fig2 = px.scatter(ma, x='Avg_Sales', y='Avg_Profit',
                          size='Orders', color='market', text='market',
                          color_discrete_sequence=P6, size_max=55,
                          title='Market: Avg Sales vs Avg Profit (Bubble=Orders)')
        fig2.update_traces(textposition='top center',
                           hovertemplate='<b>%{text}</b><br>Avg Sales: $%{x:,.0f}<br>Avg Profit: $%{y:,.0f}<extra></extra>')
        fig2.add_hline(y=0,line_dash='dash',line_color='#F87171')
        pl(fig2)
        st.plotly_chart(fig2, use_container_width=True)

    # Faceted scatter
    fig3 = px.scatter(sample, x='sales', y='order profit per order',
                      facet_col='market', facet_col_wrap=3,
                      color='delivery status', color_discrete_sequence=MIXED,
                      opacity=0.45, title='Profit vs Sales — Faceted by Market + Delivery Status')
    fig3.add_hline(y=0,line_dash='dash',line_color='#F87171')
    pl(fig3,480)
    st.plotly_chart(fig3, use_container_width=True)
    st.dataframe(ma, use_container_width=True, hide_index=True)
    st.markdown(ins("obs","Observation","A large number of individual orders across every market fall <b>below the red break-even line</b>. Late delivery orders cluster more frequently in the negative profit zone — confirming late deliveries and losses are directly linked."), unsafe_allow_html=True)
    st.markdown(ins("impact","Business Impact","Loss-making orders in every market means this is a <b>systemic pricing and cost structure problem</b> — not regional. Late deliveries trigger partial refunds, discount compensation, and support costs that actively reduce final profit recorded per order."), unsafe_allow_html=True)
    st.markdown(ins("rec","Recommendation","Build a per-market profitability floor: any product-market combination averaging negative profit over 30 days triggers an automatic price review. For LATAM: run a 60-day test — reduce discounts 5%, measure volume vs profit impact."), unsafe_allow_html=True)

elif choice == OPTIONS[2]:
    st.markdown(sec("🚚","Shipping Days vs Profit — By Mode"), unsafe_allow_html=True)
    sample = df.sample(4000, random_state=42)
    fig = px.scatter(sample, x='days for shipping (real)', y='order profit per order',
                     color='shipping mode', facet_col='shipping mode',
                     color_discrete_sequence=P3, opacity=0.55,
                     trendline='ols',
                     title='Real Shipping Days vs Profit — OLS Trendlines per Mode')
    fig.add_hline(y=0,line_dash='dash',line_color='#FACC15')
    pl(fig,420)
    st.plotly_chart(fig, use_container_width=True)

    c1,c2 = st.columns(2)
    with c1:
        md = df.groupby(['shipping mode','days for shipping (real)']).agg(
            Avg_Profit=('order profit per order','mean')).reset_index().round(2)
        fig2 = px.line(md, x='days for shipping (real)', y='Avg_Profit',
                       color='shipping mode', markers=True,
                       color_discrete_sequence=P3,
                       title='Avg Profit vs Shipping Days — Line Chart')
        fig2.add_hline(y=0,line_dash='dash',line_color='#F87171')
        fig2.update_traces(hovertemplate='Mode: %{fullData.name}<br>Days: %{x}<br>Avg Profit: $%{y:,.2f}<extra></extra>')
        pl(fig2)
        st.plotly_chart(fig2, use_container_width=True)
    with c2:
        mp2 = df.groupby('shipping mode').agg(
            Avg_Days=('days for shipping (real)','mean'),
            Avg_Profit=('order profit per order','mean'),
            Late_Pct=('late_delivery_risk','mean')).reset_index().round(3)
        mp2['Late_Pct'] = (mp2['Late_Pct']*100).round(1)
        fig3 = px.scatter(mp2, x='Avg_Days', y='Avg_Profit',
                          size='Late_Pct', color='shipping mode', text='shipping mode',
                          color_discrete_sequence=P3, size_max=55,
                          title='Avg Days vs Avg Profit (Bubble = Late %)')
        fig3.add_hline(y=0,line_dash='dash',line_color='#F87171')
        fig3.update_traces(textposition='top center',
                           hovertemplate='<b>%{text}</b><br>Avg Days: %{x:.2f}<br>Avg Profit: $%{y:.2f}<extra></extra>')
        pl(fig3)
        st.plotly_chart(fig3, use_container_width=True)

    summ = df.groupby('shipping mode').agg(
        Avg_Days=('days for shipping (real)','mean'),
        Avg_Profit=('order profit per order','mean'),
        Total_Profit=('order profit per order','sum'),
        Late_Risk=('late_delivery_risk','mean'),
        Orders=('order id','count')).reset_index().round(2)
    summ['Late_%'] = (summ['Late_Risk']*100).round(1)
    st.dataframe(summ.drop('Late_Risk',axis=1), use_container_width=True, hide_index=True)
    st.markdown(ins("obs","Observation","OLS trendlines show a <b>downward slope for most shipping modes</b> — as real shipping days increase, average profit decreases. Standard Class orders taking 6+ days frequently dip into negative profit territory."), unsafe_allow_html=True)
    st.markdown(ins("impact","Business Impact","Choosing a slower shipping mode doesn't just delay customers — it <b>directly reduces profit per order</b>. Slow delivery triggers dissatisfaction, discount requests, returns, and partial refunds, all reducing final profit."), unsafe_allow_html=True)
    st.markdown(ins("rec","Recommendation","Model the true cost of Standard Class including delayed delivery costs (refunds, vouchers, support tickets). When true cost is calculated, First Class may actually be cheaper for orders above $200. Use this to justify shifting the mix within 6 months."), unsafe_allow_html=True)

elif choice == OPTIONS[3]:
    st.markdown(sec("📂","Category × Market × Profit"), unsafe_allow_html=True)
    cm = df.groupby(['main_category','market']).agg(
        Total_Profit=('order profit per order','sum'),
        Avg_Profit=('order profit per order','mean'),
        Orders=('order id','count')).reset_index().round(2)

    pivot = cm.pivot(index='main_category',columns='market',values='Total_Profit').fillna(0)
    fig = go.Figure(data=go.Heatmap(
        z=pivot.values, x=pivot.columns.tolist(), y=pivot.index.tolist(),
        colorscale=[[0,'#7C2D12'],[0.4,'#EA580C'],[0.6,'#FACC15'],[1,'#15803D']],
        text=pivot.values.round(0),
        texttemplate='$%{text:,.0f}', textfont=dict(size=9,color='#FFFFFF'),
        hovertemplate='Category: %{y}<br>Market: %{x}<br>Profit: $%{z:,.0f}<extra></extra>'))
    fig.update_layout(title='Profit Heatmap — Category vs Market (Orange-Green Scale)',
                      xaxis=dict(tickfont=dict(color='#CBD5E1')),
                      yaxis=dict(tickfont=dict(color='#CBD5E1')))
    pl(fig,500)
    st.plotly_chart(fig, use_container_width=True)

    c1,c2 = st.columns(2)
    with c1:
        fig2 = px.bar(cm, x='main_category', y='Total_Profit', color='market',
                      barmode='group', color_discrete_sequence=MIXED,
                      title='Profit by Category and Market — Grouped Bar')
        fig2.add_hline(y=0,line_dash='dash',line_color='#F87171')
        fig2.update_layout(xaxis_tickangle=-30)
        fig2.update_traces(hovertemplate='Category: %{x}<br>Profit: $%{y:,.0f}<extra></extra>')
        pl(fig2)
        st.plotly_chart(fig2, use_container_width=True)
    with c2:
        fig3 = px.treemap(cm[cm['Total_Profit']>0],
                          path=['market','main_category'],
                          values='Total_Profit', color='Avg_Profit',
                          color_continuous_scale=[[0,'#FACC15'],[1,'#15803D']],
                          title='Treemap — Market → Category (Profitable Only)')
        fig3.update_traces(textfont=dict(color='#FFFFFF',size=12),
                           hovertemplate='<b>%{label}</b><br>Profit: $%{value:,.0f}<extra></extra>')
        pl(fig3)
        st.plotly_chart(fig3, use_container_width=True)

    st.dataframe(cm.sort_values('Total_Profit',ascending=False), use_container_width=True, hide_index=True)
    st.markdown(ins("obs","Observation","Green cells (profitable) concentrate in <b>Europe and USCA markets</b>. Red/orange cells appear more in LATAM and Africa. Critically, <b>the same category can be profitable in one market and a loss-maker in another</b>."), unsafe_allow_html=True)
    st.markdown(ins("impact","Business Impact","Blanket pricing and discount policies are dangerous. A 15% discount acceptable in USCA may create a net loss for the same product in LATAM. The company applies uniform pricing across markets, <b>systematically destroying margins in price-sensitive regions</b>."), unsafe_allow_html=True)
    st.markdown(ins("rec","Recommendation","Implement market-specific pricing for the top 20 categories. Categories loss-making in LATAM or Africa should have prices raised 8–12% in those markets or discount eligibility removed. Use this heatmap monthly to identify emerging loss zones."), unsafe_allow_html=True)

elif choice == OPTIONS[4]:
    st.markdown(sec("👥","Customer Segment × Market × Sales"), unsafe_allow_html=True)
    sm = df.groupby(['customer segment','market']).agg(
        Total_Sales=('sales','sum'),
        Total_Profit=('order profit per order','sum'),
        Orders=('order id','count')).reset_index().round(2)

    pivot_s = sm.pivot(index='customer segment',columns='market',values='Total_Sales').fillna(0)
    fig = go.Figure(data=go.Heatmap(
        z=pivot_s.values, x=pivot_s.columns.tolist(), y=pivot_s.index.tolist(),
        colorscale=[[0,'#1E3A5F'],[0.5,'#0EA5E9'],[1,'#BAE6FD']],
        text=pivot_s.values.round(0),
        texttemplate='$%{text:,.0f}', textfont=dict(size=10,color='#0F172A'),
        hovertemplate='Segment: %{y}<br>Market: %{x}<br>Sales: $%{z:,.0f}<extra></extra>'))
    fig.update_layout(title='Sales Heatmap — Customer Segment vs Market')
    pl(fig,320)
    st.plotly_chart(fig, use_container_width=True)

    c1,c2 = st.columns(2)
    with c1:
        fig2 = px.bar(sm, x='market', y='Total_Sales', color='customer segment',
                      barmode='stack', color_discrete_sequence=P1,
                      title='Stacked Sales: Market × Segment')
        fig2.update_traces(hovertemplate='<b>%{fullData.name}</b><br>Market: %{x}<br>Sales: $%{y:,.0f}<extra></extra>')
        pl(fig2)
        st.plotly_chart(fig2, use_container_width=True)
    with c2:
        fig3 = px.bar(sm, x='market', y='Total_Profit', color='customer segment',
                      barmode='stack', color_discrete_sequence=P2,
                      title='Stacked Profit: Market × Segment')
        fig3.add_hline(y=0,line_dash='dash',line_color='#F87171')
        fig3.update_traces(hovertemplate='<b>%{fullData.name}</b><br>Market: %{x}<br>Profit: $%{y:,.0f}<extra></extra>')
        pl(fig3)
        st.plotly_chart(fig3, use_container_width=True)

    fig4 = px.sunburst(sm, path=['market','customer segment'],
                       values='Total_Sales', color='Total_Profit',
                       color_continuous_scale=[[0,'#EF4444'],[0.5,'#FACC15'],[1,'#22C55E']],
                       title='Sunburst: Market → Segment → Sales (Color = Profit)')
    fig4.update_traces(textfont=dict(color='#FFFFFF'),
                       hovertemplate='<b>%{label}</b><br>Sales: $%{value:,.0f}<extra></extra>')
    pl(fig4,480)
    st.plotly_chart(fig4, use_container_width=True)
    st.dataframe(sm.sort_values('Total_Sales',ascending=False), use_container_width=True, hide_index=True)
    st.markdown(ins("obs","Observation","Consumer segment drives the highest sales across all markets, but the stacked profit chart shows <b>Consumer profit is disproportionately small</b> compared to its sales contribution. Corporate customers in Europe and USCA generate the highest profit-to-sales ratio."), unsafe_allow_html=True)
    st.markdown(ins("impact","Business Impact","The company devotes the most resources to the segment-market combination that delivers the weakest profit returns. Consumer segment in LATAM and Africa likely operates at near-zero or negative margins when shipping and discount costs are factored in. <b>Growth in these segments increases total losses</b>."), unsafe_allow_html=True)
    st.markdown(ins("rec","Recommendation","Prioritise Corporate segment acquisition in Europe and USCA where profit-to-sales ratio is proven highest. For Consumer in LATAM and Africa, introduce minimum order value requirements before discount eligibility. Track Profit per Segment per Market as a monthly board-level KPI."), unsafe_allow_html=True)
