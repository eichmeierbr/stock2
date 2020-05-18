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

ticker = 'tsla'

# clf = kDayMean(ticker, days=3)
clf1 = knn_classifier(ticker, inputSize=8, binary=True, n_neighbors=3, risk = 0.5)
clf2 = k_meansCluster(ticker, inputSize=8, binary=False)
clf3 = svm_class(ticker, inputSize=20, binary=True, risk=0.65)
clf4 = dt_class(ticker, inputSize=15, binary=False, risk =0.7)
clf5 = nb_class(ticker)
clf6 = TensorForceClass(ticker)
clf7 = gaussProcess_classifier(ticker, inputSize=10, binary=False)
clfs = [clf1, clf2, clf3, clf4, clf5, clf6, clf7]

clf = majorityVoteClass(ticker,clfs, risk = 0.5)



# Get Testing Data
numTestDays = 1
year = 2020
month = 1
day = 1
# endDay = date(year,month,day)
endDay = date.today()

# Get Training Data
numTrainDays = 150
train_end_day = wd.workday(endDay,-numTestDays-clf.inputSize) 

# Train Classifier
clf.clfs[5].trainClf(train_end_day, numTrainDays=1500)
clf.trainClf(train_end_day, numTrainDays)

# sm.dayPrices(ticker)
print('Today %s Prediction: %i' %(clf.ticker, clf.predictToday()))


gain, conf_mat = sm.evaluateClassifierBinary(clf, numTestDays, endDay, which='Open')

totalGain = 1
for val in gain:
    totalGain *= (1 + val/100)

print('Gain = %.2f' %(totalGain))
# print('Correct = %.2f' %(conf_mat[-1,-1] + conf_mat[0,0]))
print(conf_mat)