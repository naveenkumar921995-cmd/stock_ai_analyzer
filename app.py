import streamlit as st
import matplotlib.pyplot as plt
from scanner import analyze_stock
from auth import register_user, login_user

st.set_page_config(page_title="Stock AI Pro Analyzer", layout="wide")

st.title("🚀 Stock AI Pro Analyzer")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ---------------- LOGIN ---------------- #

if not st.session_state.logged_in:

    menu = st.radio("Select Option", ["Login", "Register"])

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
                st.rerun()
            else:
                st.error(message)

# ---------------- MAIN DASHBOARD ---------------- #

else:

    st.sidebar.success("Logged In ✅")

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    symbol = st.text_input("Enter Stock Symbol (Example: AAPL or RELIANCE.NS)")

    if st.button("Analyze Stock"):

        result = analyze_stock(symbol)

        if "error" in result:
            st.error(result["error"])

        else:
            col1, col2, col3, col4 = st.columns(4)

            col1.metric("Current Price", f"₹ {result['current_price']}")
            col2.metric("RSI", result["rsi"])
            col3.metric("52W High", result["52w_high"])
            col4.metric("52W Low", result["52w_low"])

            st.subheader(f"Signal: {result['signal']}")

            df = result["data"]

            # Price Chart
            st.subheader("Price Chart with MA50 & MA200")

            fig, ax = plt.subplots()
            ax.plot(df["Close"], label="Close")
            ax.plot(df["MA50"], label="MA50")
            ax.plot(df["MA200"], label="MA200")
            ax.legend()

            st.pyplot(fig)

            # RSI Chart
            st.subheader("RSI Indicator")

            fig2, ax2 = plt.subplots()
            ax2.plot(df["RSI"])
            ax2.axhline(70)
            ax2.axhline(30)
            st.pyplot(fig2)
