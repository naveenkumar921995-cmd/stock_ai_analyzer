import streamlit as st
from utils.theme import apply_dark_theme
from modules.data_fetcher import get_stock_data
from modules.fundamentals import show_company_snapshot
from modules.technical import show_technical_analysis
from modules.valuation import show_dcf
from modules.screener import show_screener
from modules.charts import show_price_chart
from modules.report_generator import generate_pdf

st.set_page_config(layout="wide", page_title="360° Stock Analyzer Pro")

apply_dark_theme()

st.title("📊 360° Professional Stock Analyzer")

symbol = st.text_input("Enter NSE Symbol", "RELIANCE.NS")

ticker, info, history, financials, cashflow = get_stock_data(symbol)

if history is None or history.empty:
    st.error("Invalid Symbol or Rate Limit Hit")
    st.stop()

tabs = st.tabs([
    "Overview",
    "Technical",
    "Valuation",
    "Screener",
    "Charts",
    "Report"
])

with tabs[0]:
    show_company_snapshot(info, history)

with tabs[1]:
    show_technical_analysis(history)

with tabs[2]:
    show_dcf(cashflow, info)

with tabs[3]:
    show_screener(info)

with tabs[4]:
    show_price_chart(history)

with tabs[5]:
    if st.button("Generate PDF Report"):
        generate_pdf(symbol)
