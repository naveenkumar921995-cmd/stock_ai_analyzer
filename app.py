import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import scipy.stats as stats
import time

st.set_page_config(page_title="360° Stock EDA Engine", layout="wide")

st.title("📊 360° Financial Exploratory Data Analysis Engine")
st.markdown("Technical + Fundamental + Risk + Statistical EDA + AI Scoring")

# -------------------------------------------------
# SAFE DATA FETCH WITH CACHING
# -------------------------------------------------

@st.cache_data(ttl=600)
def fetch_stock_data(symbol):
    try:
        ticker = yf.Ticker(symbol)
        history = ticker.history(period="5y")
        financials = ticker.financials
        return history, financials
    except Exception:
        return None, None


# -------------------------------------------------
# Utility Functions
# -------------------------------------------------

def calculate_cagr(series):
    try:
        series = series.dropna()
        if len(series) < 2:
            return None
        start_value = series.iloc[-1]
        end_value = series.iloc[0]
        years = len(series) - 1
        return round(((start_value / end_value) ** (1 / years) - 1) * 100, 2)
    except:
        return None


def calculate_sharpe_ratio(returns):
    try:
        return round(np.sqrt(252) * returns.mean() / returns.std(), 2)
    except:
        return None


def calculate_volatility(returns):
    try:
        return round(returns.std() * np.sqrt(252) * 100, 2)
    except:
        return None


def calculate_rsi(data, window=14):
    delta = data.diff()
    gain = delta.clip(lower=0).rolling(window).mean()
    loss = -delta.clip(upper=0).rolling(window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))


def ai_scoring_model(revenue_cagr, profit_cagr, sharpe, volatility, rsi):
    fundamental_score = 0
    technical_score = 0
    risk_score = 0

    if revenue_cagr and revenue_cagr > 10:
        fundamental_score += 50
    if profit_cagr and profit_cagr > 10:
        fundamental_score += 50

    if rsi:
        if 40 < rsi < 70:
            technical_score = 100
        elif 30 < rsi < 80:
            technical_score = 70
        else:
            technical_score = 40

    if sharpe and sharpe > 1:
        risk_score += 70
    if volatility and volatility < 25:
        risk_score += 30

    total_score = (
        fundamental_score * 0.4 +
        technical_score * 0.3 +
        risk_score * 0.3
    )

    if total_score > 75:
        grade = "A (Strong)"
    elif total_score > 60:
        grade = "B (Moderate)"
    elif total_score > 45:
        grade = "C (Average)"
    else:
        grade = "D (High Risk)"

    return round(total_score, 2), grade


# -------------------------------------------------
# Sidebar
# -------------------------------------------------

symbol = st.sidebar.text_input(
    "Enter Stock Symbol (Example: RELIANCE.NS or AAPL)",
    "RELIANCE.NS"
)

