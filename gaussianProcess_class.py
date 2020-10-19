from Classifier import *
from datetime import date
import stock_market as sm
import numpy as np
from sklearn.gaussian_process import GaussianProcessRegressor, GaussianProcessClassifier
from sklearn.gaussian_process.kernels import DotProduct, WhiteKernel
from sklearn.ensemble import AdaBoostClassifier, AdaBoostRegressor

class gaussProcess_classifier(Classifier):
    def __init__(self,ticker,inputSize=5, binary=True, risk=0.5, numTrainDays=300, adaboost=False):
        self.type = 'Gaussian Process'
        self.ticker=ticker
        self.days=inputSize
        self.inputSize = inputSize
        self.binary=binary
        self.risk_thresh = risk
        self.adaboost = adaboost
        self.numTrainDays = numTrainDays
        if binary:
            self.clf = GaussianProcessClassifier()
        else:
            self.clf = GaussianProcessRegressor()
            if adaboost: self.clf = AdaBoostRegressor(base_estimator=self.clf, n_estimators=100)


    def trainClf(self, endDay=date.today(), numTrainDays=100):
        X, Y = self.processData(endDay, self.numTrainDays)
        self.fit(X, Y)
    

    def predict(self, inputArray):
        inputArray = np.array(inputArray)
        inputArray.reshape([1,-1])


        if self.binary:
            pred = self.clf.predict_proba(inputArray)
            pred = (np.array(pred)[:,1] > self.risk_thresh)*1
        else:
            pred = self.clf.predict(inputArray)
        return pred



    def fit(self, X, Y):
        self.clf.fit(X,Y)

