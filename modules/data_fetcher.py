import yfinance as yf
import streamlit as st

@st.cache_data(ttl=600)   # Cache for 10 minutes
def get_stock_data(symbol):

    try:
        ticker = yf.Ticker(symbol)

        # Use history instead of .info (less blocking)
        history = ticker.history(period="2y")

        # Use fast_info instead of info (safer)
        fast_info = ticker.fast_info

        financials = ticker.financials.T if ticker.financials is not None else None
        cashflow = ticker.cashflow.T if ticker.cashflow is not None else None

        return ticker, fast_info, history, financials, cashflow

    except Exception as e:
        st.error("Data fetch failed. Possibly rate limited.")
        return None, None, None, None, None
