import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

st.set_page_config(layout="wide")

# ---------------- DARK TRADING THEME ---------------- #
st.markdown("""
<style>
.stApp {
    background-color: #0B0F19;
    color: white;
}
section[data-testid="stSidebar"] {
    background-color: #111827;
}
.metric-box {
    background-color: #1E293B;
    padding: 15px;
    border-radius: 12px;
    text-align: center;
}
.signal-buy {color:#00FF9D; font-weight:bold;}
.signal-sell {color:#FF4B4B; font-weight:bold;}
.signal-neutral {color:#FFD700; font-weight:bold;}
</style>
""", unsafe_allow_html=True)

st.title("📈 Stock Trading Dashboard Pro")

# ---------------- SYMBOL INPUT ---------------- #
symbol = st.sidebar.text_input("Enter Stock Symbol", "RELIANCE.NS")

# ---------------- RSI FUNCTION ---------------- #
def calculate_rsi(data, period=14):
    delta = data.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

if symbol:

    ticker = yf.Ticker(symbol)
    df = ticker.history(period="1y")

    if not df.empty:

        df["MA50"] = df["Close"].rolling(50).mean()
        df["MA200"] = df["Close"].rolling(200).mean()
        df["RSI"] = calculate_rsi(df["Close"])

        latest = df.iloc[-1]
        prev = df.iloc[-2]

        price = round(latest["Close"], 2)
        change = round(price - prev["Close"], 2)
        change_pct = round((change / prev["Close"]) * 100, 2)
        rsi = round(latest["RSI"], 2)

        week52_high = round(df["High"].max(), 2)
        week52_low = round(df["Low"].min(), 2)

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
        col1, col2, col3, col4, col5 = st.columns(5)

        col1.metric("Price", f"₹ {price}", f"{change} ({change_pct}%)")
        col2.metric("RSI", rsi)
        col3.metric("52W High", week52_high)
        col4.metric("52W Low", week52_low)
        col5.markdown(f"<div class='{signal_class}'>Signal: {signal}</div>", unsafe_allow_html=True)

        st.divider()

        # ---------------- PRICE CHART ---------------- #
        st.subheader("📊 Price Chart (Close, MA50, MA200)")
        st.line_chart(df[["Close", "MA50", "MA200"]])

        st.divider()

        # ---------------- RSI CHART ---------------- #
        st.subheader("📉 RSI Indicator")
        st.line_chart(df["RSI"])

        st.divider()

        # ---------------- VOLUME CHART ---------------- #
        st.subheader("📊 Volume")
        st.bar_chart(df["Volume"])

        st.divider()

        # ---------------- FUNDAMENTALS ---------------- #
        st.subheader("📑 Fundamental Snapshot")

        info = ticker.info

        pe = info.get("trailingPE", "N/A")
        pb = info.get("priceToBook", "N/A")
        roe = info.get("returnOnEquity", "N/A")
        eps = info.get("trailingEps", "N/A")
        market_cap = info.get("marketCap", 0)

        if roe != "N/A":
            roe = round(roe * 100, 2)

        if market_cap:
            market_cap = round(market_cap / 10000000, 2)

        f1, f2, f3, f4, f5 = st.columns(5)

        f1.metric("P/E", pe)
        f2.metric("P/B", pb)
        f3.metric("ROE %", roe)
        f4.metric("EPS", eps)
        f5.metric("Market Cap (Cr)", market_cap)

    else:
        st.error("No data found for this symbol.")
