import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__),".."))
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.styles import apply_styles, sec, ins, kpi, pl, P1, P2, P3, P4, P5, P6, MIXED

st.set_page_config(page_title="Executive Dashboard", page_icon="🎯", layout="wide")
apply_styles()

@st.cache_data
def load():
    df = pd.read_csv("data/supply_chain_cleaned.csv")
    df.columns = df.columns.str.strip().str.lower()
    return df
df_full = load()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class='sb-brand'>
        <div style='font-size:2rem'>📦</div>
        <h2>Supply Chain</h2>
        <p>Loss Analysis Dashboard</p>
    </div>""", unsafe_allow_html=True)
    st.markdown("<div class='nav-lbl'>Pages</div>", unsafe_allow_html=True)
    st.page_link("app.py",                  label="🏠  Home")
    st.page_link("pages/1_Univariate.py",   label="📊  Univariate Analysis")
    st.page_link("pages/2_Bivariate.py",    label="📈  Bivariate Analysis")
    st.page_link("pages/3_Multivariate.py", label="🔥  Multivariate Analysis")
    st.page_link("pages/4_Dashboard.py",    label="🎯  Executive Dashboard")
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<div class='nav-lbl'>🎛️ Filters</div>", unsafe_allow_html=True)

    markets   = ["All"]+sorted(df_full['market'].dropna().unique().tolist())
    segments  = ["All"]+sorted(df_full['customer segment'].dropna().unique().tolist())
    shipmodes = ["All"]+sorted(df_full['shipping mode'].dropna().unique().tolist())
    seasons   = ["All"]+sorted(df_full['season'].dropna().unique().tolist())

    sel_market  = st.selectbox("Market",           markets)
    sel_segment = st.selectbox("Customer Segment", segments)
    sel_ship    = st.selectbox("Shipping Mode",    shipmodes)
    sel_season  = st.selectbox("Season",           seasons)
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<small style='color:#475569;font-size:11px;'>📁 supply_chain_cleaned.csv<br>📌 180,519 records · 45 columns</small>", unsafe_allow_html=True)

df = df_full.copy()
if sel_market  != "All": df = df[df['market']           == sel_market]
if sel_segment != "All": df = df[df['customer segment'] == sel_segment]
if sel_ship    != "All": df = df[df['shipping mode']    == sel_ship]
if sel_season  != "All": df = df[df['season']           == sel_season]

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class='hero' style='padding:28px 36px'>
    <h1 style='font-size:1.7rem'>🎯 Executive Dashboard</h1>
    <p>Real-time Supply Chain Performance Overview</p>
</div>""", unsafe_allow_html=True)
st.markdown(f"<small style='color:#475569'>📊 Showing "
            f"<b style='color:#38BDF8'>{len(df):,}</b> records based on current filters</small><br><br>",
            unsafe_allow_html=True)

# ── KPIs ──────────────────────────────────────────────────────────────────────
total_sales     = df['sales'].sum()
total_profit    = df['order profit per order'].sum()
total_orders    = df['order id'].nunique()
total_customers = df['customer id'].nunique()
late_pct        = round(df['late_delivery_risk'].sum()/len(df)*100,1) if len(df)>0 else 0
avg_discount    = round(df['order item discount rate'].mean()*100,2) if len(df)>0 else 0
profit_margin   = round(total_profit/total_sales*100,2) if total_sales>0 else 0
avg_ship_days   = round(df['days for shipping (real)'].mean(),1) if len(df)>0 else 0

