from Classifier import *
from datetime import date
import stock_market as sm
import numpy as np
from sklearn import naive_bayes


class nb_class(Classifier):
    def __init__(self,ticker,inputSize=5, binary=True, risk=0.8):
        self.type = 'Naive Bayes'
        self.ticker=ticker
        self.days=inputSize
        self.inputSize = inputSize
        self.binary=binary
        self.dt = naive_bayes.GaussianNB()
        self.risk_thresh=risk
    

    def predict(self, inputArray):
        inputArray = np.array(inputArray)
        inputArray.reshape([1,-1])
        pred = self.dt.predict_proba(inputArray)
        pred_out = (np.array(pred)[:,1] > self.risk_thresh)*1
        return pred_out



    def fit(self, X, Y):
        self.dt.fit(X,Y)
