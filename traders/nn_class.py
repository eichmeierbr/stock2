from Classifier import *
from datetime import date
import stock_market as sm
import numpy as np
from sklearn.neural_network import MLPClassifier,MLPRegressor
from sklearn.ensemble import AdaBoostClassifier, AdaBoostRegressor


class nn_class(Classifier):
    def __init__(self,ticker,inputSize=5, binary=True, risk=0.5, adaboost=False, layers=(30,30), act_func='relu', solver='sgd'):
        self.type = 'ANN'
        self.ticker=ticker
        self.days=inputSize
        self.inputSize = inputSize
        self.binary=binary
        self.risk_thresh = 1 - risk
        self.adaboost = adaboost

        if binary:
            self.clf = MLPClassifier(hidden_layer_sizes=layers, activation=act_func, alpha=0.0001,
                        solver=solver, learning_rate='adaptive', max_iter=400)
            self.clf.probability=True
            if adaboost: self.clf = AdaBoostClassifier(base_estimator=self.clf, n_estimators=100)

        else:
            self.clf = MLPRegressor(hidden_layer_sizes=layers, activation=act_func, alpha=0.0001,
                        solver=solver, learning_rate='adaptive', max_iter=600)
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

