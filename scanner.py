import yfinance as yf
import pandas as pd
import numpy as np


def calculate_rsi(data, period=14):
    delta = data.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi


def analyze_stock(symbol):
    try:
        df = yf.download(symbol, period="1y")

        if df.empty:
            return {"error": "Invalid symbol or no data available."}

        df["MA50"] = df["Close"].rolling(50).mean()
        df["MA200"] = df["Close"].rolling(200).mean()
        df["RSI"] = calculate_rsi(df["Close"])

        latest = df.iloc[-1]

        current_price = round(float(latest["Close"]), 2)
        rsi = round(float(latest["RSI"]), 2)
        ma50 = round(float(latest["MA50"]), 2)
        ma200 = round(float(latest["MA200"]), 2)

        week_52_high = round(float(df["High"].max()), 2)
        week_52_low = round(float(df["Low"].min()), 2)

        # Signal Logic
        score = 0

        if rsi < 30:
            score += 2
        elif rsi > 70:
            score -= 2

        if current_price > ma50:
            score += 1
        else:
            score -= 1

        if current_price > ma200:
            score += 2
        else:
            score -= 2

        if score >= 3:
            signal = "Strong Buy"
        elif score == 2:
            signal = "Buy"
        elif score == 1:
            signal = "Mild Buy"
        elif score == 0:
            signal = "Neutral"
        elif score == -1:
            signal = "Mild Sell"
        elif score == -2:
            signal = "Sell"
        else:
            signal = "Strong Sell"

        return {
            "symbol": symbol.upper(),
            "data": df,
            "current_price": current_price,
            "rsi": rsi,
            "ma50": ma50,
            "ma200": ma200,
            "52w_high": week_52_high,
            "52w_low": week_52_low,
            "signal": signal
        }

    except Exception as e:
        return {"error": str(e)}
