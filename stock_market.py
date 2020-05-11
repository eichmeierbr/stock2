import yfinance as yf
from datetime import date, timedelta
import workdays as wd
import numpy as np


##################################################################################################################
##########################################     Get Prices Functions      #########################################

# Retreive array of stock prices. 

def dayPrices(ticker, which = 'Open', per = '1d', inter= '1d', numDays = 100, endDay=date.today()):
    startDay = getStartDay(endDay, numDays)

    stock = yf.Ticker(ticker)
    his = stock.history(start=startDay, end=endDay, period = per, interval=inter)
    if which=='Open':
        vals = his.Open.values.tolist()[-numDays:]
    elif which=='Close':
        vals = his.Close.values.tolist()[-numDays:]
    elif which == 'Low':
        vals = his.Low.values.tolist()[-numDays:]
    else:
        vals = his.High.values.tolist()[-numDays:]
    return [x for x in vals if ~np.isnan(x)]


# Retrieve the live price of a stock up to the last minute.
# The function collects the price at every minute for the 
# day, and returns the most recent value.

def livePrice(ticker, which = 'Open'):
    stock = yf.Ticker(ticker)
    his = stock.history(period = '1d', interval = '1m')
    if which=='Open':
        return his.Open[-1]
    elif which=='Close':
        return his.Close[-1]
    elif which == 'Low':
        return his.Low[-1]
    else:
        return his.High[-1]

def liveMinutePrice(ticker, which = 'Open', per = '5d'):
    stock = yf.Ticker(ticker)
    his = stock.history(period = per, interval = '1m')
    if which=='Open':
        return his.Open.values.tolist()
    elif which=='Close':
        return his.Close.values.tolist()
    elif which == 'Low':
        return his.Low.values.tolist()
    else:
        return his.High.values.tolist()

##########################################     Get Prices Functions      #########################################
##################################################################################################################

##################################################################################################################
##########################################     Single Day Functions      #########################################

# These functions return the differece in prices for a stock within a single day

# Inputs:
## ticker: Ticker identifier for the desired stock
## numDays: Number of desired data points, as an integer
## endDay: Final day of the desired stock range as a datetime.date object

# Output: A single array of stock price differences


def openToCloseDiff(ticker, numDays = 100,  endDay=date.today()):
    startDay = getStartDay(endDay, numDays)

    stock = yf.Ticker(ticker)
    his = stock.history(start=startDay, end=endDay, period = '1d')
    diff = his.Close - his.Open
    return diff.values[-numDays:]



def openToCloseDiffBinary(ticker, numDays = 100,  endDay=date.today()):
    startDay = getStartDay(endDay, numDays)

    diff = openToCloseDiff(ticker,startDay,endDay)
    for i in range(0,len(diff)):
        if diff[i]>0:
            diff[i] = 1
        else:
            diff[i] = 0
    return diff[-numDays:]


def openToCloseDiffPercent(ticker, numDays = 100,  endDay=date.today()):
    startDay = getStartDay(endDay, numDays)

    stock = yf.Ticker(ticker)
    his = stock.history(start=startDay, end=endDay, period = '1d')
    diff = (his.Close - his.Open)/his.Open*100
    return diff.values[-numDays:]


##########################################     Single Day Functions      #########################################
##################################################################################################################


##################################################################################################################
##########################################     Day To Day Functions      #########################################

# These functions return the differece in prices for a stock within a single day

# Inputs:
## ticker: Ticker identifier for the desired stock
## numDays: Number of desired data points, as an integer
## endDay: Final day of the desired stock range as a datetime.date object
## which: Select price category ('Open', 'Close', 'High', 'Low'). Default is 'Open'

# Output: A single array of stock price differences


def dayToDayDiff(ticker, which = 'Open', numDays = 100,  endDay=date.today()):
    data = dayPrices(ticker, which, numDays = numDays+1, endDay = endDay)
    for i in range(0,len(data) - 1):
        data[i] = data[i+1] - data[i]
    return data[:-1]


def dayToDayDiffPercent(ticker, which = 'Open', numDays = 100,  endDay=date.today()):
    data = dayPrices(ticker, which, numDays = numDays+1, endDay = endDay)
    for i in range(0,len(data) - 1):
        data[i] = (data[i+1] - data[i])/data[i]*100
    return data[:-1]

##########################################     Day To Day Functions      #########################################
##################################################################################################################


def getStartDay(endDay, numDays):
    numDays +=  int(numDays/5)
    return wd.workday(endDay,-numDays)    


# def array2dataset(inArray, windowSize):
#     data = []
#     for i in range(0,len(inArray)-windowSize):
#         features = inArray[i:i + windowSize]
#         target = inArray[i+windowSize]
#         data.append([features,target])
#     return data

def array2dataset(inArray, windowSize):
    data = []
    labels = []
    for i in range(0,len(inArray)-windowSize):
        features = inArray[i:i + windowSize]
        target = inArray[i+windowSize]
        data.append(features)
        labels.append(target)
    return data, labels


def evaluateClassifierBinary(classifier, numDaysOrig, endDay, which='Open'):
    inputSize = classifier.inputSize
    numDays = classifier.days+numDaysOrig
    data = dayToDayDiffPercent(classifier.ticker,which=which, numDays = numDays, endDay = endDay)

    split_data = array2dataset(data, inputSize)
    actions = []


    # Find the percent difference over the training period
    actions = classifier.predict(split_data[0])    
    percentDiff = 0
    conf_mat = np.zeros([2,2])
    for pred, true in zip(actions, split_data[1]):

        pred_bin = (pred>0)*1
        true_bin = (true>0)*1
        conf_mat[pred_bin, true_bin] += 1
        if pred > 0: percentDiff += true

    return percentDiff, conf_mat/numDaysOrig