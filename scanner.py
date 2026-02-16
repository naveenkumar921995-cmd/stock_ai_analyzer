import yfinance as yf
import pandas as pd

def analyze_stock(symbol):
    df = yf.download(symbol, period="6mo")
    df["RSI"] = 100 - (100 / (1 + df["Close"].pct_change().rolling(14).mean()))
    df["MA20"] = df["Close"].rolling(20).mean()
    df["MA50"] = df["Close"].rolling(50).mean()
    latest = df.iloc[-1]
    rsi = latest["RSI"]
    price = latest["Close"]
    if rsi < 30:
        signal = "BUY"
    elif rsi > 70:
        signal = "SELL"
    else:
        signal = "HOLD"
    risk = abs(rsi - 50)
    return {
        "Stock": symbol,
        "Price": round(price,2),
        "RSI": round(rsi,2),
        "Signal": signal,
        "Risk Score": round(risk,2)
    }
