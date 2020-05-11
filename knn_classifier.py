from Classifier import *
from datetime import date
import stock_market as sm
import numpy as np
from sklearn import neighbors


class knn_classifier(Classifier):
    def __init__(self,ticker,inputSize=5, binary=True, n_neighbors=15):
        self.ticker=ticker
        self.days=inputSize
        self.inputSize = inputSize
        self.binary=binary
        if binary:
            self.knn = neighbors.KNeighborsClassifier(n_neighbors, weights='distance')
        else:
            self.knn = neighbors.KNeighborsRegressor(n_neighbors, weights='distance')
    

    def predict(self, inputArray):
        inputArray = np.array(inputArray)
        inputArray.reshape([1,-1])
        pred = self.knn.predict(inputArray)
        return pred


    def processData(self):
        return []


    def train(self, X, Y):
        self.knn.fit(X,Y)

