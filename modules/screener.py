import streamlit as st

def show_screener(info):

    st.header("Screener Filter")

    min_roe = st.slider("Minimum ROE %", 0, 30, 15)
    max_pe = st.slider("Maximum PE", 5, 50, 25)

    roe = info.get("returnOnEquity",0) * 100
    pe = info.get("trailingPE",0)

    if roe > min_roe and pe < max_pe:
        st.success("Stock Passes Screener")
    else:
        st.warning("Stock Does Not Pass Screener")

