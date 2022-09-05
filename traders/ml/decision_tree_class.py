from Classifier import *
from datetime import date
import stock_market as sm
import numpy as np
from sklearn import tree
from sklearn.ensemble import AdaBoostClassifier, AdaBoostRegressor


class dt_class(Classifier):
    def __init__(self,ticker,inputSize=5, binary=True, risk=0.5, adaboost=False):
        self.type = 'Decision Tree'
        self.ticker=ticker
        self.days=inputSize
        self.inputSize = inputSize
        self.binary=binary
        self.adaboost = adaboost
        self.risk_thresh = risk

        if binary:
            self.clf = tree.DecisionTreeClassifier(max_depth=inputSize)
            if adaboost: self.clf = AdaBoostClassifier(base_estimator=self.clf, n_estimators=100)
        else:
            self.clf = tree.DecisionTreeRegressor(max_depth=inputSize)
            if adaboost: self.clf = AdaBoostRegressor(base_estimator=self.clf, n_estimators=100)
    

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
