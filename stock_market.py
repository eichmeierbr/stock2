import yfinance as yf
from datetime import date, timedelta



def prices(ticker, which = 'Open', per = '1d', startDay=date.today(), endDay=date.today()-timedelta(150)):
    stock = yf.Ticker(ticker)
    his = stock.history(start=startDay, end=endDay, period = per)
    if which=='Open':
        return his.Open.real.tolist()
    elif which=='Close':
        return his.Close.real.tolist()
    elif which == 'Low':
        return his.Low.real.tolist()
    else:
        return his.High.real.tolist()


##################################################################################################################
##########################################     Single Day Functions      #########################################

# These functions return the differece in prices for a stock within a single day

# Inputs:
## ticker: Ticker identifier for the desired stock
## startDay: First day of the desired stock range as a datetime.date object
## endDay: Final day of the desired stock range as a datetime.date object

# Output: A single array of stock price differences


def openToCloseDiff(ticker, startDay=date.today()-timedelta(150),  endDay=date.today()):
    stock = yf.Ticker(ticker)
    his = stock.history(start=startDay, end=endDay, period = '1d')
    diff = his.Close - his.Open
    return diff.real  



def openToCloseDiffBinary(ticker, startDay=date.today()-timedelta(150),  endDay=date.today()):
    diff = openToCloseDiff(ticker,startDay,endDay)
    for i in range(0,len(diff)):
        if diff[i]>0:
            diff[i] = 1
        else:
            diff[i] = 0
    return diff


def openToCloseDiffPercent(ticker, startDay=date.today()-timedelta(150),  endDay=date.today()):
    stock = yf.Ticker(ticker)
    his = stock.history(start=startDay, end=endDay, period = '1d')
    diff = (his.Close - his.Open)/his.Open*100
    return diff.real  


##########################################     Single Day Functions      #########################################
##################################################################################################################


##################################################################################################################
##########################################     Day To Day Functions      #########################################

# These functions return the differece in prices for a stock within a single day

# Inputs:
## ticker: Ticker identifier for the desired stock
## startDay: First day of the desired stock range as a datetime.date object
## endDay: Final day of the desired stock range as a datetime.date object
## which: Select price category ('Open', 'Close', 'High', 'Low'). Default is 'Open'

# Output: A single array of stock price differences


def dayToDayDiff(ticker, which = 'Open', startDay=date.today()-timedelta(150),  endDay=date.today()):
    data = prices(ticker, which, startDay, endDay)
    for i in range(0,len(data) - 1):
        data[i] = data[i+1] - data[i]
    return data[:-1]


def dayToDayDiffPercent(ticker, which = 'Open', startDay=date.today()-timedelta(150),  endDay=date.today()):
    data = prices(ticker, which, startDay, endDay)
    for i in range(0,len(data) - 1):
        data[i] = (data[i+1] - data[i])/data[i]*100
    return data[:-1]

##########################################     Day To Day Functions      #########################################
##################################################################################################################


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
    

print dayToDayDiff('aapl')