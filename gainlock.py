# GainLock trading bot

# If you have a Robinhood account you can use 'robin-stocks' package 
# to interact with the Robinhood API

# If you would like to read more about the documentation behind this API here's the link!
# https://pypi.org/project/robin-stocks/

# required imports
import pandas as pd 
import time

# Historical data import
import yfinance as yf  

# Robinhood imports
import robin_stocks as r 

#---- 1. Login to your Robinhood account ----# 
username = 'johncena@gmail.com'
password = '*******'
# login = r.login(username, password)


# Once your logged, check your holdings by running this command
# r.build_holdings()

# Fetch historical data
data = yf.download("GOOGL", start='2024-06-01', end='2024-06-25', interval='15m')
data.iloc[:,:]

#---- 2. Making a signal function to detect bearish/bullish patterns in the market ----#

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
data["signal"] = signal

# Prints the signal for Google stock
print(data.signal.value_counts())

#---- 3. Connecting to the market and executing trades ----#

# Following imports for API connection 

# from apscheduler.schedulers.blocking import BlockingScheduler
# from oandapyV20 import API
# import oandapyV20.endpoints.orders as orders
# from oandapyV20.contrib.requests import MarketOrderRequest
# from oanda_candles import Pair, Gran, CandleClient
# from oandapyV20.contrib.requests import TakeProfitDetails, StopLossDetails

from config import access_token, accountID
def get_candles(n):
    #access_token='XXXXXXX' 
    client = CandleClient(access_token, real=False)
    collector = client.get_collector(Pair.GOOGL, Gran.M15)
    candles = collector.grab(n)
    return candles

candles = get_candles(3)
for candle in candles:
    print(float(str(candle.bid.o))>1)  # Convert the string candle bid to a floating point number 


#---- Buy/Sell shares ----#

def execute_trades():
    candles = get_candles(3)
    stockdf = pd.DataFrame(columns=['Open','Close','High','Low'])
    
    i = 0
    for candle in candles:
        stockdf.loc[i, ['Open']] = float(str(candle.bid.o))
        stockdf.loc[i, ['Close']] = float(str(candle.bid.c))
        stockdf.loc[i, ['High']] = float(str(candle.bid.h))
        stockdf.loc[i, ['Low']] = float(str(candle.bid.l))
        i = i + 1

    stockdf['Open'] = stockdf['Open'].astype(float)
    stockdf['Close'] = stockdf['Close'].astype(float)
    stockdf['High'] = stockdf['High'].astype(float)
    stockdf['Low'] = stockdf['Low'].astype(float)

    # Call the stock signal function so the algo knows whether it's a buy/sell 
    signal = stock_signal(stockdf.iloc[:-1,:])
    
    # EXECUTING TRADES
    #accountID = "XXXXXXX" # type your account ID here
    client = API(access_token)
         
    # Stop Loss Take Profit
    SLTPRatio = 2
    previous_candle_price = abs(stockdf['High'].iloc[-2] - stockdf['Low'].iloc[-2])
    
    SLBuy = float(str(candle.bid.o)) - previous_candle_price
    SLSell = float(str(candle.bid.o)) + previous_candle_price

    # If you reach your Take Profit number decide whether to buy more or sell 
    TPBuy = float(str(candle.bid.o)) + previous_candle_price * SLTPRatio
    TPSell = float(str(candle.bid.o)) - previous_candle_price * SLTPRatio
    
    print(stockdf.iloc[:-1,:])
    print(TPBuy, "  ", SLBuy, "  ", TPSell, "  ", SLSell)
    signal = 2

    # Sell stock
    if signal == 1:
        buy = MarketOrderRequest(instrument = "GOOGL", units =- 1000, takeProfitOnFill = TakeProfitDetails(price = TPSell).data, stopLossOnFill = StopLossDetails(price=SLSell).data)
        order = orders.OrderCreate(accountID, data = buy.data)
        client_order_request = client.request(order)
        print(client_order_request)
    # Buy stock
    elif signal == 2:
        buy = MarketOrderRequest(instrument = "GOOGL", units = 1000, takeProfitOnFill = TakeProfitDetails(price=TPBuy).data, stopLossOnFill = StopLossDetails(price=SLBuy).data)
        order = orders.OrderCreate(accountID, data = buy.data)
        client_order_request = client.request(order)
        print(client_order_request)  # Displays the orders so you can track what the algorithm is doing