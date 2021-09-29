import os.path
import pandas as pd
import data.getdata as get_data
from datetime import date
import numpy as np

class BackTester:
    def __init__(self, tickers, start_date, end_date):
        self.data = []
        self.histories = []
        self.headers = []
        self.tickers = tickers
        self.start_date = start_date
        self.end_date = end_date

        self.prepare_data()

    def prepare_data(self):
        for ticker in self.tickers:
            ## Currently only do daily data
            tick = get_data.Ticker_history(ticker=ticker, interval='1d')
            self.headers = tick.headers
            self.data.append(tick.data)
            previous_data = self.data[-1][self.data[-1][:,0] < self.start_date]
            self.histories.append(previous_data)

            self.data[-1] = self.data[-1][(self.data[-1][:,0] >= self.start_date) & (self.data[-1][:,0]<=self.end_date)]

        self.data = np.swapaxes(self.data, 0, 1)


    def backtest(self, trader):
        ## For each day
        for day in self.data:
            ## Feed data to to agent
            # trader.act(day)

            ## If agent buy
            pass
        pass

## Define trading agent


## Select/Load Stock(s)
b = BackTester(['aapl', 'msft'], date(2000,1,1), date(2005,1,1))


b.backtest()
