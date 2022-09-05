from datetime import date
import yfinance as yf
import os.path
import pandas as pd
import workdays as wd
import backtrader as bt

data = bt.feeds.YahooFinanceData(
    dataname='AAPL',
    fromdate=date(1990, 1, 1),
    todate=date(2020, 12, 31),
    reverse=False)

print(data)
data.writer()