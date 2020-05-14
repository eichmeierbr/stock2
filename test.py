from kDayClassifier import *
from knn_classifier import *
from k_meansClass import *
from svm_class import *
from decision_tree_class import *
from naiveBayes_class import *
from majority_vote_class import *

from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import VotingClassifier

from datetime import date, timedelta
import workdays as wd
import numpy as np
import stock_market as sm

ticker = 'sq'

# clf = kDayMean(ticker, days=3)
clf1 = knn_classifier(ticker, inputSize=8, binary=True, n_neighbors=3, risk = 0.5)
clf2 = k_meansCluster(ticker, inputSize=8, binary=False)
clf3 = svm_class(ticker, binary=True, risk=0.55)
clf4 = dt_class(ticker, inputSize=10, binary=True, risk =0.7)
clf5 = nb_class(ticker)
clfs = [clf1, clf2, clf3, clf4, clf5]

clf = majorityVoteClass(ticker,clfs, risk = 0.5)

# Get Testing Data
numTestDays = 60
year = 2020
month = 5
day =  11
# endDay = date.today()
endDay = date(year,month,day)


# Get Training Data
numTrainDays = 150
train_end_day = wd.workday(endDay,-numTestDays-clf.inputSize) 

# Train Classifier
clf.trainClf(train_end_day, numTrainDays)

# sm.dayPrices(ticker)
gain, conf_mat = sm.evaluateClassifierBinary(clf, numTestDays, endDay, which='Open')
print('Gain = %.2f' %(gain))
print('Correct = %.2f' %(conf_mat[-1,-1] + conf_mat[0,0]))