import streamlit as st

def show_company_snapshot(info, history):
    st.header("Company Snapshot")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Market Cap", info.get("marketCap"))
    col2.metric("PE Ratio", info.get("trailingPE"))
    col3.metric("PB Ratio", info.get("priceToBook"))
    col4.metric("Dividend Yield", info.get("dividendYield"))

    high_52 = history['High'].rolling(252).max().iloc[-1]
    low_52 = history['Low'].rolling(252).min().iloc[-1]

    col5, col6 = st.columns(2)
    col5.metric("52W High", round(high_52,2))
    col6.metric("52W Low", round(low_52,2))

