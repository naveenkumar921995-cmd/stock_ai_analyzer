import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

st.set_page_config(layout="wide", page_title="Stock Analyzer Pro")

st.title("📊 Smart Stock Analyzer")

stock = st.text_input("Enter NSE Symbol", "RELIANCE.NS")

ticker = yf.Ticker(stock)
info = ticker.info
data = ticker.history(period="1y")

if data.empty:
    st.error("Invalid Symbol")
    st.stop()

# ===============================
# BASIC INFO
# ===============================
st.header("Company Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Market Cap", info.get("marketCap"))
col2.metric("PE Ratio", info.get("trailingPE"))
col3.metric("PB Ratio", info.get("priceToBook"))
col4.metric("Dividend Yield", info.get("dividendYield"))

# ===============================
# 52 WEEK DATA
# ===============================
st.subheader("52 Week Range")

high_52 = data['High'].max()
low_52 = data['Low'].min()

col5, col6 = st.columns(2)
col5.metric("52W High", round(high_52,2))
col6.metric("52W Low", round(low_52,2))

# ===============================
# TECHNICAL ANALYSIS
# ===============================
st.header("Technical Health")

data['EMA20'] = data['Close'].ewm(span=20).mean()
data['EMA50'] = data['Close'].ewm(span=50).mean()

# RSI
delta = data['Close'].diff()
gain = delta.where(delta > 0, 0).rolling(14).mean()
loss = -delta.where(delta < 0, 0).rolling(14).mean()
rs = gain / loss
data['RSI'] = 100 - (100/(1+rs))

latest = data.iloc[-1]

trend = "Sideways"

if latest['EMA20'] > latest['EMA50']:
    trend = "Bullish"
elif latest['EMA20'] < latest['EMA50']:
    trend = "Bearish"

rsi_status = "Neutral"
if latest['RSI'] > 70:
    rsi_status = "Overbought"
elif latest['RSI'] < 30:
    rsi_status = "Oversold"

col7, col8, col9 = st.columns(3)

col7.metric("Trend", trend)
col8.metric("RSI", round(latest['RSI'],2))
col9.metric("RSI Status", rsi_status)

# ===============================
# AI SUMMARY
# ===============================
st.header("AI Stock Summary")

summary = f"""
• Trend: {trend}
• RSI Condition: {rsi_status}
• Current Price: {round(latest['Close'],2)}
• 52W High: {round(high_52,2)}
• 52W Low: {round(low_52,2)}

Overall Technical View: {trend} momentum with {rsi_status} RSI.
"""

st.info(summary)
