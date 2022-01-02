from Classifier import *
from datetime import date
import stock_market as sm
import numpy as np
from sklearn.cluster import KMeans
from sklearn.ensemble import AdaBoostClassifier, AdaBoostRegressor


class k_meansCluster(Classifier):
    def __init__(self,ticker,inputSize=5, binary=True, adaboost=False):
        self.type = 'K-Means'
        self.ticker=ticker
        self.days=inputSize
        self.inputSize = inputSize
        self.binary=binary
        self.adaboost = adaboost
        self.clf = KMeans(n_clusters=2, random_state=0)
        if self.adaboost: self.clf=AdaBoostRegressor(base_estimator=self.clf, n_estimators=100)
    

    def predict(self, inputArray):
        inputArray = np.array(inputArray)
        inputArray.reshape([1,-1])
        pred = self.clf.predict(inputArray)
        return pred


    def fit(self, X, Y):
        self.clf.fit(X,Y)

