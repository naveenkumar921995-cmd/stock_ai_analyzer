import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

st.set_page_config(page_title="Stock Screener Pro", layout="wide")

# ---------------- PREMIUM DARK THEME ---------------- #
st.markdown("""
<style>
body {
    background-color: #0E1117;
}
.stApp {
    background-color: #0E1117;
    color: white;
}
section[data-testid="stSidebar"] {
    background-color: #111827;
}
.metric-card {
    background-color: #1F2937;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
}
.score-high {
    color: #00FF9D;
    font-weight: bold;
}
.score-mid {
    color: #FFD700;
    font-weight: bold;
}
.score-low {
    color: #FF4B4B;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ---------------- #
st.title("📊 Stock Screener Pro")
st.caption("Premium Fundamental + Technical Stock Analyzer")

# ---------------- STOCK LIST ---------------- #
STOCK_LIST = [
    "RELIANCE.NS", "TCS.NS", "INFY.NS",
    "HDFCBANK.NS", "ICICIBANK.NS",
    "AAPL", "MSFT", "GOOGL"
]

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

# ---------------- SIDEBAR ---------------- #
st.sidebar.markdown("## 🔎 Screener Filters")

pe_max = st.sidebar.slider("Max P/E", 5, 100, 30)
roe_min = st.sidebar.slider("Min ROE (%)", 0, 50, 10)
rsi_max = st.sidebar.slider("Max RSI", 10, 90, 60)
market_cap_min = st.sidebar.number_input("Min Market Cap (Cr)", value=10000)

run_screen = st.sidebar.button("🚀 Run Premium Scan")

# ---------------- SCREENER ---------------- #
if run_screen:

    st.markdown("### 🔍 Screening Results")

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

            if market_cap:
                market_cap_cr = market_cap / 10000000
            else:
                market_cap_cr = 0

            if pe and pe <= pe_max and \
               roe and roe >= roe_min and \
               rsi <= rsi_max and \
               market_cap_cr >= market_cap_min:

                score = 0
                if pe < 20: score += 25
                if roe > 15: score += 25
                if rsi < 40: score += 25
                if market_cap_cr > 50000: score += 25

                results.append({
                    "Symbol": symbol,
                    "Price": price,
                    "PE": round(pe,2),
                    "ROE %": round(roe,2),
                    "RSI": rsi,
                    "Market Cap (Cr)": round(market_cap_cr,2),
                    "Score": score
                })

        except:
            continue

    if results:
        df = pd.DataFrame(results).sort_values(by="Score", ascending=False)

        # Score Color
        def score_color(val):
            if val >= 75:
                return "color: #00FF9D"
            elif val >= 50:
                return "color: #FFD700"
            else:
                return "color: #FF4B4B"

        st.dataframe(
            df.style.applymap(score_color, subset=["Score"]),
            use_container_width=True
        )

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇ Download Results",
            csv,
            "premium_screen_results.csv",
            "text/csv"
        )

    else:
        st.warning("No stocks matched your premium criteria.")
