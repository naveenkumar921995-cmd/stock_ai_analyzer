import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="360° Stock Analyzer", layout="wide")

st.title("📊 360° Equity Analysis Engine")
st.markdown("Fundamental + Technical + Risk + AI Scoring Model")

# ---------------------------------------------------------
# Utility Functions
# ---------------------------------------------------------

def calculate_cagr(series):
    try:
        series = series.dropna()
        if len(series) < 2:
            return None
        start_value = series.iloc[-1]
        end_value = series.iloc[0]
        years = len(series) - 1
        cagr = ((start_value / end_value) ** (1 / years) - 1) * 100
        return round(cagr, 2)
    except:
        return None


def calculate_sharpe_ratio(returns, risk_free_rate=0.06):
    excess_returns = returns - risk_free_rate/252
    sharpe = np.sqrt(252) * excess_returns.mean() / excess_returns.std()
    return round(sharpe, 2)


def calculate_volatility(returns):
    return round(returns.std() * np.sqrt(252) * 100, 2)


def calculate_rsi(data, window=14):
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))


# ---------------------------------------------------------
# Scoring Model
# ---------------------------------------------------------

def ai_scoring_model(revenue_cagr, profit_cagr, sharpe, volatility, rsi):
    
    fundamental_score = 0
    technical_score = 0
    risk_score = 0

    # Fundamental
    if revenue_cagr and revenue_cagr > 10:
        fundamental_score += 50
    if profit_cagr and profit_cagr > 10:
        fundamental_score += 50

    # Technical
    if rsi is not None:
        if 40 < rsi < 70:
            technical_score += 100
        elif 30 < rsi < 80:
            technical_score += 70
        else:
            technical_score += 40

    # Risk
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
        grade = "A (Strong Investment)"
    elif total_score > 60:
        grade = "B (Moderate)"
    elif total_score > 45:
        grade = "C (Average)"
    else:
        grade = "D (High Risk)"

    return round(total_score, 2), grade


# ---------------------------------------------------------
# Sidebar Input
# ---------------------------------------------------------

symbol = st.sidebar.text_input("Enter Stock Symbol (e.g., RELIANCE.NS, AAPL)", "RELIANCE.NS")

if symbol:

    ticker = yf.Ticker(symbol)

    try:
        info = ticker.info
        history = ticker.history(period="5y")
        financials = ticker.financials

        st.subheader(f"{info.get('longName', symbol)}")

        col1, col2, col3 = st.columns(3)

        col1.metric("Market Cap", info.get("marketCap"))
        col2.metric("PE Ratio", info.get("trailingPE"))
        col3.metric("Sector", info.get("sector"))

        # -------------------------------------------------
        # Technical Analysis
        # -------------------------------------------------

        history['Returns'] = history['Close'].pct_change()
        history['RSI'] = calculate_rsi(history['Close'])
        history['EMA20'] = history['Close'].ewm(span=20).mean()
        history['EMA50'] = history['Close'].ewm(span=50).mean()
        history['Upper'] = history['Close'].rolling(20).mean() + 2 * history['Close'].rolling(20).std()
        history['Lower'] = history['Close'].rolling(20).mean() - 2 * history['Close'].rolling(20).std()

        sharpe_ratio = calculate_sharpe_ratio(history['Returns'].dropna())
        volatility = calculate_volatility(history['Returns'].dropna())
        latest_rsi = history['RSI'].iloc[-1]

        # -------------------------------------------------
        # Fundamental CAGR
        # -------------------------------------------------

        revenue_cagr = None
        profit_cagr = None

        if not financials.empty:
            if "Total Revenue" in financials.index:
                revenue_cagr = calculate_cagr(financials.loc["Total Revenue"])
            if "Net Income" in financials.index:
                profit_cagr = calculate_cagr(financials.loc["Net Income"])

        # -------------------------------------------------
        # AI Scoring
        # -------------------------------------------------

        score, grade = ai_scoring_model(
            revenue_cagr,
            profit_cagr,
            sharpe_ratio,
            volatility,
            latest_rsi
        )

        # -------------------------------------------------
        # Display Risk Metrics
        # -------------------------------------------------

        st.subheader("📉 Risk Metrics")
        col1, col2, col3 = st.columns(3)
        col1.metric("Sharpe Ratio", sharpe_ratio)
        col2.metric("Volatility (%)", volatility)
        col3.metric("Latest RSI", round(latest_rsi, 2))

        # -------------------------------------------------
        # Display CAGR
        # -------------------------------------------------

        st.subheader("📈 5-Year Growth")
        col1, col2 = st.columns(2)
        col1.metric("Revenue CAGR (%)", revenue_cagr)
        col2.metric("Profit CAGR (%)", profit_cagr)

        # -------------------------------------------------
        # AI Grade
        # -------------------------------------------------

        st.subheader("🤖 AI Investment Score")
        st.metric("Overall Score", score)
        st.success(f"Investment Grade: {grade}")

        # -------------------------------------------------
        # Chart
        # -------------------------------------------------

        fig = go.Figure()

        fig.add_trace(go.Candlestick(
            x=history.index,
            open=history['Open'],
            high=history['High'],
            low=history['Low'],
            close=history['Close'],
            name="Candlestick"
        ))

        fig.add_trace(go.Scatter(x=history.index, y=history['EMA20'], name="EMA 20"))
        fig.add_trace(go.Scatter(x=history.index, y=history['EMA50'], name="EMA 50"))
        fig.add_trace(go.Scatter(x=history.index, y=history['Upper'], name="Upper Band"))
        fig.add_trace(go.Scatter(x=history.index, y=history['Lower'], name="Lower Band"))

        fig.update_layout(height=700)
        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error("Error fetching stock data. Please check symbol.")
