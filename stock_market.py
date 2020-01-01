import yfinance as yf
from datetime import date, timedelta



def prices(ticker, which = 'Open', startDay=date.today(), endDay=date.today()-timedelta(150)):
    stock = yf.Ticker(ticker)
    his = stock.history(start=startDay, end=endDay, period = '1d')
    if which=='Open':
        return his.Open.real.tolist()
    elif which=='Close':
        return his.Close.real.tolist()
    elif which == 'Low':
        return his.Low.real.tolist()
    else:
        return his.High.real.tolist()


def dayDiff(ticker, startDay=date.today()-timedelta(150),  endDay=date.today()):
    stock = yf.Ticker(ticker)
    his = stock.history(start=startDay, end=endDay, period = '1d')
    diff = his.Close - his.Open
    return diff.real  



def dayDiffBinary(ticker, startDay=date.today()-timedelta(150),  endDay=date.today()):
    diff = dayDiff(ticker,startDay,endDay)
    for i in range(0,len(diff)):
        if diff[i]>0:
            diff[i] = 1
        else:
            diff[i] = 0
    return diff


def dayDiffPercent(ticker, startDay=date.today()-timedelta(150),  endDay=date.today()):
    stock = yf.Ticker(ticker)
    his = stock.history(start=startDay, end=endDay, period = '1d')
    diff = (his.Close - his.Open)/his.Open*100
    return diff.real  



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
    

print dayDiffBinary('aapl')