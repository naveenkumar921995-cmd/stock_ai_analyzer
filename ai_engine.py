import requests
import streamlit as st

def ai_explain(stock, rsi, signal):
    key = st.secrets.get("OPENAI_API_KEY", "")
    if not key:
        return f"{stock}: RSI {rsi}, Signal {signal}"
    headers = {"Authorization": f"Bearer {key}"}
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role":"system","content":"You are a professional stock analyst."},
            {"role":"user","content":f"{stock} RSI {rsi}, Signal {signal}. Explain briefly."}
        ]
    }
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        json=payload
    )
    return response.json()["choices"][0]["message"]["content"]
