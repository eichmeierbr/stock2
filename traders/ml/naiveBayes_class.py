from Classifier import *
from datetime import date
import stock_market as sm
import numpy as np
from sklearn import naive_bayes
from sklearn.ensemble import AdaBoostClassifier, AdaBoostRegressor


class nb_class(Classifier):
    def __init__(self,ticker,inputSize=5, binary=True, risk=0.8, adaboost=False):
        self.type = 'Naive Bayes'
        self.ticker=ticker
        self.days=inputSize
        self.inputSize = inputSize
        self.binary=binary
        self.adaboost = adaboost
        self.clf = naive_bayes.GaussianNB()
        if self.adaboost: 
            if binary:
                self.clf=AdaBoostClassifier(base_estimator=self.clf, n_estimators=100)
        self.risk_thresh=risk
    

    def predict(self, inputArray):
        inputArray = np.array(inputArray)
        inputArray.reshape([1,-1])
        pred = self.clf.predict_proba(inputArray)
        pred_out = (np.array(pred)[:,1] > self.risk_thresh)*1
        return pred_out



    def fit(self, X, Y):
        self.clf.fit(X,Y)
