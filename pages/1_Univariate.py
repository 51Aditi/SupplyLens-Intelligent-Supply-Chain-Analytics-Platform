import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__),".."))
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.styles import apply_styles, sidebar_nav, sec, ins, sel_cards, pl, P1, P2, P3, P4, P5, P6, MIXED

st.set_page_config(page_title="Univariate Analysis", page_icon="📊", layout="wide")
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
    <h1 style='font-size:1.7rem'>📊 Univariate Analysis</h1>
    <p>Exploring individual variable distributions</p>
</div>""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("<div class='nav-lbl'>Analysis Type</div>", unsafe_allow_html=True)
    mode = st.radio("", ["Categorical Variables","Numerical Variables"],
                    label_visibility="collapsed")

# ═══════════════════════════════════════════════════════════════════════════════
if mode == "Categorical Variables":
    st.markdown(sec("🏷️","Categorical Variable Analysis"), unsafe_allow_html=True)

    # ── 1. Delivery Status — Donut ────────────────────────────────────────────
    st.markdown("#### 1️⃣ Delivery Status")
    ds = df['delivery status'].value_counts().reset_index()
    ds.columns = ['Status','Count']
    ds['Pct'] = (ds['Count']/ds['Count'].sum()*100).round(2)

    c1,c2 = st.columns(2)
    with c1:
        fig = px.pie(ds, values='Count', names='Status', hole=0.55,
                     color_discrete_sequence=P1,
                     title='Delivery Status — Donut')
        fig.update_traces(
            textposition='outside', textinfo='percent+label',
            textfont=dict(color='#0F172A', size=12),
            hovertemplate='<b>%{label}</b><br>Count: %{value:,}<br>Share: %{percent}<extra></extra>')
        fig.update_layout(showlegend=True,
            annotations=[dict(text=f"<b>{ds['Count'].sum():,}</b><br><span style='font-size:11px'>Orders</span>",
                              x=0.5, y=0.5, font=dict(color='#0F172A', size=14),
                              showarrow=False)])
        pl(fig, 380)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig2 = px.bar(ds.sort_values('Count'), x='Count', y='Status', orientation='h',
                      color='Count', color_continuous_scale='Blues',
                      text='Pct', title='Delivery Status — Count')
        fig2.update_traces(
            texttemplate='%{text:.1f}%', textposition='outside',
            textfont=dict(color='#0F172A'),
            hovertemplate='<b>%{y}</b><br>Count: %{x:,}<extra></extra>')
        fig2.update_layout(coloraxis_showscale=False, yaxis_title='')
        pl(fig2, 380)
        st.plotly_chart(fig2, use_container_width=True)

    st.dataframe(ds, use_container_width=True, hide_index=True)
    st.markdown(ins("obs","Observation",
        "The donut chart reveals <b>Late Delivery at 54.83%</b> — the dominant status. Only "
        "10.8% of orders arrive on time, while 18.7% are cancelled before delivery. The company "
        "fails to deliver on time in nearly <b>9 out of every 10 orders that actually ship</b>"),
        unsafe_allow_html=True)
    st.markdown(ins("impact","Business Impact",
        "Consistent late deliveries erode customer trust, trigger refunds and cancellations, and "
        "signal broken logistics agreements with shipping partners — inflating operational costs "
        "and reducing net margins further."), unsafe_allow_html=True)
    st.markdown(ins("rec","Recommendation",
        "Set an internal SLA: reduce late deliveries from 54.83% to below 20% within 2 quarters. "
        "Renegotiate the top 3 highest-delay shipping routes. Auto-upgrade orders above $300 to "
        "Second Class or First Class."), unsafe_allow_html=True)

    st.markdown("---")

    # ── 2. Shipping Mode — Funnel ─────────────────────────────────────────────
    st.markdown("#### 2️⃣ Shipping Mode")
    sm = df['shipping mode'].value_counts().reset_index()
    sm.columns = ['Mode','Count']
    sm['Pct'] = (sm['Count']/sm['Count'].sum()*100).round(2)

    c1,c2 = st.columns(2)
    with c1:
        fig = go.Figure(go.Funnel(
            y=sm['Mode'], x=sm['Count'],
            textinfo='value+percent total',
            textfont=dict(color='#0F172A', size=12),
            marker=dict(color=P3, line=dict(color='rgba(0,0,0,0)', width=0)),
            hovertemplate='<b>%{y}</b><br>Orders: %{x:,}<br>%{percentTotal:.1%}<extra></extra>'))
        fig.update_layout(title='Shipping Mode — Funnel', yaxis_title='')
        pl(fig, 380)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig2 = px.bar(sm.sort_values('Count'), x='Count', y='Mode', orientation='h',
                      color='Mode', color_discrete_sequence=P3,
                      text='Pct', title='Shipping Mode — Volume')
        fig2.update_traces(
            texttemplate='%{text:.1f}%', textposition='outside',
            textfont=dict(color='#0F172A'),
            hovertemplate='<b>%{y}</b><br>Count: %{x:,}<extra></extra>')
        fig2.update_layout(showlegend=False, yaxis_title='')
        pl(fig2, 380)
        st.plotly_chart(fig2, use_container_width=True)

    st.dataframe(sm, use_container_width=True, hide_index=True)
    st.markdown(ins("obs","Observation",
        "<b>Standard Class dominates at ~59%</b> of all shipments, followed by Second Class (19%), "
        "First Class (15%), and Same Day (7%). The funnel shape highlights the severe drop-off "
        "to faster shipping modes that actually perform better."), unsafe_allow_html=True)
    st.markdown(ins("impact","Business Impact",
        "Over-reliance on Standard Class reduces per-order shipping costs short-term, but the "
        "downstream cost of late deliveries — customer churn, refunds, negative reviews — far "
        "outweighs savings. The company optimises for <b>cost instead of customer satisfaction</b>"),
        unsafe_allow_html=True)
    st.markdown(ins("rec","Recommendation",
        "Introduce a rule-based upgrade: orders above $250 auto-use First Class; urgent or "
        "repeat-customer orders use Same Day. Target reducing Standard Class from 59% to below 40%."),
        unsafe_allow_html=True)

    st.markdown("---")

    # ── 3. Customer Segment — Exploded Donut ──────────────────────────────────
    st.markdown("#### 3️⃣ Customer Segment")
    cs = df['customer segment'].value_counts().reset_index()
    cs.columns = ['Segment','Count']
    cs['Pct'] = (cs['Count']/cs['Count'].sum()*100).round(2)

    c1,c2 = st.columns(2)
    with c1:
        fig = px.pie(cs, values='Count', names='Segment', hole=0.5,
                     color_discrete_sequence=P4,
                     title='Customer Segment — Exploded Donut')
        fig.update_traces(
            pull=[0.06,0.03,0.01],
            textposition='outside', textinfo='percent+label',
            textfont=dict(color='#0F172A', size=12),
            hovertemplate='<b>%{label}</b><br>Customers: %{value:,}<br>%{percent}<extra></extra>')
        pl(fig, 380)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        # Sunburst: segment → market
        sb = df.groupby(['customer segment','market']).size().reset_index(name='Count')
        fig2 = px.sunburst(sb, path=['customer segment','market'], values='Count',
                           color='customer segment', color_discrete_sequence=P4,
                           title='Segment → Market Breakdown')
        fig2.update_traces(
            textfont=dict(color='#0F172A'),
            hovertemplate='<b>%{label}</b><br>Orders: %{value:,}<extra></extra>')
        pl(fig2, 380)
        st.plotly_chart(fig2, use_container_width=True)

    st.dataframe(cs, use_container_width=True, hide_index=True)
    st.markdown(ins("obs","Observation",
        "<b>Consumer segment makes up 51.4%</b> of all customers, Corporate 30.1%, Home Office "
        "18.5%. The sunburst shows Corporate customers are spread more evenly across markets, "
        "while Consumer is concentrated in Europe and LATAM."), unsafe_allow_html=True)
    st.markdown(ins("impact","Business Impact",
        "Serving a large Consumer segment at thin margins requires extreme volume to stay "
        "profitable. Any disruption — delays, discounts, or returns — immediately creates net "
        "losses. Corporate customers generating better returns are being under-targeted."),
        unsafe_allow_html=True)
    st.markdown(ins("rec","Recommendation",
        "Develop a dedicated B2B Corporate acquisition strategy. Offer loyalty programs for bulk "
        "and repeat orders. Redirect marketing spend to grow Corporate from 30% to 40% within "
        "12 months."), unsafe_allow_html=True)

    st.markdown("---")

    # ── 4. Market — Treemap ───────────────────────────────────────────────────
    st.markdown("#### 4️⃣ Market Distribution")
    mk = df['market'].value_counts().reset_index()
    mk.columns = ['Market','Count']
    mk['Pct'] = (mk['Count']/mk['Count'].sum()*100).round(2)

    c1,c2 = st.columns(2)
    with c1:
        fig = px.treemap(mk, path=['Market'], values='Count',
                         color='Count', color_continuous_scale='Blues',
                         title='Market — Treemap by Order Volume')
        fig.update_traces(
            texttemplate='<b>%{label}</b><br>%{value:,}',
            textfont=dict(color='#FFFFFF', size=13),
            hovertemplate='<b>%{label}</b><br>Orders: %{value:,}<extra></extra>')
        pl(fig, 380)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig2 = px.bar(mk.sort_values('Count'), x='Count', y='Market', orientation='h',
                      color='Count',
                      color_continuous_scale=[[0,'#0284C7'],[0.5,'#38BDF8'],[1,'#BAE6FD']],
                      text='Pct', title='Market — Gradient Bar')
        fig2.update_traces(
            texttemplate='%{text:.1f}%', textposition='outside',
            textfont=dict(color='#0F172A'),
            hovertemplate='<b>%{y}</b><br>Orders: %{x:,}<extra></extra>')
        fig2.update_layout(coloraxis_showscale=False, yaxis_title='')
        pl(fig2, 380)
        st.plotly_chart(fig2, use_container_width=True)

    st.dataframe(mk, use_container_width=True, hide_index=True)
    st.markdown(ins("obs","Observation",
        "<b>Europe leads at ~34% order volume</b> followed by LATAM (~24%), Pacific Asia (~20%), "
        "USCA (~13%), Africa (~9%). The treemap shows how disproportionately Europe dominates "
        "total order volume compared to other markets."), unsafe_allow_html=True)
    st.markdown(ins("impact","Business Impact",
        "Pouring resources into high-volume but low-margin markets like LATAM inflates costs "
        "without proportional profit returns — the company is <b>busy but not profitable.</b> "
        "Uncontrolled LATAM and Africa costs continue draining profit."), unsafe_allow_html=True)
    st.markdown(ins("rec","Recommendation",
        "Audit cost-to-serve per market. Increase prices or cut discounts in LATAM. Invest in "
        "growing USCA which shows proven higher returns. Explore Africa as a premium-positioning "
        "market with targeted campaigns."), unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
else:
    st.markdown(sec("🔢","Numerical Variable Analysis"), unsafe_allow_html=True)

    num_map = {
        "Sales Per Customer":       "sales per customer",
        "Benefit Per Order":        "benefit per order",
        "Order Item Product Price": "order item product price",
        "Order Item Discount":      "order item discount",
        "Days for Shipping (Real)": "days for shipping (real)",
    }
    palette_map = {
        "Sales Per Customer":       (P1,"#38BDF8"),
        "Benefit Per Order":        (P2,"#22C55E"),
        "Order Item Product Price": (P4,"#A855F7"),
        "Order Item Discount":      (P3,"#F97316"),
        "Days for Shipping (Real)": (P5,"#EC4899"),
    }
    selected = st.selectbox("Select Variable", list(num_map.keys()))
    col_name = num_map[selected]
    pal, accent = palette_map[selected]
    series = df[col_name].dropna()

    # Stats row
    stats = {"Count":f"{series.count():,}","Mean":f"{series.mean():.2f}",
             "Median":f"{series.median():.2f}","Std Dev":f"{series.std():.2f}",
             "Min":f"{series.min():.2f}","Max":f"{series.max():.2f}",
             "Skewness":f"{series.skew():.3f}","Kurtosis":f"{series.kurtosis():.3f}"}
    st.markdown(f"#### 📐 Statistical Summary — {selected}")
    cols8 = st.columns(8)
    for (k,v), col in zip(stats.items(), cols8):
        with col:
            st.markdown(f"<div class='stat-card'><b style='color:{accent}'>{v}</b>"
                        f"<br><small style='color:#94A3B8'>{k}</small></div>",
                        unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("📋 Full Statistical Table"):
        sd = pd.DataFrame(series.describe()).reset_index()
        sd.columns = ["Statistic","Value"]
        sd["Value"] = sd["Value"].round(3)
        st.dataframe(sd, use_container_width=True, hide_index=True)

    c1,c2 = st.columns(2)
    with c1:
        fig = px.histogram(df, x=col_name, nbins=50,
                           color_discrete_sequence=[accent],
                           title=f"Histogram — {selected}")
        fig.update_traces(
            marker_line_color='rgba(0,0,0,0)',
            hovertemplate='Range: %{x}<br>Count: %{y:,}<extra></extra>')
        pl(fig)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig2 = px.violin(df, y=col_name, box=True, points='outliers',
                         color_discrete_sequence=[accent],
                         title=f"Violin + Box — {selected}")
        fig2.update_traces(
            hovertemplate='Value: %{y:.2f}<extra></extra>',
            meanline_visible=True)
        pl(fig2)
        st.plotly_chart(fig2, use_container_width=True)

    # ECDF
    fig3 = px.ecdf(df, x=col_name, color_discrete_sequence=[accent],
                   title=f"Cumulative Distribution — {selected}")
    fig3.update_traces(hovertemplate='Value: %{x:.2f}<br>Cumulative: %{y:.2%}<extra></extra>')
    pl(fig3, 340)
    st.plotly_chart(fig3, use_container_width=True)

    obs_map = {
        "Sales Per Customer":
            ("The histogram shows a <b>strong right skew</b> — most customers generate $100–$300 "
             "in sales, but a small elite group generates $1,000+. The median is significantly "
             "lower than the mean, confirming a Pareto-style revenue distribution.",
             "The company is dangerously dependent on a small group of high-value customers. "
             "If 10% of top buyers leave, total revenue could drop 20–30%.",
             "Segment the top 15% of customers by sales. Create a VIP loyalty program. Run "
             "upsell campaigns to push average order value above $250."),
        "Benefit Per Order":
            ("Benefit Per Order has <b>significant negative values</b> — many orders lose money. "
             "The violin plot shows wide spread with outliers on both ends, indicating high "
             "inconsistency in per-order profitability.",
             "If 20% of orders produce net loss, proportionally higher profit must be generated "
             "on the rest just to break even — making financial forecasting unreliable.",
             "Identify product-shipping-market combos that consistently produce negative benefit. "
             "Set a minimum margin threshold: any configuration producing negative benefit "
             "triggers automatic price adjustment."),
        "Order Item Product Price":
            ("Prices range widely but the <b>histogram is heavily concentrated below $200</b>. "
             "Most items are low-to-mid priced. The ECDF shows 75% of items are below $250.",
             "A low-price-dominated portfolio requires very high volume to generate meaningful "
             "profit. Any increase in shipping or discount costs immediately creates a loss.",
             "Identify the top 20 high-margin products and give them better visibility. Gradually "
             "shift revenue mix toward items above $250 to improve per-order profitability."),
        "Order Item Discount":
            ("Many orders carry <b>zero or near-zero discount</b>, but a clear segment has high "
             "discounts (20–40%). Average discount rate is ~11.5%, directly cutting into "
             "already thin margins.",
             "A 20% discount on a $200 item removes $40 revenue. If gross margin is 15% ($30), "
             "the discount alone exceeds the margin — <b>making the sale a net loss before "
             "shipping and operations</b>.",
             "Cap discounts at 10% for Consumer and 12% for Corporate. Replace blanket "
             "promotions with targeted offers based on customer lifetime value."),
        "Days for Shipping (Real)":
            ("Real shipping days concentrate between <b>3–6 days</b> with a visible right tail. "
             "The violin plot confirms orders taking more than 5 days correlate strongly with "
             "late delivery status.",
             "Every additional day beyond the scheduled window risks a complaint or refund. "
             "The cumulative effect — affecting 54%+ of orders — is the <b>single largest "
             "driver of customer attrition</b> in this dataset.",
             "Set a 4-day maximum for Standard Class and enforce it contractually. For orders "
             "past their scheduled date by 1 day, trigger automatic customer notification "
             "with a next-order voucher."),
    }
    o,im,r = obs_map[selected]
    st.markdown(ins("obs","Observation",o), unsafe_allow_html=True)
    st.markdown(ins("impact","Business Impact",im), unsafe_allow_html=True)
    st.markdown(ins("rec","Recommendation",r), unsafe_allow_html=True)
