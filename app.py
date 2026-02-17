import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

st.set_page_config(layout="wide", page_title="360° Stock Analyzer")

st.title("📊 360° Professional Stock Analyzer")

stock = st.text_input("Enter NSE Stock Symbol", "RELIANCE.NS")

ticker = yf.Ticker(stock)
info = ticker.info
data = ticker.history(period="2y")

if data.empty:
    st.error("Invalid Stock Symbol")
    st.stop()

# ===============================
# COMPANY SNAPSHOT
# ===============================
st.header("Company Snapshot")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Market Cap", info.get("marketCap"))
col2.metric("PE Ratio", round(info.get("trailingPE",0),2))
col3.metric("PB Ratio", round(info.get("priceToBook",0),2))
col4.metric("Dividend Yield", info.get("dividendYield"))

# 52W
high_52 = data['High'].rolling(252).max().iloc[-1]
low_52 = data['Low'].rolling(252).min().iloc[-1]

col5, col6 = st.columns(2)
col5.metric("52W High", round(high_52,2))
col6.metric("52W Low", round(low_52,2))

# ===============================
# FINANCIAL STRENGTH
# ===============================
st.header("Financial Strength")

roe = info.get("returnOnEquity")
debt_equity = info.get("debtToEquity")
eps = info.get("trailingEps")

col7, col8, col9 = st.columns(3)

col7.metric("ROE", roe)
col8.metric("Debt/Equity", debt_equity)
col9.metric("EPS", eps)

# ===============================
# TECHNICAL ANALYSIS
# ===============================
st.header("Technical Health")

data['EMA20'] = data['Close'].ewm(span=20).mean()
data['EMA50'] = data['Close'].ewm(span=50).mean()

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

volatility = data['Close'].pct_change().std() * np.sqrt(252) * 100

col10, col11, col12 = st.columns(3)
col10.metric("Trend", trend)
col11.metric("RSI", round(latest['RSI'],2))
col12.metric("Volatility %", round(volatility,2))

# ===============================
# RISK ANALYSIS
# ===============================
st.header("Risk Meter")

beta = info.get("beta")
drawdown = (data['Close'] / data['Close'].cummax() - 1).min() * 100

col13, col14 = st.columns(2)
col13.metric("Beta", beta)
col14.metric("Max Drawdown %", round(drawdown,2))

# ===============================
# AI RATING SYSTEM
# ===============================
st.header("AI Overall Score")

score = 0

# Fundamental Score
if roe and roe > 0.15:
    score += 20
if debt_equity and debt_equity < 100:
    score += 20

# Technical Score
if trend == "Bullish":
    score += 20
if rsi_status == "Neutral":
    score += 20

# Risk Score
if volatility < 30:
    score += 20

st.success(f"Overall Stock Score: {score} / 100")

# ===============================
# AI SUMMARY
# ===============================
st.header("AI Summary")

summary = f"""
Trend: {trend}
RSI Status: {rsi_status}
Volatility: {round(volatility,2)}%
ROE: {roe}
Debt/Equity: {debt_equity}

Overall Rating: {score}/100
"""

st.info(summary)
