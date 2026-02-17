import streamlit as st
from scanner import analyze_stock
from auth import register_user, login_user

st.set_page_config(page_title="Stock AI Analyzer", layout="centered")

st.title("📈 Stock AI Analyzer")

# Session state for login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ---------------- LOGIN / REGISTER ---------------- #

if not st.session_state.logged_in:

    menu = st.radio("Choose Option", ["Login", "Register"])

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if menu == "Register":
        if st.button("Register"):
            success, message = register_user(username, password)
            if success:
                st.success(message)
            else:
                st.error(message)

    if menu == "Login":
        if st.button("Login"):
            success, message = login_user(username, password)
            if success:
                st.session_state.logged_in = True
                st.success("Login successful")
                st.rerun()
            else:
                st.error(message)

# ---------------- STOCK ANALYZER ---------------- #

else:
    st.success("Welcome! You are logged in ✅")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    st.subheader("Analyze Stock")

    symbol = st.text_input("Enter Stock Symbol (Example: AAPL or RELIANCE.NS)")

    if st.button("Analyze"):
        if symbol:
            result = analyze_stock(symbol)

            if "error" in result:
                st.error(result["error"])
            else:
                st.write("### Result")
                st.write(f"**Symbol:** {result['symbol']}")
                st.write(f"**Current Price:** ₹ {result['current_price']}")
                st.write(f"**RSI:** {result['rsi']}")
                st.write(f"**Signal:** {result['signal']}")
        else:
            st.warning("Please enter a stock symbol.")
