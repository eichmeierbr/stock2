from kDayClassifier import *
from knn_classifier import *
from datetime import date, timedelta
import workdays as wd
import numpy as np
import stock_market as sm

# clf = kDayMean('aapl', days=3)
clf = knn_classifier('aapl', inputSize=8, binary=False, n_neighbors=3)

# Get Testing Data
numTestDays = 200
year = 2020
month = 5
day =  11
# endDay = date.today()
endDay = date(year,month,day)


# Get Training Data
numTrainDays = 150
train_end_day = wd.workday(endDay,-numTestDays) 
inputSize = clf.inputSize
numDays = clf.days+numTrainDays
data = np.array(sm.dayToDayDiffPercent(clf.ticker,which='Open', numDays = numDays, endDay = train_end_day))

X, Y = sm.array2dataset(data, inputSize)
if clf.binary: Y = (np.array(Y) > 0)*1


# Train Classifier
clf.train(X,Y)

# sm.dayPrices('aapl')
gain, conf_mat = sm.evaluateClassifierBinary(clf, numTestDays, endDay, which='Open')
print('Gain = %.2f' %(gain))
print('Correct = %.2f' %(conf_mat[-1,-1] + conf_mat[0,0]))