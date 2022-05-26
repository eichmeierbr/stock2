import yfinance as yf
import numpy as np

def analyzeOptions(ticker):
    today = np.datetime64('today', 'D')
    stock = yf.Ticker(ticker)

    commission = 0.65

    live_price = stock.info['currentPrice']
    dates = stock.options

    for date in dates:
        opt = stock.option_chain(date)
        calls = opt.calls

        for _, row in calls.iterrows():
            tradeDaysElapsed = -(row.lastTradeDate - today).days
            commish = commission/100

            openInterest = row.openInterest

            noExerciseReturn = (row.bid - commish)/live_price * 100
            exerciseReturn = (row.bid + row.strike - live_price - commish)/live_price * 100

            if noExerciseReturn > 0 and exerciseReturn > 0 and row.volume > 50 and tradeDaysElapsed < 5 :
                print('Tick: %s, Date: %s, Strike %.2f, No: %.2f%%, Exc: %.2f%%' %(ticker, date, row.strike, noExerciseReturn, exerciseReturn))
            a = 3
        a = 3 

stocks = ['aapl', 'msft']
for tick in stocks:
    analyzeOptions(tick)

a = 23