import yfinance as yf
import pandas as pd


def calculate_rsi(data, period=14):
    delta = data.diff()

    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()

    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))

    return rsi


def analyze_stock(symbol):
    try:
        df = yf.download(symbol, period="6mo", interval="1d")

        if df.empty:
            return {"error": "Invalid symbol or no data available."}

        df["RSI"] = calculate_rsi(df["Close"])

        latest_rsi = df["RSI"].iloc[-1]

        signal = "Neutral"

        if latest_rsi < 30:
            signal = "Oversold (Buy Signal)"
        elif latest_rsi > 70:
            signal = "Overbought (Sell Signal)"

        return {
            "symbol": symbol.upper(),
            "current_price": round(df["Close"].iloc[-1], 2),
            "rsi": round(float(latest_rsi), 2),
            "signal": signal
        }

    except Exception as e:
        return {"error": str(e)}
