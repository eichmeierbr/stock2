import sys
sys.path.append('./traders')

from kDayClassifier import *
from knn_classifier import *
from k_meansClass import *
from svm_class import *
from decision_tree_class import *
from naiveBayes_class import *
from majority_vote_class import *
from tensorForceAgent import *
from gaussianProcess_class import *
from nn_class import *


from datetime import date, timedelta
import workdays as wd
import numpy as np
import stock_market as sm
import matplotlib.pyplot as plt
import yfinance as yf


def plotGains(gains,clf, year, holdGains=[], save=False):
    plt.plot(gains, 'b-')
    if len(holdGains) > 0:
        plt.plot(holdGains, 'r--')
    plt.pause(0.001)
    plt.title('%s: %s, Year: %i' %(clf.type,clf.ticker,year))
    plt.xlabel('Days')
    plt.ylabel('Yield')
    plt.legend(['Clf', 'Stock'])
    if save:
        plt.savefig('results/%s-%s_Year-%i.png' %(clf.type,clf.ticker,year))
        plt.clf()
    else:
        plt.show()
        plt.clf()


def getHoldGains(ticker, startDate, endDate):
    
    numDays =wd.networkdays(startDate, endDate)

    stock = yf.Ticker(ticker)
    his = stock.history(start=startDate, end=endDate, period = '1d', interval='1d')
    data2 = his.Open.values.tolist()[-numDays:]
    data_f = data2[0]
    for i in range(len(data2)):
        data2[i] = (data2[i]-data_f)/data_f + 1
    return data2



def checkIfDateHasPrice(ticker, date):
    stock = yf.Ticker(ticker)
    numDays = 2
    his = stock.history(start=date, end=wd.workday(date,numDays), period = '1d', interval='1d')

    try:
        dates = his.Open.index.date
    except:
        return False
    return numDays == len(dates)

        


def evaluateTimePeriod(ticker, testDate, end_date):
    # clf = kDayMean(ticker, days=3)
    # clf1 = knn_classifier(ticker, inputSize=12, binary=False, n_neighbors=3, risk = 0.5, adaboost=True)  ### GOOD ON SOME
    # clf2 = k_meansCluster(ticker, inputSize=15, binary=False, adaboost=True)                           ##### BAD
    # clf3 = svm_class(ticker, inputSize=10, binary=True, risk=0.6, adaboost=True)                      ################# This is good... on some!
    # clf4 = dt_class(ticker, inputSize=15, binary=True, risk =0.7, adaboost=True)
    # clf5 = nb_class(ticker,inputSize=20, risk=0.5, adaboost=True)
    # clf6 = TensorForceClass(ticker)
    # clf6.trainClf(testDate, numTrainDays=1500)
    clf7 = gaussProcess_classifier(ticker, inputSize=10, binary=True, adaboost=True)
    # clf8 = adaboost_classifier(ticker, inputSize=12, binary=False, n_neighbors=3, risk = 0.5)
    # clf9 = nn_class(ticker, inputSize=20, binary=False, risk=0.6, adaboost=False, layers=(20,20), act_func='logistic', solver='sgd')
    clf10 = nn_class(ticker, inputSize=20, binary=False, risk=0.6, adaboost=False, layers=(20,20), act_func='tanh', solver='sgd')
    clf11 = nn_class(ticker, inputSize=10, binary=False, risk=0.5, adaboost=False, layers=(80,30,20,20), act_func='tanh', solver='sgd')
    # clf12 = nn_class(ticker, inputSize=30, binary=False, risk=0.6, adaboost=False, layers=(40,20), act_func='tanh', solver='sgd')
    # clfs = [clf1, clf2, clf3, clf4, clf5, clf7]
    # clfs = [clf3, clf1, clf6, clf9]
    clfs = [clf11, clf7, clf10]
    # clfs = [clf9, clf10,clf11,clf12, clf6]
    
  
    clf = majorityVoteClass(ticker,clfs, risk = 0.5)
    # clf = clf7
# 

    # Train Classifier
    numTrainDays = 200
    totalGain = 1.0
    allGains = [totalGain]
    totalConf = np.zeros([2,2])
    iters = 0

    clf.trainClf(testDate, numTrainDays)

    plt.ion()
    month = testDate.month

    # Predict Today's Outcome
    firstDate = testDate
    holdGains = getHoldGains(ticker,firstDate,end_date)

    while testDate < end_date:
        # Make Prediction
        if testDate.month > month:
            clf.trainClf(testDate, numTrainDays)
            month += 1
        if checkIfDateHasPrice(ticker, testDate):
            gain, conf_mat, actions = sm.evaluateClassifierBinary(clf, numTestDays, testDate, which='Open')
            # Update Gain and Conf
            totalGain *= (1 + np.sum(gain)/100)
            allGains.append(totalGain)
            # plotGains(allGains, clf, year)
            totalConf += conf_mat
            iters+=1
        # Increment Day
        testDate = wd.workday(testDate,1)


    # print('Today %s Prediction: %i' %(clf.ticker, clf.predictToday()))
    print('Hold Gain = %.2f' %(holdGains[-1]))
    print('Gain = %.2f' %(np.sum(totalGain)))
    print('Confusion Matrix:')
    print('\t  V,   ^')
    print('No Buy\t' + str(np.round(totalConf[0]/iters,2)))
    print('Buy\t' + str(np.round(totalConf[1]/iters,2)))
    startPrice = sm.dayPrices(ticker,numDays=1, endDay=firstDate)

    plt.ioff()
    plotGains(allGains,clf, year, holdGains, save=False)



ticker = 'f'

# Get Testing Start Data
numTestDays = 1
year = 2021
month = 4
day = 1
testDate = date(year,month,day)

# Get End Day
if year == 2021: end_date = date.today()
else: 
    endYear = year + 1
    end_month = 1
    end_day = 1
    end_date = date(endYear, end_month, end_day)


end_date = date.today()
evaluateTimePeriod(ticker,testDate,end_date)