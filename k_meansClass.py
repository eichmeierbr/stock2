from Classifier import *
from datetime import date
import stock_market as sm
import numpy as np
from sklearn.cluster import KMeans


class k_meansCluster(Classifier):
    def __init__(self,ticker,inputSize=5, binary=True):
        self.ticker=ticker
        self.days=inputSize
        self.inputSize = inputSize
        self.binary=binary
        self.kmeans = KMeans(n_clusters=2, random_state=0)
    

    def predict(self, inputArray):
        inputArray = np.array(inputArray)
        inputArray.reshape([1,-1])
        pred = self.kmeans.predict(inputArray)
        return pred


    def processData(self):
        return []


    def train(self, X, Y):
        self.kmeans.fit(X,Y)

