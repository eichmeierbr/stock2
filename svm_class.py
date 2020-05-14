from Classifier import *
from datetime import date
import stock_market as sm
import numpy as np
from sklearn import svm


class svm_class(Classifier):
    def __init__(self,ticker,inputSize=5, binary=True, risk=0.5):
        self.type = 'SVM'
        self.ticker=ticker
        self.days=inputSize
        self.inputSize = inputSize
        self.binary=binary
        kern = 'sigmoid'
        self.risk_thresh = 1 - risk
        if binary:
            self.svm = svm.SVC(kernel=kern)
            self.svm.probability=True
        else:
            self.svm = svm.SVR(kernel=kern)
    

    def predict(self, inputArray):
        inputArray = np.array(inputArray)
        inputArray.reshape([1,-1])

        if self.binary:
            pred = self.svm.predict_proba(inputArray)
            pred = (np.array(pred)[:,1] > self.risk_thresh)*1
        else:
            pred = self.svm.predict(inputArray)
        return pred



    def fit(self, X, Y):
        self.svm.fit(X,Y)

