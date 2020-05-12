from Classifier import *
from datetime import date
import stock_market as sm
import numpy as np
from sklearn import svm


class svm_class(Classifier):
    def __init__(self,ticker,inputSize=5, binary=True):
        self.ticker=ticker
        self.days=inputSize
        self.inputSize = inputSize
        self.binary=binary
        kern = 'sigmoid'
        if binary:
            self.svm = svm.SVC(kernel=kern)
        else:
            self.svm = svm.SVR(kernel=kern)
    

    def predict(self, inputArray):
        inputArray = np.array(inputArray)
        inputArray.reshape([1,-1])
        pred = self.svm.predict(inputArray)
        return pred


    def processData(self):
        return []


    def train(self, X, Y):
        self.svm.fit(X,Y)

