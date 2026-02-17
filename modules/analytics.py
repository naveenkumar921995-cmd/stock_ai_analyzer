import numpy as np
import pandas as pd
import streamlit as st


# ===============================
# CAGR CALCULATION
# ===============================

def calculate_cagr(series):

    if series is None or len(series) < 2:
        return None

    start_value = series.iloc[-1]
    end_value = series.iloc[0]
    years = len(series)

    if start_value <= 0:
        return None

    cagr = ((end_value / start_value) ** (1/years) - 1) * 100
    return round(cagr, 2)


# ===============================
# RISK METRICS
# ===============================

def calculate_risk_metrics(data):

    returns = data['Close'].pct_change().dropna()

    volatility = returns.std() * np.sqrt(252) * 100
    avg_return = returns.mean() * 252 * 100

    # Risk free rate assumed 6% (India)
    risk_free = 6

    sharpe_ratio = (avg_return - risk_free) / volatility if volatility != 0 else 0

    max_drawdown = (data['Close'] / data['Close'].cummax() - 1).min() * 100

    return round(volatility,2), round(sharpe_ratio,2), round(max_drawdown,2)


# ===============================
# AI WEIGHTED SCORING MODEL
# ===============================

def calculate_ai_score(
        revenue_cagr,
        profit_cagr,
        sharpe_ratio,
        volatility,
        intrinsic_value,
        current_price):

    score = 0

    # Fundamental Weight 40%
    if revenue_cagr and revenue_cagr > 8:
        score += 20
    if profit_cagr and profit_cagr > 8:
        score += 20

    # Risk & Performance 30%
    if sharpe_ratio > 1:
        score += 15
    if volatility < 30:
        score += 15

    # Valuation 30%
    if intrinsic_value and current_price:
        if intrinsic_value > current_price:
            score += 30

    return score
