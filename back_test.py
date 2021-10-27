import os.path
import pandas as pd
import data.getdata as get_data
from datetime import date
import numpy as np

class BackTester:
    def __init__(self, tickers, start_date, end_date):
        self.data = []
        self.tickers = tickers
        self.start_date = start_date
        self.end_date = end_date

        self.prepare_data()

    # def prepare_data(self):
    #     for ticker in self.tickers:
    #         ## Currently only do daily data
    #         tick = get_data.Ticker_history(ticker=ticker, interval='1d')
    #         self.headers = tick.headers
    #         self.data.append(tick.data)
    #         previous_data = self.data[-1][self.data[-1][:,0] < self.start_date]
    #         self.histories.append(previous_data)

    #         self.data[-1] = self.data[-1][(self.data[-1][:,0] >= self.start_date) & (self.data[-1][:,0]<=self.end_date)]

    #     self.data = np.swapaxes(self.data, 0, 1)

    def prepare_data(self):
        for ticker in self.tickers:
            ## Currently only do daily data
            tick = get_data.Ticker_history(ticker=ticker, interval='1d')
            tick.set_start_day(self.start_date)
            self.data.append(tick)


    def backtest(self, trader):
        day = self.data[0].now_data[0]
        ## For each day
        while day <= self.end_date:
            print('Processing day: ', day)
            #@ delete future

            ## Feed data to to agent
            # trader.act(day)

            ## Perform market interactions

            ## Advance time
            for i in range(len(self.data)):
                self.data[i].advance_time()
            day = self.data[0].now_data[0]
            pass
        pass

## Define trading agent


## Select/Load Stock(s)
b = BackTester(['aapl', 'msft'], date(2000,1,1), date(2005,1,1))


b.backtest(7)
