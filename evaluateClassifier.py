from kDayClassifier import *
from knn_classifier import *
from k_meansClass import *
from svm_class import *
from decision_tree_class import *
from naiveBayes_class import *
from majority_vote_class import *
from tensorForceAgent import *
from gaussianProcess_class import *


from sklearn.ensemble import RandomForestClassifier

from datetime import date, timedelta
import workdays as wd
import numpy as np
import stock_market as sm
import matplotlib.pyplot as plt

def plotGains(gains,clf, year, save=False):
    plt.plot(gains, 'b-')
    plt.pause(0.001)
    plt.title('%s: %s, Year: %i' %(clf.type,clf.ticker,year))
    plt.xlabel('Days')
    plt.ylabel('Yield')
    if save:
        plt.savefig('results/%s-%s_Year-%i.png' %(clf.type,clf.ticker,year))
        plt.clf()
    else:
        plt.show()
        plt.clf()



def evaluateTimePeriod(ticker, testDate, end_date):
    # clf = kDayMean(ticker, days=3)
    clf1 = knn_classifier(ticker, inputSize=8, binary=True, n_neighbors=3, risk = 0.5)
    clf2 = k_meansCluster(ticker, inputSize=8, binary=False)
    clf3 = svm_class(ticker, inputSize=20, binary=True, risk=0.65)
    clf4 = dt_class(ticker, inputSize=15, binary=False, risk =0.7)
    clf5 = nb_class(ticker)
    clf6 = TensorForceClass(ticker)
    clf6.trainClf(testDate, numTrainDays=1500)
    clf7 = gaussProcess_classifier(ticker, inputSize=10, binary=False)
    clfs = [clf1, clf2, clf3, clf4, clf5, clf6, clf7]
    
    clf = majorityVoteClass(ticker,clfs, risk = 0.5)

    # Train Classifier
    numTrainDays = 150
    totalGain = 1.0
    allGains = [totalGain]
    totalConf = np.zeros([2,2])
    iters = 0

    clf.trainClf(testDate, numTrainDays)

    plt.ion()
    month = testDate.month

    # Predict Today's Outcome

    while testDate < end_date:
        # Make Prediction
        if testDate.month > month:
            clf.trainClf(testDate, numTrainDays)
            month += 1
        gain, conf_mat = sm.evaluateClassifierBinary(clf, numTestDays, testDate, which='Open')
        # Update Gain and Conf
        totalGain *= (1 + np.sum(gain)/100)
        allGains.append(totalGain)
        # plotGains(allGains, clf, year)
        totalConf += conf_mat
        # Increment Day
        testDate = wd.workday(testDate,1)
        iters+=1


    print('Today %s Prediction: %i' %(clf.ticker, clf.predictToday()))
    print('Gain = %.2f' %(np.sum(totalGain)))
    print('Confusion Matrix:')
    print(np.round(totalConf/iters,2))

    plt.ioff()
    plotGains(allGains,clf, year, save=True)



ticker = 'sbux'

# Get Testing Start Data
numTestDays = 1
year = 2020
month = 1
day = 1
testDate = date(year,month,day)

# Get End Day
if year == 2020: end_date = date.today()
else: 
    endYear = year + 1
    end_month = 1
    end_day = 1
    end_date = date(endYear, end_month, end_day)

evaluateTimePeriod(ticker,testDate,end_date)