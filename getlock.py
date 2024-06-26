# GetLock trading bot

# If you have a robinhood account you can use 'robin-stocks' package 
# to interact with the Robinhood API

# If you would like to read more about the documentation behind this API here's the link!
# Link: https://pypi.org/project/robin-stocks/

# required imports
import pandas as pd 
import time

# Historical data import
import yfinance as yf  

# Robinhood imports
import robin_stocks as r 

# Login to your Robinhood account
username = 'johncena@gmail.com'
password = '*******'
login = r.login(username, password)


# Once your logged, check your holdings by running this command
r.build_holdings()

# Fetch historical data
tech_stocks = ['AAPL', 'MSFT', 'NVDA', 'GOOGL']
data = yf.download(tech_stocks, start='2024-06-01', end='2024-06-25', interval='15m')

# Making a signal function to detect bearish/bullish patterns in the market 
# It'll tell us whether we should buy or sell

def stock_signal(df):
    market_open = df.Open.iloc[-1]
    market_close = df.Close.iloc[-1]
    previous_open = df.Open.iloc[-2]
    previous_close = df.Close.iloc[-2]

    # Bearish Pattern
    if (market_open > market_close and 
    previous_open < previous_close and 
    market_close < previous_open and
    market_open >= previous_close):
        return 1

    # Bullish Pattern
    elif (market_open < market_close and 
        previous_open > previous_close and 
        market_close > previous_open and
        market_open <= previous_close):
        return 2
    
    # No clear pattern
    else:
        return 0

signal = []
signal.append(0)
for i in range(1,len(data)):
    df = data[i-1:i+1]
    signal.append(stock_signal(df))
#signal_generator(data)
data["signal"] = signal