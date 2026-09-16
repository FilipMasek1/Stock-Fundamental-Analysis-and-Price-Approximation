import yfinance as yf
import GUI

"""Checks connection to yfinance and launches corresponding GUI"""

try:
    value = yf.Ticker("AAPL").info.get("returnOnEquity")
    connection = True
except Exception:
    connection = False

if connection == True:
    GUI.RAWindow().MainWindow()
else:
    GUI.MAWindow().MainWindow()