st.markdown(sec("📌","Key Performance Indicators"), unsafe_allow_html=True)
c1,c2,c3,c4 = st.columns(4)
for col,(icon,label,val,sub,cls) in zip([c1,c2,c3,c4],[
    ("💰","Total Sales",    f"${total_sales/1e6:.2f}M","Revenue Generated","kpi-sub"),
    ("📈","Total Profit",   f"${total_profit/1e3:.1f}K","Net Profit","kpi-sub" if total_profit>0 else "kpi-danger"),
    ("🛒","Unique Orders",  f"{total_orders:,}","Order Count","kpi-sub"),
    ("👥","Customers",      f"{total_customers:,}","Unique Customers","kpi-sub"),
]):
    with col: st.markdown(kpi(icon,label,val,sub,cls), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
c5,c6,c7,c8 = st.columns(4)
for col,(icon,label,val,sub,cls) in zip([c5,c6,c7,c8],[
    ("⏰","Late Delivery",  f"{late_pct}%",        "Target below 20%","kpi-danger" if late_pct>30 else "kpi-sub"),
    ("🏷️","Avg Discount",  f"{avg_discount}%",    "Margin Impact",   "kpi-warn"   if avg_discount>10 else "kpi-sub"),
    ("📊","Profit Margin",  f"{profit_margin}%",   "Overall Margin",  "kpi-sub"    if profit_margin>5  else "kpi-danger"),
    ("🚚","Avg Ship Days",  f"{avg_ship_days}d",   "Delivery Speed",  "kpi-warn"   if avg_ship_days>4  else "kpi-sub"),
]):
    with col: st.markdown(kpi(icon,label,val,sub,cls), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Sales & Profit — Waterfall ────────────────────────────────────────────────
st.markdown(sec("💰","Sales & Profit Analysis"), unsafe_allow_html=True)
c1,c2 = st.columns(2)
with c1:
    sbm = df.groupby('market')['sales'].sum().reset_index().sort_values('sales',ascending=False)
    fig = px.bar(sbm, x='market', y='sales', color='sales',
                 color_continuous_scale=[[0,'#0284C7'],[1,'#BAE6FD']],
                 text='sales', title='Total Sales by Market — Gradient Bar')
    fig.update_traces(texttemplate='$%{text:,.0f}',textposition='outside',
                      textfont=dict(color='black'),
                      hovertemplate='<b>%{x}</b><br>Sales: $%{y:,.0f}<extra></extra>')
    fig.update_layout(coloraxis_showscale=False,showlegend=False)
    pl(fig)
    st.plotly_chart(fig, use_container_width=True)
with c2:
    pbm = df.groupby('market')['order profit per order'].sum().reset_index()
    pbm.columns = ['market','profit']
    pbm = pbm.sort_values('profit',ascending=False)
    fig2 = go.Figure(go.Waterfall(
        name='Profit', orientation='v',
        x=pbm['market'].tolist(),
        y=pbm['profit'].tolist(),
        text=[f"${v:,.0f}" for v in pbm['profit']],
        textposition='outside',
        textfont=dict(color='black',size=11),
        connector=dict(line=dict(color='#334155',width=1)),
        increasing=dict(marker=dict(color='#22C55E')),
        decreasing=dict(marker=dict(color='#EF4444')),
        hovertemplate='<b>%{x}</b><br>Profit: $%{y:,.0f}<extra></extra>'))
    fig2.update_layout(title='Total Profit by Market — Waterfall Chart',showlegend=False)
    pl(fig2)
    st.plotly_chart(fig2, use_container_width=True)

# ── Delivery Performance ──────────────────────────────────────────────────────
st.markdown(sec("🚚","Delivery Performance"), unsafe_allow_html=True)
c1,c2,c3 = st.columns(3)
with c1:
    ds = df['delivery status'].value_counts().reset_index()
    ds.columns = ['Status','Count']
    fig = px.pie(ds, values='Count', names='Status', hole=0.5,
                 color_discrete_sequence=['#EF4444','#38BDF8','#22C55E','#F97316'],
                 title='Delivery Status — Donut')
    fig.update_traces(textposition='outside',textinfo='percent+label',
                      textfont=dict(color='black',size=11),
                      hovertemplate='<b>%{label}</b><br>Count: %{value:,}<br>%{percent}<extra></extra>')
    pl(fig,360)
    st.plotly_chart(fig, use_container_width=True)
with c2:
    sp = df.groupby('shipping mode').agg(Late_Pct=('late_delivery_risk','mean')).reset_index()
    sp['Late_Pct'] = (sp['Late_Pct']*100).round(1)
    fig2 = go.Figure(go.Funnel(
        y=sp.sort_values('Late_Pct',ascending=False)['shipping mode'],
        x=sp.sort_values('Late_Pct',ascending=False)['Late_Pct'],
        textinfo='value+percent total',
        textfont=dict(color='#E2E8F0',size=12),
        marker=dict(color=['#EF4444','#F97316','#FACC15','#22C55E']),
        hovertemplate='<b>%{y}</b><br>Late: %{x:.1f}%<extra></extra>'))
    fig2.update_layout(title='Late Delivery % — Funnel by Mode',yaxis_title='')
    pl(fig2,360)
    st.plotly_chart(fig2, use_container_width=True)
with c3:
    dm = df.groupby('market')['delay'].mean().reset_index()
    dm.columns = ['Market','Avg Delay Days']
    dm = dm.sort_values('Avg Delay Days',ascending=True).round(2)
    fig3 = px.bar(dm, x='Avg Delay Days', y='Market', orientation='h',
                  color='Avg Delay Days',
                  color_continuous_scale=[[0,'#22C55E'],[0.5,'#FACC15'],[1,'#EF4444']],
                  text='Avg Delay Days', title='Avg Delay Days by Market')
    fig3.update_traces(texttemplate='%{text:.1f}d',textposition='outside',
                       textfont=dict(color='black'),
                       hovertemplate='<b>%{y}</b><br>Avg Delay: %{x:.2f}d<extra></extra>')
    fig3.add_vline(x=0,line_dash='dash',line_color='#4ADE80')
    fig3.update_layout(coloraxis_showscale=False,yaxis_title='')
    pl(fig3,360)
    st.plotly_chart(fig3, use_container_width=True)

st.markdown(ins("obs","Observation — Delivery Performance",
    "Late Delivery dominates at <b>54.83%</b> of all orders. The funnel confirms Standard Class has "
    "the worst on-time rate. Every market shows positive average delay — no market consistently "
    "delivers on the promised date."), unsafe_allow_html=True)
st.markdown(ins("impact","Business Impact",
    "A company where more than half of deliveries are late cannot build loyalty at scale. Each "
    "late delivery triggers compensation costs, refund processing, and support tickets that "
    "reduce effective profit per order."), unsafe_allow_html=True)
st.markdown(ins("rec","Recommendation",
    "Set a 90-day goal: reduce late delivery from 54.83% to below 35% by upgrading all Standard "
    "Class orders above $200 to Second Class. Monitor weekly delay rates per market with "
    "escalation when any market exceeds 30% late in a given week."), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Customer Segment ──────────────────────────────────────────────────────────
st.markdown(sec("👥","Customer Segment Performance"), unsafe_allow_html=True)
seg = df.groupby('customer segment').agg(
    Total_Sales=('sales','sum'), Total_Profit=('order profit per order','sum'),
    Orders=('order id','count'), Customers=('customer id','nunique'),
    Avg_Discount=('order item discount rate','mean')
).reset_index().round(2)
seg['Profit_Margin_%'] = (seg['Total_Profit']/seg['Total_Sales']*100).round(2)
seg['Avg_Discount_%']  = (seg['Avg_Discount']*100).round(2)

c1,c2 = st.columns(2)
with c1:
    # Diverging bar
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Total Sales', x=seg['Total_Sales'],
                         y=seg['customer segment'], orientation='h',
                         marker_color='#38BDF8',
                         hovertemplate='<b>%{y}</b><br>Sales: $%{x:,.0f}<extra></extra>'))
    fig.add_trace(go.Bar(name='Total Profit', x=seg['Total_Profit'],
                         y=seg['customer segment'], orientation='h',
                         marker_color='#22C55E',
                         hovertemplate='<b>%{y}</b><br>Profit: $%{x:,.0f}<extra></extra>'))
    fig.update_layout(barmode='group',title='Sales vs Profit — Grouped Horizontal Bars',yaxis_title='')
    pl(fig)
    st.plotly_chart(fig, use_container_width=True)
with c2:
    st.markdown("#### 📋 Segment KPI Table")
    st.dataframe(seg[['customer segment','Total_Sales','Total_Profit',
                       'Orders','Customers','Profit_Margin_%','Avg_Discount_%']],
                 use_container_width=True, hide_index=True)

# ── Top Categories — Lollipop ─────────────────────────────────────────────────
st.markdown(sec("🏆","Top Categories by Performance"), unsafe_allow_html=True)
c1,c2 = st.columns(2)
with c1:
    tc = df.groupby('category name')['sales'].sum().nlargest(10).reset_index()
    tc.columns = ['Category','Total Sales']
    tc = tc.sort_values('Total Sales')
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=tc['Total Sales'], y=tc['Category'], mode='markers',
        marker=dict(color='#38BDF8',size=13,line=dict(color='#FFFFFF',width=1.5)),
        hovertemplate='<b>%{y}</b><br>Sales: $%{x:,.0f}<extra></extra>'))
    for _,row in tc.iterrows():
        fig.add_shape(type='line',x0=0,x1=row['Total Sales'],
                      y0=row['Category'],y1=row['Category'],
                      line=dict(color='rgba(56,189,248,0.35)',width=2))
    fig.update_layout(title='Top 10 Categories by Sales — Lollipop',yaxis_title='')
    pl(fig,420)
    st.plotly_chart(fig, use_container_width=True)
