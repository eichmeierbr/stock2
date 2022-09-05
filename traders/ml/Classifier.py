from datetime import date, timedelta
import workdays as wd
import numpy as np
import stock_market as sm

class Classifier:
    def __init__(self, ticker):
        self.type = 'Parent'
        self.ticker = ticker
        self.inputSize=5
        self.days = self.inputSize
        self.binary=True

    def processData(self, endDay=date.today(), numDays=100):
        inputSize = self.inputSize
        numDays = self.days+numDays
        data = np.array(sm.dayToDayDiffPercent(self.ticker,which='Open', numDays = numDays, endDay = endDay))

        X, Y = sm.array2dataset(data, inputSize)
        if self.binary: Y = (np.array(Y) > 0)*1
        return X,Y

    def trainClf(self, endDay=date.today(), numTrainDays=100):
        X, Y = self.processData(endDay, numTrainDays)
        self.fit(X, Y)


    def predict(self, day):
        return [1]

    def fit(self, input, labels):
        return


    def predictToday(self, day=date.today()):
        today = wd.workday(day, 1) 
        data = sm.dayToDayDiffPercent(self.ticker,which='Open', numDays = self.inputSize, endDay=today)
        if len(data) < self.inputSize: return -1
        act = self.predict([data])
        return act