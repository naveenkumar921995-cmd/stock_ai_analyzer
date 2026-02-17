import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

st.set_page_config(page_title="Stock Screener Pro", layout="wide")

st.title("📊 Stock Screener Pro")

# -----------------------------
# STOCK LIST (Editable)
# -----------------------------
STOCK_LIST = [
    "RELIANCE.NS", "TCS.NS", "INFY.NS",
    "HDFCBANK.NS", "ICICIBANK.NS",
    "AAPL", "MSFT", "GOOGL"
]

# -----------------------------
# RSI FUNCTION
# -----------------------------
def calculate_rsi(data, period=14):
    delta = data.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------
st.sidebar.header("🔍 Screener Filters")

pe_max = st.sidebar.number_input("Max P/E", value=30)
roe_min = st.sidebar.number_input("Min ROE (%)", value=10)
rsi_max = st.sidebar.number_input("Max RSI", value=60)
market_cap_min = st.sidebar.number_input("Min Market Cap (Cr)", value=10000)

run_screen = st.sidebar.button("Run Screen")

# -----------------------------
# SCREENER LOGIC
# -----------------------------
if run_screen:

    results = []

    for symbol in STOCK_LIST:
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info

            hist = ticker.history(period="6mo")

            if hist.empty:
                continue

            hist["RSI"] = calculate_rsi(hist["Close"])
            rsi = round(float(hist["RSI"].iloc[-1]), 2)

            price = round(float(hist["Close"].iloc[-1]), 2)

            pe = info.get("trailingPE", None)
            roe = info.get("returnOnEquity", None)
            market_cap = info.get("marketCap", None)

            if roe:
                roe = roe * 100

            # Convert Market Cap to Crores
            if market_cap:
                market_cap_cr = market_cap / 10000000
            else:
                market_cap_cr = 0

            # Apply Filters
            if pe and pe <= pe_max and \
               roe and roe >= roe_min and \
               rsi <= rsi_max and \
               market_cap_cr >= market_cap_min:

                # Score Calculation
                score = 0

                if pe < 20:
                    score += 25
                if roe > 15:
                    score += 25
                if rsi < 40:
                    score += 25
                if market_cap_cr > 50000:
                    score += 25

                results.append({
                    "Symbol": symbol,
                    "Price": price,
                    "PE": round(pe, 2) if pe else None,
                    "ROE %": round(roe, 2) if roe else None,
                    "RSI": rsi,
                    "Market Cap (Cr)": round(market_cap_cr, 2),
                    "Score": score
                })

        except:
            continue

    if results:
        df = pd.DataFrame(results).sort_values(by="Score", ascending=False)

        st.success(f"{len(df)} Stocks Found")

        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            "Download CSV",
            csv,
            "screened_stocks.csv",
            "text/csv"
        )

    else:
        st.warning("No stocks matched the criteria.")
