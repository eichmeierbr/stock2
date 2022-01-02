import sys
import data.getdata as get_data
from datetime import date
import numpy as np

sys.path.append('./traders')
from random_trader import randomTrader
from holdTrader import holdTrader

class BackTester:
    def __init__(self, tickers, start_date, end_date):
        self.data = []
        self.tickers = tickers
        self.start_date = start_date
        self.end_date = end_date
        self.day = 0

        self.prepare_data()


    def prepare_data(self):
        for ticker in self.tickers:
            ## Currently only do daily data
            tick = get_data.Ticker_history(ticker=ticker, interval='1d')
            tick.set_start_day(self.start_date)
            self.data.append(tick)

    def advanceTime(self):
        for i in range(len(self.data)):
            self.data[i].advance_time()
        self.day = self.data[0].now_data[0]  


    def backtest(self, trader):
        self.day = self.data[0].now_data[0]
        ## For each day
        while self.day <= self.end_date:
            
            print('Processing day: ', self.day)

            ## Feed data to to agent
            actions = trader.act(self.data)

            ## Perform market interactions
            trader.performTransactions(self.data,actions)

            ## Advance time
            self.advanceTime()
            trader.advanceTime()
            pass
        print('Final Value: ', trader.totalValue)
        pass



## Select/Load Stock(s)
stockUniverse = ['aapl','msft']
b = BackTester(stockUniverse, date(2000,1,1), date(2008,1,1))

## Define trading agent
trader = holdTrader()
trader.initPortfolio(stockUniverse)

b.backtest(trader)
