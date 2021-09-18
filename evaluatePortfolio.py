from datetime import date, timedelta
import workdays as wd
import numpy as np
import stock_market as sm
import matplotlib.pyplot as plt
import yfinance as yf


def plotGains(portfolio, total=True, individual=True):

    if individual:
        for stock in portfolio:
            if len(stock[2]) > 0 and not stock[0] == 'total':
                plt.plot(stock[2], label=stock[0])
        plt.pause(0.001)
        plt.xlabel('Days')
        plt.ylabel('Yield')
        plt.title('Individual Stock Performance')
        plt.legend()

    if total:
        plt.figure(2)
        
        for stock in portfolio:
            if len(stock[2]) > 0 and stock[0] == 'total':
                plt.plot(stock[2], label=stock[0])
    
        plt.xlabel('Days')
        plt.ylabel('Yield')
        plt.title('Total Portfolio Performance')

    if total or individual:
        plt.show()


def getHoldGains(ticker, startDate, endDate):
    
    numDays =wd.networkdays(startDate, endDate)

    stock = yf.Ticker(ticker)
    his = stock.history(start=startDate, end=endDate, period = '1d', interval='1d')
    data = his.Open
    data=data/data[0]
    return data.values.tolist()


def getCumulativeGain(portfolio, normalize=True):
    totalGain = []
    principal = 0

    for stock in portfolio:
        totalGain.append(stock[2])
    totalGain = np.array(totalGain)

    for i in range(len(portfolio)):
        principal += portfolio[i][1]
        totalGain[i] *= portfolio[i][1]
    
    totalGain = np.sum(totalGain, axis=0)
    totalGain /= principal
    return ['total', principal, list(totalGain)]


def evaluatePortfolio(portfolio, startDate, end_date, normalize):
    # Get hold gains
    holdGains = []
    for stock in portfolio:
        stock.append(getHoldGains(stock[0],startDate,end_date))

    # Get cumulative gain
    portfolio.append(getCumulativeGain(portfolio, normalize=normalize))

    # Report Results
    scale=1
    if normalize:
        scale = portfolio[-1][1]
    finalReturn = portfolio[-1][-1][-1] * scale
    print("Principal: %.2f" %(portfolio[-1][1]))
    print("Final Return: %.2f" %(finalReturn))
    

    plotGains(portfolio)



if __name__ == '__main__':
    portfolio = [['aapl',1],
                 ['tsla',1]]
    normalize = True

    # Get Testing Start Data
    numTestDays = 1
    year = 2020
    month = 1
    day = 1
    startDate = date(year,month,day)

    # Get End Day
    if year == 2021: end_date = date.today()
    else: 
        endYear = year + 1
        end_month = 1
        end_day = 1
        end_date = date(endYear, end_month, end_day)

    evaluatePortfolio(portfolio, startDate, end_date, normalize)


