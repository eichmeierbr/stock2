import multiprocessing
import yfinance as yf
import numpy as np
import requests
from datetime import timedelta, datetime


import time
import json
from functools import partial
import pandas as pd

class OptionScannerParams:
    def __init__(self):
        self.commission = 0.65
        self.commish = self.commission/100
        self.minVolume = 50
        self.maxDaysSinceLastTrade = 4
        self.maxOptionsAway = 30
        self.minReturn = 7.5
        self.numExpireDates = 4
        self.today = np.datetime64('today', 'D')
        self.endDate = datetime.today() + timedelta(days=self.maxOptionsAway)



def getOptionOnExpiration(ticker, date=None, endDate=None):
    if not date == None and not endDate == None:
        optDate = datetime.utcfromtimestamp(date)
        if optDate > endDate:
            return None

    try:
        url = 'https://query2.finance.yahoo.com/v7/finance/options/' + ticker.lower()
        if not date == None:
            url += '?date={}'.format(date)
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(
            url=url,
            headers=headers).json()

        optDate = datetime.utcfromtimestamp(r['optionChain']['result'][0]['expirationDates'][0])
        if optDate > endDate:
            return None
        return r['optionChain']['result'][0]
    except:
        return None

def saveOptionsOnDate(req):
    return  {'calls': req['options'][0]['calls'], 
                'puts': req['options'][0]['puts']}

def getOptions(ticker, endDate=None):
    r = getOptionOnExpiration(ticker, endDate=endDate)
    live_price = - 1
    if r == None:
        return r, live_price
    
    expirations = r['expirationDates']
    options = {}
    firstDate = datetime.utcfromtimestamp(expirations[0]).strftime('%Y-%m-%d')
    options[firstDate] = saveOptionsOnDate(r)
    live_price = r['quote']['regularMarketPrice']

    for date in expirations[1:]:
        thisDate = datetime.utcfromtimestamp(date).strftime('%Y-%m-%d')
        opts = getOptionOnExpiration(ticker, date, endDate)

        if opts == None:
            return options, live_price

        options[thisDate] = saveOptionsOnDate(opts)
    
    return options, live_price



def evaluateOption(params, live_price, ticker, date, option):
    lastTradedDay = np.datetime64(datetime.utcfromtimestamp(option['lastTradeDate']).strftime('%Y-%m-%d'))
    daysSinceLastTrade = np.timedelta64(params.today - lastTradedDay) / np.timedelta64(1, 'D')

    # openInterest = option[9]

    noExerciseReturn = (option['bid'] - params.commish)/live_price * 100
    exerciseReturn = (option['bid'] + option['strike'] - live_price - params.commish)/live_price * 100

    if daysSinceLastTrade < params.maxDaysSinceLastTrade : # and option[8] > params.minVolume:
        if np.min([noExerciseReturn, exerciseReturn]) > params.minReturn:
            print('Tick: %s, Date: %s, Price: %.2f, Strike %.2f, No: %.2f%%, Exc: %.2f%%' %(ticker, date, live_price, option['strike'], noExerciseReturn, exerciseReturn))
            return [ticker, date, live_price, option[2], np.round(noExerciseReturn,2), np.round(exerciseReturn,2)]
    return []

def analyzeOptions(params, ticker):
    goodOptions = []

    try:
        option_chain, live_price = getOptions(ticker, params.endDate)

        a = 3
        if len(option_chain) == 0:
            return []

        print('Scanning stock: ', ticker)

        for date in option_chain:
            for option in option_chain[date]['calls']:
                goodOptions.append(evaluateOption(params, live_price, ticker, date, option))

    except:
        return [x for x in goodOptions if len(x)>0 ]
    return [x for x in goodOptions if len(x)>0 ]
        

def findGoodOptions(tickers, params):
    # good_options = list(map(partial(analyzeOptions, params), all_tickers))


    n_worker = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(n_worker)
    # pool = multiprocessing.Pool(1)
    functi = partial(analyzeOptions, params)
    good_options = pool.map(functi, tickers)    
    pool.close()
    pool.join()

    return good_options



def getAllTickers(universe='nasdaq'):
    if universe == 'sp500':
        table=pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
        spy =  list(table[0]['Symbol'])
        spy.sort()
        return spy
    else:
        url='https://api.nasdaq.com/api/screener/stocks?tableonly=true&limit=25&offset=0&download=true'
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        js = json.loads(response.content)

        stock_data = js['data']['rows']
        return [stock['symbol'] for stock in stock_data if "/" not in stock['symbol'] and "^" not in stock['symbol']]


if __name__ == "__main__":
    params = OptionScannerParams()
    # all_tickers = getAllTickers('sp500')
    all_tickers = ['GME', 'AAPL', 'TSLA']
    # all_tickers = ['GME']

    start = time.time()
    print("Starting Options Scan")

    goodOptions = findGoodOptions(all_tickers, params)

    for opts in goodOptions:
        if opts == None or len(opts) == 0:
            continue
        for option in opts:
            print(option)


    print('Finished')
    print("Time Elapsed: ", time.time() - start)