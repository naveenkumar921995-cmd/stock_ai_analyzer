import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(layout="wide")

# ---------------- DARK THEME ---------------- #
st.markdown("""
<style>
.stApp {
    background-color: #0B0F19;
    color: white;
}
section[data-testid="stSidebar"] {
    background-color: #111827;
}
.signal-buy {color:#00FF9D; font-weight:bold; font-size:18px;}
.signal-sell {color:#FF4B4B; font-weight:bold; font-size:18px;}
.signal-neutral {color:#FFD700; font-weight:bold; font-size:18px;}
</style>
""", unsafe_allow_html=True)

st.title("📈 Trading Dashboard Pro")

# ---------------- SIDEBAR ---------------- #
symbol = st.sidebar.text_input("Stock Symbol", "RELIANCE.NS")

timeframe = st.sidebar.selectbox(
    "Select Timeframe",
    ["1mo", "3mo", "6mo", "1y", "5y"],
    index=3
)

# ---------------- RSI ---------------- #
def calculate_rsi(data, period=14):
    delta = data.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# ---------------- MACD ---------------- #
def calculate_macd(data):
    exp1 = data.ewm(span=12, adjust=False).mean()
    exp2 = data.ewm(span=26, adjust=False).mean()
    macd = exp1 - exp2
    signal = macd.ewm(span=9, adjust=False).mean()
    return macd, signal

# ---------------- DATA LOAD ---------------- #
if symbol:

    ticker = yf.Ticker(symbol)
    df = ticker.history(period=timeframe)

    if not df.empty:

        df["RSI"] = calculate_rsi(df["Close"])
        df["MACD"], df["MACD_Signal"] = calculate_macd(df["Close"])

        latest = df.iloc[-1]
        prev = df.iloc[-2]

        price = round(latest["Close"], 2)
        change = round(price - prev["Close"], 2)
        change_pct = round((change / prev["Close"]) * 100, 2)
        rsi = round(latest["RSI"], 2)

        # Signal Logic
        if rsi < 30:
            signal = "Strong Buy"
            signal_class = "signal-buy"
        elif rsi > 70:
            signal = "Strong Sell"
            signal_class = "signal-sell"
        else:
            signal = "Neutral"
            signal_class = "signal-neutral"

        # ---------------- TOP METRICS ---------------- #
        col1, col2, col3 = st.columns(3)
        col1.metric("Price", f"₹ {price}", f"{change} ({change_pct}%)")
        col2.metric("RSI", rsi)
        col3.markdown(f"<div class='{signal_class}'>Signal: {signal}</div>", unsafe_allow_html=True)

        st.divider()

        # ---------------- CANDLESTICK ---------------- #
        st.subheader("🕯 Candlestick Chart")

        fig = go.Figure()

        fig.add_trace(go.Candlestick(
            x=df.index,
            open=df["Open"],
            high=df["High"],
            low=df["Low"],
            close=df["Close"],
            name="Price"
        ))

        fig.update_layout(
            template="plotly_dark",
            xaxis_rangeslider_visible=False,
            height=500
        )

        st.plotly_chart(fig, use_container_width=True)

        st.divider()

        # ---------------- MACD ---------------- #
        st.subheader("📊 MACD Indicator")

        macd_fig = go.Figure()
        macd_fig.add_trace(go.Scatter(
            x=df.index, y=df["MACD"],
            mode="lines", name="MACD"
        ))
        macd_fig.add_trace(go.Scatter(
            x=df.index, y=df["MACD_Signal"],
            mode="lines", name="Signal Line"
        ))

        macd_fig.update_layout(
            template="plotly_dark",
            height=400
        )

        st.plotly_chart(macd_fig, use_container_width=True)

        st.divider()

        # ---------------- RSI ---------------- #
        st.subheader("📉 RSI")

        rsi_fig = go.Figure()
        rsi_fig.add_trace(go.Scatter(
            x=df.index, y=df["RSI"],
            mode="lines", name="RSI"
        ))
        rsi_fig.add_hline(y=70)
        rsi_fig.add_hline(y=30)

        rsi_fig.update_layout(
            template="plotly_dark",
            height=400
        )

        st.plotly_chart(rsi_fig, use_container_width=True)

        st.divider()

        # ---------------- VOLUME ---------------- #
        st.subheader("📊 Volume")

        volume_fig = go.Figure()
        volume_fig.add_trace(go.Bar(
            x=df.index, y=df["Volume"],
            name="Volume"
        ))

        volume_fig.update_layout(
            template="plotly_dark",
            height=300
        )

        st.plotly_chart(volume_fig, use_container_width=True)

    else:
        st.error("No data found.")
