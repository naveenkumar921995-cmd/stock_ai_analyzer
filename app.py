import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time

st.set_page_config(layout="wide", page_title="AI Trading Terminal")

# ===============================
# AUTO REFRESH
# ===============================
refresh_rate = st.sidebar.selectbox("Auto Refresh (seconds)", [0, 30, 60, 120])
if refresh_rate > 0:
    time.sleep(refresh_rate)
    st.rerun()

# ===============================
# INPUT SECTION
# ===============================
st.sidebar.title("📊 Market Controls")

stock = st.sidebar.text_input("Enter Stock Symbol", "RELIANCE.NS")

timeframe = st.sidebar.selectbox(
    "Select Timeframe",
    ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y"]
)

# ===============================
# FETCH DATA
# ===============================
data = yf.download(stock, period=timeframe)

if data.empty:
    st.error("Invalid Stock Symbol")
    st.stop()

# ===============================
# INDICATORS
# ===============================

# EMA
data['EMA20'] = data['Close'].ewm(span=20).mean()
data['EMA50'] = data['Close'].ewm(span=50).mean()

# Bollinger Bands
data['MA20'] = data['Close'].rolling(window=20).mean()
data['Upper'] = data['MA20'] + 2 * data['Close'].rolling(window=20).std()
data['Lower'] = data['MA20'] - 2 * data['Close'].rolling(window=20).std()

# MACD
data['EMA12'] = data['Close'].ewm(span=12).mean()
data['EMA26'] = data['Close'].ewm(span=26).mean()
data['MACD'] = data['EMA12'] - data['EMA26']
data['Signal'] = data['MACD'].ewm(span=9).mean()

# RSI
delta = data['Close'].diff()
gain = (delta.where(delta > 0, 0)).rolling(14).mean()
loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
rs = gain / loss
data['RSI'] = 100 - (100 / (1 + rs))

# ===============================
# SIGNAL LOGIC
# ===============================
latest = data.iloc[-1]

signal = "HOLD"

if latest['EMA20'] > latest['EMA50'] and latest['RSI'] > 50:
    signal = "BUY 🚀"
elif latest['EMA20'] < latest['EMA50'] and latest['RSI'] < 50:
    signal = "SELL 🔻"

# ===============================
# DASHBOARD HEADER
# ===============================
st.title("📈 AI Trading Dashboard")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Current Price", f"₹{round(latest['Close'],2)}")
col2.metric("RSI", round(latest['RSI'],2))
col3.metric("MACD", round(latest['MACD'],2))
col4.metric("Signal", signal)

# ===============================
# CHART SECTION
# ===============================
fig = make_subplots(
    rows=3, cols=1,
    shared_xaxes=True,
    vertical_spacing=0.03,
    row_heights=[0.6, 0.2, 0.2]
)

# Candlestick
fig.add_trace(go.Candlestick(
    x=data.index,
    open=data['Open'],
    high=data['High'],
    low=data['Low'],
    close=data['Close'],
    name="Candlestick"
), row=1, col=1)

# EMA
fig.add_trace(go.Scatter(
    x=data.index,
    y=data['EMA20'],
    line=dict(color='blue'),
    name="EMA20"
), row=1, col=1)

fig.add_trace(go.Scatter(
    x=data.index,
    y=data['EMA50'],
    line=dict(color='orange'),
    name="EMA50"
), row=1, col=1)

# Bollinger Bands
fig.add_trace(go.Scatter(
    x=data.index,
    y=data['Upper'],
    line=dict(color='grey'),
    name="Upper Band"
), row=1, col=1)

fig.add_trace(go.Scatter(
    x=data.index,
    y=data['Lower'],
    line=dict(color='grey'),
    name="Lower Band"
), row=1, col=1)

# MACD
fig.add_trace(go.Scatter(
    x=data.index,
    y=data['MACD'],
    line=dict(color='green'),
    name="MACD"
), row=2, col=1)

fig.add_trace(go.Scatter(
    x=data.index,
    y=data['Signal'],
    line=dict(color='red'),
    name="Signal Line"
), row=2, col=1)

# RSI
fig.add_trace(go.Scatter(
    x=data.index,
    y=data['RSI'],
    line=dict(color='purple'),
    name="RSI"
), row=3, col=1)

fig.update_layout(height=900, xaxis_rangeslider_visible=False)

st.plotly_chart(fig, use_container_width=True)

# ===============================
# 52 WEEK DATA
# ===============================
year_data = yf.download(stock, period="1y")

st.subheader("📊 52 Week Stats")

col5, col6 = st.columns(2)
col5.metric("52 Week High", f"₹{round(year_data['High'].max(),2)}")
col6.metric("52 Week Low", f"₹{round(year_data['Low'].min(),2)}")
