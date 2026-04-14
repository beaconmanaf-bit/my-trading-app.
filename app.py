import streamlit as st
import pandas as pd
import plotly.express as px
import yfinance as yf

# Page Config
st.set_page_config(page_title="AI Trading Analyzer", layout="wide")

# 1. Load your uploaded data
@st.cache_data
def load_data():
    df = pd.read_csv('data.csv')
    # Column mapping based on your file structure
    cols = ['ID', 'Stock_Name', 'Price', 'PE', 'MarketCap', 'DivYield', 
            'NP_Qtr', 'Profit_Var', 'ROCE', 'ROE', 'Sales_Var', 'D_E', 'P_B', 'Reserves']
    df.columns = cols
    return df

df = load_data()

st.sidebar.title("Trading Controls")
st.title("📈 AI Stock Analysis Dashboard")

# 2. Key Metrics Overview
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Stocks Analyzed", len(df))
with col2:
    st.metric("Avg ROCE", f"{df['ROCE'].mean():.2f}%")
with col3:
    st.metric("Top Performer", df.iloc[df['ROCE'].idxmax()]['Stock_Name'])

# 3. Stock Selection & Live Charting
st.subheader("Live Technical Analysis")
selected_stock = st.selectbox("Select a Stock from your List:", df['Stock_Name'].unique())

# Simple mapping logic (In a real app, you'd need a Ticker lookup table)
ticker_input = st.text_input("Enter Yahoo Finance Ticker (e.g., RELIANCE.NS, TCS.NS):", "RELIANCE.NS")

if st.button("Fetch Live Data"):
    stock_data = yf.download(ticker_input, period="6mo", interval="1d")
    if not stock_data.empty:
        fig = px.line(stock_data, y='Close', title=f"Price Action for {selected_stock}")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("Ticker not found. Please use '.NS' for Indian stocks.")

# 4. Fundamental Screener (Using your CSV data)
st.subheader("Fundamental Rankings")
min_roce = st.slider("Minimum ROCE (%)", 0, 100, 20)
filtered_df = df[df['ROCE'] >= min_roce].sort_values(by='ROCE', ascending=False)

st.dataframe(filtered_df[['Stock_Name', 'ROCE', 'ROE', 'Price', 'D_E']], use_container_width=True)

# 5. Automated "Buy/Sell" Signal Logic (Demo)
st.subheader("🤖 AI Strategy Signal")
if not filtered_df.empty:
    top_pick = filtered_df.iloc[0]
    st.success(f"**STRATEGY ALERT:** {top_pick['Stock_Name']} has an ROCE of {top_pick['ROCE']}%. "
               "If RSI is < 30 on the live chart, consider a BUY entry.")
