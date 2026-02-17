import streamlit as st

def show_dcf(cashflow, info):

    st.header("Intrinsic Value (DCF Model)")

    if cashflow.empty:
        st.warning("No cash flow data available")
        return

    free_cash_flow = cashflow['Free Cash Flow'].iloc[0]

    growth = st.slider("Growth Rate %", 1, 20, 10)
    discount = st.slider("Discount Rate %", 5, 20, 12)

    intrinsic = 0
    for i in range(1,6):
        intrinsic += (free_cash_flow * ((1+growth/100)**i)) / ((1+discount/100)**i)

    shares = info.get("sharesOutstanding",1)
    value = intrinsic / shares

    st.success(f"Estimated Intrinsic Value: ₹{round(value,2)}")

