from kDayClassifier import *
from knn_classifier import *
from k_meansClass import *
from svm_class import *
from decision_tree_class import *
from naiveBayes_class import *
from majority_vote_class import *
from gaussianProcess_class import *
from tensorForceAgent import *

from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import VotingClassifier

from datetime import date, timedelta
import workdays as wd
import numpy as np
import stock_market as sm
import os, math, multiprocessing
from functools import partial
from os.path import join


def printYesterdayResults(ticker):
    day = wd.workday(date.today(),1)
    price = sm.dayToDayDiffPercent(ticker,numDays=1, endDay=day)
    print('%s: %.2f' %(ticker,price[0]))



def getTodayPredictions(ticker, endDay=date.today()):
    # clf = kDayMean(ticker, days=3)
    clf1 = knn_classifier(ticker, inputSize=8, binary=True, n_neighbors=3, risk = 0.5)
    clf2 = k_meansCluster(ticker, inputSize=8, binary=False)
    clf3 = svm_class(ticker, inputSize=20, binary=True, risk=0.65)
    clf4 = dt_class(ticker, inputSize=15, binary=False, risk =0.7)
    clf5 = nb_class(ticker)
    clf6 = TensorForceClass(ticker)
    clf7 = gaussProcess_classifier(ticker, inputSize=10, binary=False)
    # clfs = [clf1, clf2, clf3, clf4, clf5, clf6, clf7]
    clfs = [clf4, clf6, clf7]

    clf = majorityVoteClass(ticker,clfs, risk = 0.5)

    preds = []

    # Get Testing Data
    numTestDays = 1

    # Get Training Data
    numTrainDays = 150
    train_end_day = endDay
    # train_end_day = wd.workday(train_end_day,-1)

    # Train Classifier
    clf.clfs[1].trainClf(train_end_day, numTrainDays=1500)
    clf.trainClf(train_end_day, numTrainDays)

    preds.append(clf.predictToday(day=train_end_day))
    # print('Today %s Prediction: %i' %(clf.ticker, preds[-1]))


def fullProcess():
    # tickers = ['tsla', 'aapl', 'noc', 'dis', 'nflx', 'sq', 'fb', 'twtr', 'msft', 'atvi', 'baba', 'lmt', 'ea', 'alv', 'hlt', 'ntdoy', 'sbux', 'de', 'bac']
    # tickers = ['tsla', 'aapl', 'noc', 'dis', 'nflx', 'sq', 'fb', 'twtr', 'msft', 'atvi', 'baba', 'lmt', 'ea', 'alv', 'hlt', 'sbux', 'de', 'bac']
    # tickers = ['ea', 'alv', 'hlt', 'ntdoy', 'sbux', 'de', 'bac']    
    tickers = ['tsla']
    # inFunct = printYesterdayResults
    # inFunct = getTodayPredictions
        
    for ticker in tickers:
        # printYesterdayResults(ticker)
        getTodayPredictions(ticker)



def singleGuessManyDays():
    ticker = 'tsla'
    endDate = date.today()
    # startDate = date(2020,8,5)
    startDate = date(2020,5,1)
    while startDate <= endDate:
        print(startDate)
        getTodayPredictions(ticker, startDate)
        startDate = wd.workday(startDate, 1)


# singleGuessManyDays()
fullProcess()