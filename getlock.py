import yfinance as yf  # historical market data library 
import pandas as pd 


# Fetch historical data
tech_stocks = ['AAPL', 'MSFT', 'NVDA', 'GOOGL']
data = yf.download(tech_stocks, start='2024-06-01', end='2024-06-25')

# Print the first few rows of the data
print(data.head())