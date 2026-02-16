import sqlite3

def add_stock(username, stock, qty, price):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("""
        INSERT INTO portfolio (username, stock, quantity, buy_price)
        VALUES (?,?,?,?)
    """,(username, stock, qty, price))
    conn.commit()
    conn.close()

def get_portfolio(username):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT stock, quantity, buy_price FROM portfolio WHERE username=?",
              (username,))
    data = c.fetchall()
    conn.close()
    return data
