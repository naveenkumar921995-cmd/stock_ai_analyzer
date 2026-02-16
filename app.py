import streamlit as st
from database import init_db
from auth import register_user, login_user
from scanner import analyze_stock
from ai_engine import ai_explain
from portfolio import add_stock, get_portfolio

# Initialize database
init_db()

st.set_page_config(page_title="AI Stock SaaS", layout="wide")
st.title("🚀 AI Stock Analyzer SaaS")

# -------------------------------
# Session Setup
# -------------------------------
if "user" not in st.session_state:
    st.session_state.user = None

# -------------------------------
# Sidebar Menu
# -------------------------------
menu = ["Login", "Register"]
choice = st.sidebar.selectbox("Menu", menu)

# -------------------------------
# Register Section
# -------------------------------
if choice == "Register":

    st.subheader("Create Account")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        if username and password:
            success = register_user(username, password)
            if success:
                st.success("Account created successfully!")
            else:
                st.error("Username already exists.")
        else:
            st.warning("Please enter username and password.")

# -------------------------------
# Login Section
# -------------------------------
elif choice == "Login":

    st.subheader("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if login_user(username, password):
            st.session_state.user = username
            st.success("Login successful!")
        else:
            st.error("Invalid credentials")

# -------------------------------
# Main App After Login
# -------------------------------
if st.session_state.user:

    st.sidebar.success(f"Welcome {st.session_state.user}")

    page = st.sidebar.selectbox(
        "Dashboard",
        ["Stock Scanner", "Portfolio"]
    )

    # ===============================
    # STOCK SCANNER PAGE
    # ===============================
    if page == "Stock Scanner":

        st.subheader("📈 Stock Scanner")

        symbol = st.text_input("Enter NSE Stock (Example: RELIANCE)")

        if st.button("Analyze Stock"):

            if not symbol:
                st.warning("Please enter a stock symbol.")
            else:
                symbol = symbol.strip().upper()

                # Automatically add .NS if missing
                if not symbol.endswith(".NS"):
                    symbol = symbol + ".NS"

                result = analyze_stock(symbol)

                # If error returned from scanner
                if "Error" in result:
                    st.error(result["Error"])

                else:
                    st.success("Analysis Complete")
                    st.write(result)

                    # AI Explanation
                    try:
                        explanation = ai_explain(
                            result["Stock"],
                            result["RSI"],
                            result["Signal"]
                        )
                        st.info(explanation)
                    except:
                        st.info("AI explanation unavailable.")

    # ===============================
    # PORTFOLIO PAGE
    # ===============================
    elif page == "Portfolio":

        st.subheader("💼 Portfolio Tracker")

        stock = st.text_input("Stock Symbol (Example: TCS)")
        qty = st.number_input("Quantity", min_value=1)
        price = st.number_input("Buy Price", min_value=0.0)

        if st.button("Add to Portfolio"):

            if stock:
                stock = stock.strip().upper()

                if not stock.endswith(".NS"):
                    stock = stock + ".NS"

                add_stock(st.session_state.user, stock, qty, price)
                st.success("Stock added to portfolio")
            else:
                st.warning("Please enter stock name.")

        st.subheader("Your Holdings")

        data = get_portfolio(st.session_state.user)

        if data:
            st.table(data)
        else:
            st.info("No stocks in portfolio yet.")