with c2:
    tp = df.groupby('category name')['order profit per order'].sum().nlargest(10).reset_index()
    tp.columns = ['Category','Total Profit']
    tp = tp.sort_values('Total Profit')
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=tp['Total Profit'], y=tp['Category'], mode='markers',
        marker=dict(color='#22C55E',size=13,line=dict(color='#FFFFFF',width=1.5)),
        hovertemplate='<b>%{y}</b><br>Profit: $%{x:,.0f}<extra></extra>'))
    for _,row in tp.iterrows():
        fig2.add_shape(type='line',x0=0,x1=row['Total Profit'],
                       y0=row['Category'],y1=row['Category'],
                       line=dict(color='rgba(34,197,94,0.35)',width=2))
    fig2.update_layout(title='Top 10 Categories by Profit — Lollipop',yaxis_title='')
    pl(fig2,420)
    st.plotly_chart(fig2, use_container_width=True)

# ── Loss Categories ───────────────────────────────────────────────────────────
st.markdown(sec("🔴","Loss-Making Categories"), unsafe_allow_html=True)
lc = df.groupby('category name').agg(
    Total_Profit=('order profit per order','sum'),
    Orders=('order id','count'),
    Avg_Margin=('profit_margin','mean')
).reset_index()
lc = lc[lc['Total_Profit']<0].sort_values('Total_Profit').round(2)
if not lc.empty:
    lc_sorted = lc.sort_values('Total_Profit',ascending=False)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=lc_sorted['Total_Profit'], y=lc_sorted['category name'], mode='markers',
        marker=dict(color='#EF4444',size=13,line=dict(color='#FFFFFF',width=1.5)),
        hovertemplate='<b>%{y}</b><br>Loss: $%{x:,.0f}<extra></extra>'))
    for _,row in lc_sorted.iterrows():
        fig.add_shape(type='line',x0=row['Total_Profit'],x1=0,
                      y0=row['category name'],y1=row['category name'],
                      line=dict(color='rgba(239,68,68,0.35)',width=2))
    fig.add_vline(x=0,line_dash='dash',line_color='#F87171')
    fig.update_layout(title='Loss-Making Categories — Lollipop',yaxis_title='')
    pl(fig,max(300,len(lc)*40))
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(lc, use_container_width=True, hide_index=True)
    st.markdown(ins("obs","Observation","These categories have generated <b>negative total profit</b> despite high order volumes. The lollipop chart shows how far each category extends into loss territory."), unsafe_allow_html=True)
    st.markdown(ins("impact","Business Impact","Every order in a loss-making category is a direct financial drain. High order volumes in these categories signal <b>accelerated losses at scale</b>. Continued investment widens the profit gap and drives the overall low net margin of 10.7%."), unsafe_allow_html=True)
    st.markdown(ins("rec","Recommendation","Stop all discount promotions for loss-making categories immediately. Within 30 days, if selling price cannot cover COGS + shipping + 10% margin, raise prices or discontinue. Redirect freed budget toward the top 5 most profitable categories."), unsafe_allow_html=True)
