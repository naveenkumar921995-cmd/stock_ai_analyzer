import yfinance as yf
import streamlit as st
import pandas as pd

@st.cache_data(ttl=600)
def get_stock_data(symbol):

    try:
        ticker = yf.Ticker(symbol)

        history = ticker.history(period="2y")

        fast_info = ticker.fast_info

        # Convert fast_info to normal dict (important!)
        info = dict(fast_info) if fast_info else {}

        financials = ticker.financials.T if ticker.financials is not None else pd.DataFrame()
        cashflow = ticker.cashflow.T if ticker.cashflow is not None else pd.DataFrame()

        return info, history, financials, cashflow

    except Exception:
        return None, pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
