import sys
import data.getdata as get_data
from datetime import date, datetime, timedelta
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

sys.path.append('./traders')
from random_trader import randomTrader
from holdTrader import holdTrader
from movingAverageCross import simpleMovingAverageCrossTrader

class BackTester:
    def __init__(self, tickers, start_date, end_date):
        self.data = []
        self.tickers = tickers
        self.start_date = start_date
        self.end_date = end_date
        self.day = 0
        self.openings = []

        self.prepare_data()

    def updateOpenings(self):
        todaysOpenings = []
        for dat in self.data:
            todaysOpenings.append(dat.now_data[1])
        self.openings.append(todaysOpenings[:])

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
        self.days.append(self.day)

    def plotResults(self, traders):
        ## Format for days
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        interv = int(len(self.days)/4 + 1)
        plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=interv))
        plt.gcf().autofmt_xdate()

        self.days = np.array(self.days)
        for trader in traders:
            trader.plotResults(self.days)

        
        self.openings = np.array(self.openings)/self.openings[0]
        for i in range(len(self.data)):
            print('%s Final Value: %.2f' %(self.data[i].ticker, self.openings[-1,i]))
            plt.plot(self.days, self.openings[:,i], label=self.data[i].ticker)
        plt.legend()
        plt.show()

    def backtest(self, traders):
        self.day = self.data[0].now_data[0]

        # TODO: Fix these to numpy extract the ranges
        # FORNOW: Just append for each day iteration
        self.days = [self.day]
        ## For each day
        while self.day < self.end_date:
            
            # print('Processing day: ', self.day)
            self.updateOpenings()

            for trader in traders:
                ## Feed data to to agent
                actions = trader.act(self.data)
    
                ## Perform market interactions
                trader.performTransactions(self.data,actions)
    
                ## Advance time
                trader.advanceTime()
            self.advanceTime()
            pass
        
        self.updateOpenings()

        ### Plot function
        self.plotResults(traders)



## Select/Load Stock(s)
stockUniverse = ['bbby']
b = BackTester(stockUniverse, date(2022,1,1), date(2022,8,29))

## Define trading agents
traders= []
traders.append(holdTrader())
traders.append(randomTrader())
traders.append(simpleMovingAverageCrossTrader())

for trader in traders:
    trader.initPortfolio(stockUniverse)

b.backtest(traders)