else:
    st.success("✅ No loss-making categories under current filter selection.")

st.markdown("<br>", unsafe_allow_html=True)

# ── Management Recommendations ────────────────────────────────────────────────
st.markdown("""
<div style='background:linear-gradient(135deg,#0F172A,#1E293B);
            border:1px solid #1E3A5F; border-radius:16px; padding:24px 28px; margin:10px 0;
            position:relative; overflow:hidden;'>
    <div style='position:absolute;top:0;left:0;right:0;height:2px;
                background:linear-gradient(90deg,#38BDF8,#A855F7,#22C55E,#F97316);'></div>
    <h2 style='color:#FFFFFF;margin:0 0 4px;font-size:1.2rem;font-weight:800;'>
        📋 Management Recommendations</h2>
    <p style='color:#94A3B8;margin:0;font-size:.84rem;'>
        Six strategic actions derived from data analysis — for executive decision-making</p>
</div>""", unsafe_allow_html=True)

RECS = [
    ("#EF4444","🔴","Priority 1 — Reduce Late Deliveries",
     "54.83% of all orders are delivered late. Standard Class shipping contributes ~60% of all delays across every market.",
     "Customer churn will accelerate. Repeat purchase rate will decline. Refunds and compensation costs will continue eroding margins each quarter.",
     "• Upgrade all orders above $200 from Standard to Second Class automatically\n• Renegotiate carrier SLAs with penalties for delay rates above 15%\n• Target: Reduce late delivery to below 25% within 6 months\n• KPI: Weekly late delivery % per market on Executive Dashboard"),
    ("#F97316","🟠","Priority 2 — Optimise Discount Strategy",
     "Average discount rate is 11.5%. Correlation analysis proves higher discount rates directly reduce profit per order.",
     "Blanket discounting destroys margins silently. High-discount campaigns drive volume but create net losses on every discounted order.",
     "• Cap Consumer discounts at 8%; Corporate at 12% (volume-based only)\n• Remove discounts from all loss-making product categories\n• Only trigger discounts for orders above $150 minimum\n• KPI: Avg discount rate monthly — target below 7% within 1 year"),
    ("#22C55E","🟢","Priority 3 — Focus on High-Profit Categories",
     "Top 5 categories generate a disproportionate share of total profit. Several categories actively generate net losses at high order volumes.",
     "Investment in loss-making categories drains logistics, storage, and marketing budgets that could be redeployed into profitable product lines.",
     "• Increase inventory and marketing for top 5 profit categories by 20%\n• Raise prices on loss-making categories by 10–15% or remove discount eligibility\n• Discontinue categories still loss-making after repricing within 90 days\n• KPI: Monthly profit per category ranking reviewed by procurement team"),
    ("#38BDF8","🔵","Priority 4 — Improve Shipping Efficiency",
     "Real shipping days consistently exceed scheduled days in every market and for every shipping mode. The gap is systematic, not occasional.",
     "Customers receive broken delivery promises every time they order. Brand reputation damage compounds through negative reviews and rising operational costs.",
     "• Replace optimistic estimates with data-driven realistic delivery windows at checkout\n• Build an internal real-time shipping performance tracker per carrier per region\n• Conduct quarterly carrier performance reviews\n• KPI: Real vs scheduled days gap — target below 0.5 days average"),
    ("#A855F7","🟣","Priority 5 — Target Profitable Customer Segments",
     "Consumer segment dominates at 51% of orders but delivers the lowest profit margins. Corporate (30%) delivers the highest per-order profit but grows slowly.",
     "As Consumer segment grows without margin improvement, total company profit stagnates even as revenue increases — a high-revenue, low-profit trap.",
     "• Launch B2B Corporate acquisition campaign targeting SMEs in Europe and USCA\n• Offer Corporate accounts: volume pricing at $500+, dedicated support, net-30 terms\n• For Consumer: focus retention of top 15% spenders, not new low-value acquisition\n• KPI: Grow Corporate share from 30% to 38% within 12 months"),
    ("#06B6D4","🩵","Priority 6 — Market Profitability Realignment",
     "USCA generates the best profit margins despite not having the highest order volume. LATAM shows high sales but dangerously thin margins.",
     "Continued volume growth in LATAM without margin fixes will disproportionately increase costs — the company risks structural unprofitability at scale.",
     "• Publish monthly cost-to-serve per market for leadership review\n• LATAM: run 60-day test — reduce discounts 5%, measure volume vs profit impact\n• USCA: invest in customer retention to capitalise on proven profitability\n• KPI: All markets must achieve minimum 10% profit margin within 18 months"),
]

c1,c2 = st.columns(2)
for i,(color,emoji,title,obs_t,imp_t,rec_t) in enumerate(RECS):
    col = c1 if i%2==0 else c2
    rec_html = rec_t.replace("\n","<br>")
    with col:
        st.markdown(f"""
        <div class='mgmt-card'>
            <div class='mgmt-title' style='color:{color}'>{emoji} {title}</div>
            <div class='ins-obs'>
                <b>📊 Current State:</b><span>{obs_t}</span>
            </div>
            <div class='ins-impact'>
                <b>🔥 Impact if Unresolved:</b><span>{imp_t}</span>
            </div>
            <div class='ins-rec'>
                <b>✅ Action Plan:</b><span>{rec_html}</span>
            </div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<div style='text-align:center;color:#475569;font-size:.78rem;"
            "border-top:1px solid #1E3A5F;padding-top:12px;'>"
            "📦 Supply Chain Loss Analysis &nbsp;&nbsp;</div>",
            unsafe_allow_html=True)
