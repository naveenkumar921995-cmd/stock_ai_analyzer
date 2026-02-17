import yfinance as yf

def get_stock_data(symbol):
    ticker = yf.Ticker(symbol)
    info = ticker.info
    history = ticker.history(period="2y")
    financials = ticker.financials.T
    cashflow = ticker.cashflow.T
    return ticker, info, history, financials, cashflow

