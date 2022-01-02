from Classifier import *
from datetime import date
import stock_market as sm
import numpy as np


class majorityVoteClass(Classifier):
    def __init__(self,ticker, classifiers, inputSize=5, binary=True, risk=0.5):
        self.type = 'Majority Vote'
        self.ticker=ticker
        self.days=inputSize
        self.inputSize = inputSize
        self.binary=binary
        self.risk_thresh = risk
        self.clfs = classifiers
        self.clf = self.clfs[0]
        self.weights = np.ones(len(classifiers))
        self.discount = 0.95
        self.actions = []

    def processData(self, endDay=date.today(), numDays=100):
        inputSize = self.inputSize
        numDays = self.days+numDays
        data = np.array(sm.dayToDayDiffPercent(self.ticker,which='Open', numDays = numDays, endDay = endDay))

        X, Y = sm.array2dataset(data, inputSize)
        if self.binary: Y = (np.array(Y) > 0)*1
        return X,Y

    # This function assumes all the sub-classifiers are all trained on separate data
    def trainClf(self, endDay=date.today(), numTrainDays=100, full_train=True):
        self.inputSize = 0
        for i in range(len(self.clfs)):
            if self.inputSize < self.clfs[i].inputSize:
                self.inputSize = self.clfs[i].inputSize
            self.clfs[i].trainClf(endDay=endDay, numTrainDays=100)
    

    def predict(self, inputArray):
        inputArray = np.array(inputArray)
        self.actions = []
        preds = np.zeros([inputArray.shape[0],2])
        for i in range(len(self.clfs)):
            self.clf = self.clfs[i]
            actions = self.clf.predict(inputArray[:,-self.clf.inputSize:])
            for j in range(len(actions)):
                act = actions[j]
                preds[j,(act>0.01)*1] += self.weights[i]
            self.actions.append(actions)

        maxVotes = np.max(preds,axis=1)
        pred = np.argmax(preds, axis=1)
        conf = maxVotes/np.sum(self.weights)
        pred = pred * (conf > self.risk_thresh)*1
        # print('%s: Pred: %i, Conf: %.2f' %(self.ticker, pred, conf))

        return pred

    def predictSingleClf(self, inputArray):
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
