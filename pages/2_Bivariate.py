import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__),".."))
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.styles import apply_styles, sidebar_nav, sec, ins, sel_cards, pl, P1, P2, P3, P4, P5, P6, MIXED

st.set_page_config(page_title="Bivariate Analysis", page_icon="📈", layout="wide")
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
    <h1 style='font-size:1.7rem'>📈 Bivariate Analysis</h1>
    <p>Exploring relationships between two variables to uncover hidden patterns</p>
</div>""", unsafe_allow_html=True)

OPTIONS = ["📦 Shipping Days vs Real","📂 Category vs Profit",
           "👥 Customer Segment vs Sales","🌍 Market vs Profit","🚚 Shipping Mode vs Delay"]
with st.sidebar:
    st.markdown("<div class='nav-lbl'>Analysis</div>", unsafe_allow_html=True)
    choice = st.radio("", OPTIONS, label_visibility="collapsed")

# ═══════════════════════════════════════════════════════════════════════════════
if choice == OPTIONS[0]:
    st.markdown(sec("📦","Scheduled vs Real Shipping Days"), unsafe_allow_html=True)
    sample = df.sample(3000, random_state=42)

    c1,c2 = st.columns(2)
    with c1:
        fig = px.scatter(sample, x='days for shipment (scheduled)',
                         y='days for shipping (real)',
                         color='delivery status', opacity=0.55,
                         color_discrete_sequence=MIXED,
                         title='Scheduled vs Real Shipping Days',
                         labels={'days for shipment (scheduled)':'Scheduled Days',
                                 'days for shipping (real)':'Real Days'})
        fig.add_shape(type='line',x0=0,y0=0,x1=10,y1=10,
                      line=dict(color='#FACC15',dash='dash',width=2))
        fig.add_annotation(x=8,y=7.5,text='Perfect Delivery Line',
                           font=dict(color='#FACC15',size=11),showarrow=False)
        fig.update_traces(hovertemplate='Scheduled: %{x}d<br>Real: %{y}d<extra></extra>')
        pl(fig)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        agg = df.groupby('days for shipment (scheduled)')['days for shipping (real)'].mean().reset_index()
        agg.columns = ['Scheduled','Avg Real']
        fig2 = px.area(agg, x='Scheduled', y='Avg Real',
                       color_discrete_sequence=['#38BDF8'],
                       title='Avg Real Days per Scheduled Day — Area Chart')
        fig2.add_scatter(x=agg['Scheduled'],y=agg['Scheduled'],
                         mode='lines', name='Perfect (1:1)',
                         line=dict(color='#FACC15',dash='dash',width=2))
        fig2.update_traces(hovertemplate='Scheduled: %{x}d<br>Avg Real: %{y:.2f}d<extra></extra>',
                           selector=dict(type='scatter',mode='lines+markers'))
        pl(fig2)
        st.plotly_chart(fig2, use_container_width=True)

    tbl = df.groupby('days for shipment (scheduled)').agg(
        Orders=('order id','count'),
        Avg_Real=('days for shipping (real)','mean'),
        Avg_Delay=('delay','mean'),
        Late_Count=('late_delivery_risk','sum')
    ).reset_index().round(2)
    tbl.columns=['Scheduled Days','Orders','Avg Real Days','Avg Delay Days','Late Deliveries']
    st.markdown("#### 📋 Comparison Table")
    st.dataframe(tbl, use_container_width=True, hide_index=True)
    st.markdown(ins("obs","Observation","Almost all orders fall <b>above the yellow diagonal</b> — real shipping days consistently exceed promises. Orders scheduled for 3 days often take 5–6 days. There is no scheduling window where actual delivery matches the plan."), unsafe_allow_html=True)
    st.markdown(ins("impact","Business Impact","This gap is the root cause of the 54.83% late delivery rate. Customers make purchasing decisions based on the delivery promise shown at checkout. When promises are systematically broken, <b>customers lose confidence and reduce repeat purchases</b>."), unsafe_allow_html=True)
    st.markdown(ins("rec","Recommendation","Stop showing optimistic estimates. Use historical real shipping data to calculate realistic delivery windows at checkout (e.g. '5–7 business days' instead of '3–4 days'). Work with logistics partners to close the gap contractually."), unsafe_allow_html=True)

elif choice == OPTIONS[1]:
    st.markdown(sec("📂","Category vs Profit Analysis"), unsafe_allow_html=True)
    cp = df.groupby('category name').agg(
        Total_Profit=('order profit per order','sum'),
        Avg_Profit=('order profit per order','mean'),
        Orders=('order id','count')
    ).reset_index().sort_values('Total_Profit',ascending=False).round(2)

    c1,c2 = st.columns(2)
    with c1:
        # Lollipop chart for top 15
        top15 = cp.head(15).sort_values('Total_Profit')
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=top15['Total_Profit'], y=top15['category name'],
            mode='markers', marker=dict(color=P2[0],size=12,line=dict(color='#FFFFFF',width=1)),
            name='Profit',
            hovertemplate='<b>%{y}</b><br>Profit: $%{x:,.0f}<extra></extra>'))
        for _,row in top15.iterrows():
            fig.add_shape(type='line',x0=0,x1=row['Total_Profit'],
                          y0=row['category name'],y1=row['category name'],
                          line=dict(color='rgba(34,197,94,0.4)',width=2))
        fig.add_vline(x=0,line_dash='dash',line_color='#EF4444')
        fig.update_layout(title='Top 15 Categories — Lollipop Chart',yaxis_title='')
        pl(fig,480)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig2 = px.scatter(cp,x='Orders',y='Avg_Profit',size='Total_Profit',
                          color='Total_Profit',hover_name='category name',
                          color_continuous_scale='RdYlGn',
                          title='Orders vs Avg Profit — Bubble Chart',
                          labels={'Avg_Profit':'Avg Profit per Order'})
        fig2.add_hline(y=0,line_dash='dash',line_color='#EF4444',
                       annotation_text='Break Even',annotation_font_color='#F87171')
        fig2.update_traces(hovertemplate='<b>%{hovertext}</b><br>Orders: %{x:,}<br>Avg Profit: $%{y:.2f}<extra></extra>')
        pl(fig2,480)
        st.plotly_chart(fig2, use_container_width=True)

    loss = cp[cp['Total_Profit']<0]
    if not loss.empty:
        st.markdown("#### 🔴 Loss-Making Categories")
        st.dataframe(loss, use_container_width=True, hide_index=True)
    st.dataframe(cp, use_container_width=True, hide_index=True)
    st.markdown(ins("obs","Observation","The lollipop chart clearly shows categories extending right (profit) vs left (loss). High order volume does <b>NOT guarantee positive profit</b> — some of the most-ordered categories sit below the break-even line."), unsafe_allow_html=True)
    st.markdown(ins("impact","Business Impact","Loss-making categories are a hidden financial drain. High-volume loss categories appear healthy on a sales dashboard while silently <b>destroying profit at scale</b>. Marketing and logistics investment amplifies these losses."), unsafe_allow_html=True)
    st.markdown(ins("rec","Recommendation","Flag the bottom 5 categories for an immediate pricing and cost review. For each: (1) check if selling price covers COGS + shipping, (2) remove discounts, (3) discontinue if losses persist after repricing. Increase investment in the top 5 profit-generating categories."), unsafe_allow_html=True)

elif choice == OPTIONS[2]:
    st.markdown(sec("👥","Customer Segment vs Sales"), unsafe_allow_html=True)
    seg = df.groupby('customer segment').agg(
        Total_Sales=('sales','sum'),
        Total_Profit=('order profit per order','sum'),
        Orders=('order id','count'),
        Customers=('customer id','nunique'),
        Avg_Discount=('order item discount rate','mean')
    ).reset_index().round(2)
    seg['Profit_Margin_%'] = (seg['Total_Profit']/seg['Total_Sales']*100).round(2)

    c1,c2 = st.columns(2)
    with c1:
        # Diverging bar: sales vs profit
        fig = go.Figure()
        fig.add_trace(go.Bar(name='Total Sales',x=seg['Total_Sales'],y=seg['customer segment'],
                             orientation='h',marker_color='#38BDF8',
                             hovertemplate='<b>%{y}</b><br>Sales: $%{x:,.0f}<extra></extra>'))
        fig.add_trace(go.Bar(name='Total Profit',x=seg['Total_Profit'],y=seg['customer segment'],
                             orientation='h',marker_color='#22C55E',
                             hovertemplate='<b>%{y}</b><br>Profit: $%{x:,.0f}<extra></extra>'))
        fig.update_layout(barmode='group',title='Sales vs Profit — Grouped Bars',yaxis_title='')
        pl(fig,360)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        # Waterfall: profit margin
        fig2 = go.Figure(go.Waterfall(
            name='Profit Margin %',
            orientation='v',
            x=seg['customer segment'].tolist(),
            y=seg['Profit_Margin_%'].tolist(),
            text=[f"{v:.1f}%" for v in seg['Profit_Margin_%']],
            textposition='outside',
            textfont=dict(color='#0F172A'),
            connector=dict(line=dict(color='#334155',width=1)),
            increasing=dict(marker=dict(color='#22C55E')),
            decreasing=dict(marker=dict(color='#EF4444')),
            totals=dict(marker=dict(color='#38BDF8')),
            hovertemplate='<b>%{x}</b><br>Margin: %{y:.2f}%<extra></extra>'))
        fig2.update_layout(title='Profit Margin % — Waterfall',showlegend=False)
        pl(fig2,360)
        st.plotly_chart(fig2, use_container_width=True)

    st.dataframe(seg, use_container_width=True, hide_index=True)
    st.markdown(ins("obs","Observation","The Consumer segment generates the highest absolute sales (~51%), but the grouped bar chart shows its <b>profit is disproportionately low</b> relative to sales volume. The waterfall confirms Corporate has the healthiest profit margin %."), unsafe_allow_html=True)
    st.markdown(ins("impact","Business Impact","Pouring marketing budget into Consumer segment acquisition is a losing strategy if each Consumer order earns minimal profit. The company runs a high-revenue, low-profit operation in its largest segment — creating a <b>false sense of growth</b>."), unsafe_allow_html=True)
    st.markdown(ins("rec","Recommendation","Reallocate 20% of Consumer marketing budget toward Corporate outreach. Introduce minimum order value thresholds for Consumer discount eligibility ($150+). Launch a Corporate account program with bulk pricing and dedicated account managers."), unsafe_allow_html=True)

elif choice == OPTIONS[3]:
    st.markdown(sec("🌍","Market vs Profit Analysis"), unsafe_allow_html=True)
    mp = df.groupby('market').agg(
        Total_Sales=('sales','sum'),
        Total_Profit=('order profit per order','sum'),
        Avg_Profit=('order profit per order','mean'),
        Orders=('order id','count')
    ).reset_index().round(2)
    mp['Profit_Margin_%'] = (mp['Total_Profit']/mp['Total_Sales']*100).round(2)

    c1,c2 = st.columns(2)
    with c1:
        fig = px.bar(mp.sort_values('Total_Profit'), x='Total_Profit', y='market',
                     orientation='h',
                     color='Total_Profit',
                     color_continuous_scale=[[0,'#EF4444'],[0.5,'#FACC15'],[1,'#22C55E']],
                     text='Total_Profit',title='Total Profit by Market — Gradient Bar')
        fig.update_traces(
    texttemplate='$%{text:,.0f}',
    textposition='outside',
    textfont=dict(size=12, color='black'),
    hovertemplate='<b>%{y}</b><br>Profit: $%{x:,.0f}<extra></extra>'
)
        fig.add_vline(x=0,line_dash='dash',line_color='#F87171')
        fig.update_layout(coloraxis_showscale=False,yaxis_title='')
        pl(fig,380)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig2 = px.scatter(mp, x='Total_Sales', y='Total_Profit',
                          size='Orders', color='market', text='market',
                          color_discrete_sequence=MIXED, size_max=55,
                          title='Sales vs Profit — Bubble (Size=Orders)')
        fig2.update_traces(textposition='top center',
                           hovertemplate='<b>%{text}</b><br>Sales: $%{x:,.0f}<br>Profit: $%{y:,.0f}<extra></extra>')
        fig2.add_hline(y=0,line_dash='dash',line_color='#EF4444')
        pl(fig2,380)
        st.plotly_chart(fig2, use_container_width=True)

    fig3 = px.bar(mp, x='market', y='Profit_Margin_%',
                  color='Profit_Margin_%',
                  color_continuous_scale=[[0,'#EF4444'],[0.5,'#FACC15'],[1,'#22C55E']],
                  text='Profit_Margin_%', title='Profit Margin % by Market')
    fig3.update_traces(texttemplate='%{text:.1f}%',textposition='outside',
                       textfont=dict(color='black'),
                       hovertemplate='<b>%{x}</b><br>Margin: %{y:.2f}%<extra></extra>')
    fig3.update_layout(coloraxis_showscale=False)
    pl(fig3,340)
    st.plotly_chart(fig3, use_container_width=True)
    st.dataframe(mp, use_container_width=True, hide_index=True)
    st.markdown(ins("obs","Observation","Europe has the highest total sales but USCA delivers better profit margins relative to sales volume. LATAM shows high sales but the gradient bar confirms its profit is dangerously close to zero."), unsafe_allow_html=True)
    st.markdown(ins("impact","Business Impact","Operating in low-margin markets requires high volumes to be sustainable. Continued expansion in LATAM without fixing profitability means <b>losses scale proportionally with revenue growth</b> — a classic growth trap."), unsafe_allow_html=True)
    st.markdown(ins("rec","Recommendation","Conduct a market-level P&L analysis. For LATAM: reduce discount rates by minimum 5%, introduce market-specific pricing. For USCA and Europe: invest in retention. Set a minimum 12% profit margin target per market."), unsafe_allow_html=True)

elif choice == OPTIONS[4]:
    st.markdown(sec("🚚","Shipping Mode vs Delivery Delay"), unsafe_allow_html=True)
    sd = df.groupby('shipping mode').agg(
        Avg_Delay=('delay','mean'),
        Late_Orders=('late_delivery_risk','sum'),
        Total_Orders=('order id','count')
    ).reset_index()
    sd['Late_%'] = (sd['Late_Orders']/sd['Total_Orders']*100).round(2)
    sd = sd.round(2)

    c1,c2 = st.columns(2)
    with c1:
        fig = px.bar(sd.sort_values('Late_%'), x='Late_%', y='shipping mode',
                     orientation='h',
                     color='Late_%',
                     color_continuous_scale=[[0,'#22C55E'],[0.5,'#FACC15'],[1,'#EF4444']],
                     text='Late_%', title='Late Delivery % — Gradient Bar')
        fig.update_traces(texttemplate='%{text:.1f}%',textposition='outside',
                          textfont=dict(color='black'),
                          hovertemplate='<b>%{y}</b><br>Late: %{x:.1f}%<extra></extra>')
        fig.update_layout(coloraxis_showscale=False,yaxis_title='')
        pl(fig,360)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig2 = px.violin(df, x='shipping mode', y='delay', color='shipping mode',
                         color_discrete_sequence=P5, box=True, points='outliers',
                         title='Delay Distribution — Violin by Mode')
        fig2.add_hline(y=0,line_dash='dash',line_color='#FACC15',
                       annotation_text='No Delay',annotation_font_color='#FEF08A')
        fig2.update_traces(hovertemplate='Mode: %{x}<br>Delay: %{y}d<extra></extra>')
        fig2.update_layout(showlegend=False)
        pl(fig2,360)
        st.plotly_chart(fig2, use_container_width=True)

    fig3 = px.scatter(df.sample(4000,random_state=1),
                      x='days for shipping (real)', y='delay',
                      color='shipping mode', facet_col='shipping mode',
                      color_discrete_sequence=P5, opacity=0.5,
                      title='Real Shipping Days vs Delay — Faceted by Mode')
    fig3.add_hline(y=0,line_dash='dash',line_color='#FACC15')
    pl(fig3,400)
    st.plotly_chart(fig3, use_container_width=True)
    st.dataframe(sd, use_container_width=True, hide_index=True)
    st.markdown(ins("obs","Observation","Standard Class has the <b>highest late delivery rate (~60%)</b> and widest delay spread — it is both the slowest and most unpredictable shipping mode. Same Day achieves near-zero delays."), unsafe_allow_html=True)
    st.markdown(ins("impact","Business Impact","Since Standard Class handles ~59% of all shipments, its poor performance is directly responsible for the majority of the 54.83% overall late delivery rate — affecting <b>tens of thousands of customers per month</b>."), unsafe_allow_html=True)
    st.markdown(ins("rec","Recommendation","Reduce Standard Class usage from 59% to below 40% by routing orders based on value and urgency. Any order above $200 or from a repeat customer should use Second Class or higher. Negotiate SLA penalties with carriers for delay rates above 20%."), unsafe_allow_html=True)
