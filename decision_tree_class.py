from Classifier import *
from datetime import date
import stock_market as sm
import numpy as np
from sklearn import tree


class dt_class(Classifier):
    def __init__(self,ticker,inputSize=5, binary=True, risk=0.5):
        self.type = 'Decision Tree'
        self.ticker=ticker
        self.days=inputSize
        self.inputSize = inputSize
        self.binary=binary
        self.risk_thresh = risk
        if binary:
            self.dt = tree.DecisionTreeClassifier(max_depth=inputSize)
        else:
            self.dt = tree.DecisionTreeRegressor(max_depth=inputSize)
    

    def predict(self, inputArray):
        inputArray = np.array(inputArray)
        inputArray.reshape([1,-1])

        if self.binary:
            pred = self.dt.predict_proba(inputArray)
            pred = (np.array(pred)[:,1] > self.risk_thresh)*1
        else:
            pred = self.dt.predict(inputArray)
        return pred


    def fit(self, X, Y):
        self.dt.fit(X,Y)
