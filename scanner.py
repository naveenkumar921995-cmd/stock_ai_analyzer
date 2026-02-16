import yfinance as yf
import pandas as pd
import ta


def analyze_stock(symbol):
    try:
        # Download stock data
        df = yf.download(symbol, period="6mo", interval="1d")

        if df.empty:
            return {"error": "Invalid symbol or no data available."}

        # Calculate RSI
        df["RSI"] = ta.momentum.RSIIndicator(df["Close"]).rsi()

        # Get latest RSI value (IMPORTANT FIX)
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
