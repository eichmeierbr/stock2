from Classifier import *
from datetime import date
import stock_market as sm
import numpy as np
from sklearn import neighbors
from sklearn.ensemble import AdaBoostClassifier, AdaBoostRegressor


class knn_classifier(Classifier):
    def __init__(self,ticker,inputSize=5, binary=True, n_neighbors=15, risk=0.5, adaboost=False):
        self.type = 'KNN'
        self.ticker=ticker
        self.days=inputSize
        self.inputSize = inputSize
        self.binary=binary
        self.risk_thresh = risk
        self.adaboost = adaboost
        if binary:
            self.clf = neighbors.KNeighborsClassifier(n_neighbors, weights='distance')
        else:
            self.clf = neighbors.KNeighborsRegressor(n_neighbors, weights='distance')
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

