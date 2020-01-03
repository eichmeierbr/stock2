from Classifier import *
from datetime import date
import stock_market as sm
import numpy as np

# Simple kDay Mean Classifier. This class decides to buy if the preivous k-Day mean is less than
# the live price. The class sells if the live price is less than the mean
# The only function can create the rolling mean from each minute wihtin the past 5 days, or 
# from the open/closing values from the past self.days

class kDayMean(Classifier):
    def __init__(self,ticker,days=5):
        self.ticker=ticker
        self.days=days
    
    def predict(self, day=date.today(), minute = False, which = 'Open'):

        if minute:
            data = sm.liveMinutePrice(self.ticker)
            av = np.mean(data)
            nowPrice = sm.livePrice(self.ticker)

        else:
            data = sm.prices(self.ticker,which=which, inter='1m', numDays = self.days, endDay = day)
            av = np.mean(data)
            nowPrice = sm.livePrice(self.ticker)

        if nowPrice > av:
            return 1
        else:
            return 0