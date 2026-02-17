import streamlit as st

def show_company_snapshot(info, history):

    st.header("Company Snapshot")

    if info is None or history is None:
        st.warning("Data not available")
        return

    # Create columns FIRST
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Last Price", info.get("lastPrice"))
    col2.metric("Day High", info.get("dayHigh"))
    col3.metric("Day Low", info.get("dayLow"))
    col4.metric("Previous Close", info.get("previousClose"))

    # 52 Week Range
    if not history.empty:
        high_52 = history['High'].rolling(252).max().iloc[-1]
        low_52 = history['Low'].rolling(252).min().iloc[-1]

        col5, col6 = st.columns(2)
        col5.metric("52W High", round(high_52,2))
        col6.metric("52W Low", round(low_52,2))