if symbol:

    with st.spinner("Fetching data safely..."):
        history, financials = fetch_stock_data(symbol)
        time.sleep(1)

    if history is None or history.empty:
        st.error("⚠ Data not available or Yahoo rate limit exceeded.")
        st.stop()

    st.subheader(f"Stock Selected: {symbol}")

    # -------------------------------------------------
    # EDA SECTION
    # -------------------------------------------------

    st.header("📊 Exploratory Data Analysis")

    st.subheader("📋 Data Overview")
    col1, col2 = st.columns(2)
    col1.write(f"Dataset Shape: {history.shape}")
    col2.write("Date Range:",
               f"{history.index.min().date()} to {history.index.max().date()}")

    st.write("Summary Statistics")
    st.dataframe(history.describe())

    st.write("Missing Values")
    st.dataframe(history.isnull().sum())

    # -------------------------------------------------
    # Feature Engineering
    # -------------------------------------------------

    history["Returns"] = history["Close"].pct_change()
    history["RSI"] = calculate_rsi(history["Close"])
    history["EMA20"] = history["Close"].ewm(span=20).mean()
    history["EMA50"] = history["Close"].ewm(span=50).mean()

    returns = history["Returns"].dropna()

    # -------------------------------------------------
    # Distribution Analysis
    # -------------------------------------------------

    st.subheader("📊 Return Distribution")

    fig_hist = go.Figure()
    fig_hist.add_trace(go.Histogram(x=returns, nbinsx=60))
    st.plotly_chart(fig_hist, use_container_width=True)

    skewness = stats.skew(returns)
    kurt = stats.kurtosis(returns)

    st.write(f"Skewness: {round(skewness,2)}")
    st.write(f"Kurtosis: {round(kurt,2)}")

    # -------------------------------------------------
    # Outlier Detection
    # -------------------------------------------------

    st.subheader("🚨 Outlier Detection")

    Q1 = returns.quantile(0.25)
    Q3 = returns.quantile(0.75)
    IQR = Q3 - Q1

    outliers = returns[
        (returns < Q1 - 1.5*IQR) |
        (returns > Q3 + 1.5*IQR)
    ]

    st.write("Extreme Return Days:", len(outliers))

    # -------------------------------------------------
    # Rolling Volatility
    # -------------------------------------------------

    history["Rolling_Volatility"] = (
        returns.rolling(30).std() * np.sqrt(252) * 100
    )

    st.subheader("📈 Rolling Volatility (30-Day)")

    fig_vol = go.Figure()
    fig_vol.add_trace(go.Scatter(
        x=history.index,
        y=history["Rolling_Volatility"],
        name="Rolling Volatility"
    ))
    st.plotly_chart(fig_vol, use_container_width=True)

    # -------------------------------------------------
    # Drawdown Analysis
    # -------------------------------------------------

    st.subheader("📉 Drawdown Analysis")

    history["Cumulative"] = (1 + returns).cumprod()
    history["Peak"] = history["Cumulative"].cummax()
    history["Drawdown"] = (
        history["Cumulative"] - history["Peak"]
    ) / history["Peak"]

    fig_dd = go.Figure()
    fig_dd.add_trace(go.Scatter(
        x=history.index,
        y=history["Drawdown"],
        name="Drawdown"
    ))
    st.plotly_chart(fig_dd, use_container_width=True)

    st.write("Maximum Drawdown:",
             round(history["Drawdown"].min()*100,2), "%")

    # -------------------------------------------------
    # Risk Metrics
    # -------------------------------------------------

    sharpe_ratio = calculate_sharpe_ratio(returns)
    volatility = calculate_volatility(returns)
    latest_rsi = history["RSI"].iloc[-1]

    st.header("📉 Risk Metrics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Sharpe Ratio", sharpe_ratio if sharpe_ratio else "N/A")
    col2.metric("Volatility (%)", volatility if volatility else "N/A")
    col3.metric("Latest RSI", round(latest_rsi, 2))

    # -------------------------------------------------
    # Fundamental Growth
    # -------------------------------------------------

    revenue_cagr = None
    profit_cagr = None

    if isinstance(financials, pd.DataFrame) and not financials.empty:
        if "Total Revenue" in financials.index:
            revenue_cagr = calculate_cagr(financials.loc["Total Revenue"])
        if "Net Income" in financials.index:
            profit_cagr = calculate_cagr(financials.loc["Net Income"])

    st.header("📈 5-Year Growth")
    col1, col2 = st.columns(2)
    col1.metric("Revenue CAGR (%)", revenue_cagr if revenue_cagr else "N/A")
    col2.metric("Profit CAGR (%)", profit_cagr if profit_cagr else "N/A")

    # -------------------------------------------------
    # AI Score
    # -------------------------------------------------

    score, grade = ai_scoring_model(
        revenue_cagr,
        profit_cagr,
        sharpe_ratio,
        volatility,
        latest_rsi
    )

    st.header("🤖 AI Investment Score")
    st.metric("Overall Score", score)
    st.success(f"Investment Grade: {grade}")

    # -------------------------------------------------
    # Insight Summary
    # -------------------------------------------------

    st.header("🧠 EDA Insight Summary")

    if volatility and volatility > 30:
        st.warning("High volatility environment detected.")

    if skewness < 0:
        st.warning("Negative skew suggests downside risk dominance.")

    if history["Drawdown"].min() < -0.3:
        st.error("Significant historical crash observed.")
