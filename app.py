import streamlit as st
import pandas as pd
import numpy as np
import statsmodels.api as sm
from datetime import timedelta

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Revenue Optimization Engine", layout="wide")
st.title("📈 Dynamic Pricing & Revenue Optimization Engine")
st.markdown("Simulate the financial impact of price changes utilizing statistical Price Elasticity of Demand (PED).")

# --- DATA PIPELINE & MODELING (Cached to prevent reloading on slider move) ---
@st.cache_data
def load_and_model_data():
    np.random.seed(42)
    categories = ['Electronics', 'Apparel', 'Home Goods', 'Fitness', 'Accessories']
    
    # 1. Generate Base Products
    products = []
    for i in range(50):
        cat = np.random.choice(categories)
        cost = round(np.random.lognormal(mean=3.5, sigma=0.8), 2)
        true_ped = round(np.random.uniform(-2.5, -0.5), 2)
        products.append({'Product_ID': f'PRD_{i:03}', 'Category': cat, 'Base_Cost': cost, 'True_PED': true_ped})
    df_prod = pd.DataFrame(products)
    
    # 2. Generate 1 Year of Hyper-Realistic Transactions
    sales = []
    start_date = pd.to_datetime('2024-01-01')
    for day in range(365):
        date = start_date + timedelta(days=day)
        seasonality = 1 + 0.3 * np.sin((day / 365) * 2 * np.pi - (np.pi / 2))
        
        for _, p in df_prod.iterrows():
            base_price = p['Base_Cost'] * np.random.uniform(1.4, 2.2)
            actual_price = round(base_price * np.random.normal(1.0, 0.05), 2)
            
            # Volume calculation driven by elasticity and noise
            base_vol = np.random.randint(10, 100)
            price_ratio = actual_price / p['Base_Cost']
            elastic_vol = base_vol * (price_ratio ** p['True_PED'])
            final_vol = int(max(1, elastic_vol * seasonality * np.random.normal(1.0, 0.15)))
            
            sales.append({'Date': date, 'Product_ID': p['Product_ID'], 'Actual_Price': actual_price, 'Units_Sold': final_vol})
            
    df_sales = pd.DataFrame(sales)
    df_main = pd.merge(df_sales, df_prod, on='Product_ID')
    df_main['Gross_Profit'] = (df_main['Actual_Price'] - df_main['Base_Cost']) * df_main['Units_Sold']
    
    # 3. Statistical Modeling: Calculate PED via Log-Log Regression
    ped_results = []
    for cat in categories:
        cat_data = df_main[df_main['Category'] == cat].copy()
        cat_data['Log_Q'] = np.log(cat_data['Units_Sold'])
        cat_data['Log_P'] = np.log(cat_data['Actual_Price'])
        
        X = sm.add_constant(cat_data['Log_P'])
        y = cat_data['Log_Q']
        model = sm.OLS(y, X).fit()
        ped_results.append({'Category': cat, 'Calculated_PED': round(model.params['Log_P'], 2)})
        
    df_ped = pd.DataFrame(ped_results)
    return df_main, df_ped

# Load data
df, df_ped = load_and_model_data()

# --- SIDEBAR CONTROLS ---
st.sidebar.header("Simulation Parameters")
st.sidebar.markdown("Adjust the slider to simulate a global price change.")
price_adj_pct = st.sidebar.slider("Global Price Adjustment", min_value=-20, max_value=20, value=0, step=1)
price_adj = price_adj_pct / 100.0

# --- SIMULATION ENGINE ---
# Merge elasticity into main dataframe for row-by-row simulation
df_sim = pd.merge(df, df_ped, on='Category')

# DAX-equivalent Python logic
df_sim['Simulated_Price'] = df_sim['Actual_Price'] * (1 + price_adj)
df_sim['Simulated_Volume'] = df_sim['Units_Sold'] * (1 + (price_adj * df_sim['Calculated_PED']))
df_sim['Simulated_Profit'] = (df_sim['Simulated_Price'] - df_sim['Base_Cost']) * df_sim['Simulated_Volume']

baseline_profit = df['Gross_Profit'].sum()
projected_profit = df_sim['Simulated_Profit'].sum()
profit_variance = projected_profit - baseline_profit

# --- DASHBOARD UI ---
st.subheader("Executive Summary")
col1, col2, col3 = st.columns(3)

col1.metric("Baseline Gross Profit", f"${baseline_profit:,.0f}")
col2.metric("Projected Gross Profit", f"${projected_profit:,.0f}", delta=f"${profit_variance:,.0f}")
col3.metric("Simulated Price Change", f"{price_adj_pct}%")

st.divider()

# Charts & Data
col_chart, col_data = st.columns([2, 1])

with col_chart:
    st.subheader("Profitability by Category")
    # Grouping for the bar chart
    cat_profit = df_sim.groupby('Category')[['Gross_Profit', 'Simulated_Profit']].sum().reset_index()
    st.bar_chart(cat_profit.set_index('Category'))

with col_data:
    st.subheader("Category Elasticity (PED)")
    st.dataframe(df_ped.style.format({'Calculated_PED': '{:.2f}'}), use_container_width=True)
    st.caption("Values < -1 are highly elastic (sensitive to price).")
