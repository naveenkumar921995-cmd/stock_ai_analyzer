import pandas as pd
import numpy as np
import streamlit as st

def show_technical_analysis(data):

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

    volatility = data['Close'].pct_change().std() * np.sqrt(252) * 100

    col1, col2, col3 = st.columns(3)
    col1.metric("Trend", trend)
    col2.metric("RSI", round(latest['RSI'],2))
    col3.metric("Volatility %", round(volatility,2))

    return trend

