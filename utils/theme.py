import streamlit as st

def apply_dark_theme():
    st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
        color: #FAFAFA;
    }
    [data-testid="metric-container"] {
        background-color: #1c1f26;
        padding: 15px;
        border-radius: 12px;
    }
    h1, h2, h3 {
        color: #00BFFF;
    }
    </style>
    """, unsafe_allow_html=True)

