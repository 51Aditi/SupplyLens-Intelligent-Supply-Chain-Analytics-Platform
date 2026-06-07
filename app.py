import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.styles import (apply_styles, sidebar_nav, kpi, sec,
                          quick_insights, pl, MIXED, P1, P2)

st.set_page_config(page_title="Supply Chain Loss Analysis",
                   page_icon="📦", layout="wide",
                   initial_sidebar_state="expanded")
apply_styles()
sidebar_nav()



@st.cache_data
def load():
    st.markdown("""
# 🏭 ➡️ 🚛 ➡️ 📦 ➡️ 🏢
## Supply Chain Loss Analysis Dashboard
""")
    df = pd.read_csv("data/supply_chain_cleaned.csv")
    df.columns = df.columns.str.strip().str.lower()
    return df
df = load()

# # =====================================================
# BUSINESS PROBLEM
# =====================================================

st.markdown("## 🎯 Business Problem")

st.info("""
The company faces challenges related to delivery delays,
profit reduction, inefficient shipping operations, and
inconsistent performance across markets and customer segments.

This project analyzes supply chain operations to identify
the major drivers of losses and provide actionable business recommendations.
""")

# =====================================================
# OBJECTIVES
# =====================================================

st.markdown("## 📌 Project Objectives")

col1, col2 = st.columns(2)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div style="
        background:#E8F5E9;
        padding:22px;
        border-radius:10px;
        min-height:220px;
        font-size:18px;
        font-weight:600;
        color:#0F172A;
        line-height:2;">
        ✓ Identify factors causing profit reduction<br>
        ✓ Analyze delivery performance<br>
        ✓ Evaluate shipping efficiency<br>
        ✓ Study customer behavior
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="
        background:#E8F5E9;
        padding:22px;
        border-radius:10px;
        min-height:220px;
        font-size:18px;
        font-weight:600;
        color:#0F172A;
        line-height:2;">
        ✓ Compare market profitability<br>
        ✓ Analyze discount impact<br>
        ✓ Improve operational efficiency<br>
        ✓ Generate business recommendations
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# ANALYSIS WORKFLOW
# =====================================================

st.markdown("## 🔄 Analysis Workflow")

c1, c2, c3, c4 = st.columns(4)

c1.info("📂 Data Collection")
c2.info("🧹 Data Cleaning")
c3.info("📊 Exploratory Analysis")
c4.info("💡 Business Insights")

# =====================================================
# FACTORS ANALYZED
# =====================================================

st.markdown("## 🔍 Factors Influencing Company Losses")

c1, c2, c3, c4 = st.columns(4)

c1.warning("🚚 Delivery Status")
c2.warning("📦 Shipping Mode")
c3.warning("💰 Discount Rate")
c4.warning("📈 Profit Margin")

c5, c6, c7, c8 = st.columns(4)

c5.warning("🌍 Market Performance")
c6.warning("👥 Customer Segment")
c7.warning("🏷 Product Category")
c8.warning("⏱ Shipping Delay")

# =====================================================
# EXPECTED OUTCOMES
# =====================================================

st.markdown("## 🚀 Expected Business Outcomes")

st.success("""
• Reduce delivery delays and improve customer satisfaction.

• Optimize shipping operations and logistics efficiency.

• Improve profit margins through better pricing and discount strategies.

• Identify underperforming markets and product categories.

• Improve customer profitability and retention.

• Support data-driven business decision making.
""")

# =====================================================
# DATASET OVERVIEW
# =====================================================

st.markdown("## 📊 Dataset Overview")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric("Rows", f"{df.shape[0]:,}")

with c2:
    st.metric("Columns", df.shape[1])

with c3:
    st.metric("Missing Values", int(df.isnull().sum().sum()))

# =====================================================
# COLUMN REFERENCE
# =====================================================

with st.expander("📋 View Column Reference"):
    col_info = pd.DataFrame({
        "Column Name": df.columns,
        "Data Type": df.dtypes.astype(str)
    })
    st.dataframe(col_info, use_container_width=True)




# =====================================================
# SAMPLE DATA PREVIEW
# =====================================================

with st.expander("🔍 View Sample Data (First 10 Rows)"):
    st.dataframe(df.head(10), use_container_width=True)