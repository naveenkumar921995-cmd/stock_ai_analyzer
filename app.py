import streamlit as st
from database import init_db
from auth import register_user, login_user
from scanner import analyze_stock
from ai_engine import ai_explain
from portfolio import add_stock, get_portfolio

init_db()

st.set_page_config(page_title="AI Stock SaaS", layout="wide")
st.title("🚀 AI Stock Analyzer SaaS")

menu = ["Login","Register"]
choice = st.sidebar.selectbox("Menu", menu)

if "user" not in st.session_state:
    st.session_state.user = None

if choice == "Register":
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Register"):
        if register_user(username,password):
            st.success("Account created!")
        else:
            st.error("Username exists.")

elif choice == "Login":
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if login_user(username,password):
            st.session_state.user = username
            st.success("Logged in!")
        else:
            st.error("Invalid credentials")

if st.session_state.user:

    st.sidebar.success(f"Welcome {st.session_state.user}")
    page = st.sidebar.selectbox("Dashboard",
                                ["Stock Scanner","Portfolio"])

    if page == "Stock Scanner":
        symbol = st.text_input("Enter NSE Stock (e.g. RELIANCE.NS)")
        if st.button("Analyze"):
            result = analyze_stock(symbol)

if "Error" in result:
    st.error(result["Error"])
else:
    st.write(result)

    explanation = ai_explain(
        result["Stock"],
        result["RSI"],
        result["Signal"]
    )
    st.info(explanation)

            explanation = ai_explain(
                result["Stock"],
                result["RSI"],
                result["Signal"]
            )
            st.info(explanation)

    if page == "Portfolio":
        stock = st.text_input("Stock")
        qty = st.number_input("Quantity", min_value=1)
        price = st.number_input("Buy Price", min_value=0.0)
        if st.button("Add to Portfolio"):
            add_stock(st.session_state.user, stock, qty, price)
            st.success("Added")
        data = get_portfolio(st.session_state.user)
        st.write(data)
