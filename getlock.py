# GetLock trading bot

# If you have a robinhood account you can use 'robin-stocks' package 
# to interact with the Robinhood API

# Link: https://pypi.org/project/robin-stocks/

import yfinance as yf  # historical market data library 
import pandas as pd 

# Fetch historical data
tech_stocks = ['AAPL', 'MSFT', 'NVDA', 'GOOGL']
data = yf.download(tech_stocks, start='2024-06-01', end='2024-06-25', interval='15m')

# Making a signal function to detect bearish/bullish patterns in the market 

def stock_signal(df):
    pass