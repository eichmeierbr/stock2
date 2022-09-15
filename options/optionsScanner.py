import multiprocessing
import yfinance as yf
import numpy as np
import requests
from datetime import timedelta, datetime
from datetime import time as dt_time
import os
import csv

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
        self.minReturn = 5
        self.numExpireDates = 4
        self.today = np.datetime64('today', 'D')
        self.endDate = datetime.today() + timedelta(days=self.maxOptionsAway)

    def setMaxOptionsAway(self, maxOptions):
        self.maxOptionsAway = maxOptions
        self.endDate = datetime.today() + timedelta(days=self.maxOptionsAway)


def isNowInTimePeriod(startTime, endTime, nowTime): 
    if startTime < endTime: 
        return nowTime >= startTime and nowTime <= endTime 
    else: 
        #Over midnight: 
        return nowTime >= startTime or nowTime <= endTime 

def getTradingDayString(dayDelta=0):
    day = (datetime.today()-timedelta(days=dayDelta)).date()
    if day.isoweekday() == 7:
        return str(day-timedelta(days=2))
    elif day.isoweekday() == 6:
        return str(day-timedelta(days=1))
    elif isNowInTimePeriod(dt_time(14,30), dt_time(0,0), datetime.now().time()):
        return str(day)
    elif isNowInTimePeriod(dt_time(0,0), dt_time(7,30), datetime.now().time()):
        return str(day-timedelta(days=1))
    else:
        return None

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

def getOptions(ticker, endDate=None, delay=0):
    api_calls = 0
    r = getOptionOnExpiration(ticker, endDate=endDate)
    api_calls += 1
    if r == None:
        return r, -1, -1
    
    expirations = r['expirationDates']
    options = {}
    firstDate = datetime.utcfromtimestamp(expirations[0]).strftime('%Y-%m-%d')
    options[firstDate] = saveOptionsOnDate(r)
    live_price = r['quote']['regularMarketPrice']

    for date in expirations[1:]:
        time.sleep(delay)
        thisDate = datetime.utcfromtimestamp(date).strftime('%Y-%m-%d')
        opts = getOptionOnExpiration(ticker, date, endDate)
        api_calls += 1

        if opts == None:
            return options, live_price, api_calls

        options[thisDate] = saveOptionsOnDate(opts)
    
    return options, live_price, api_calls

def loadOptions(ticker, endDate):
    option_chain = 0
    live_price = 0
    day = getTradingDayString()
    with open(f"options/data/{ticker}_{getTradingDayString()}.json", 'r') as f:
        data = json.load(f)
    return data['option_chain'], data['live_price'], 0
    # raise Exception('Option not found')


def evaluateOption(params, live_price, ticker, date, option):
    lastTradedDay = np.datetime64(datetime.utcfromtimestamp(option['lastTradeDate']).strftime('%Y-%m-%d'))
    daysSinceLastTrade = np.timedelta64(params.today - lastTradedDay) / np.timedelta64(1, 'D')

    # openInterest = option[9]

    noExerciseReturn = (option['bid'] - params.commish)/live_price * 100
    exerciseReturn = (option['bid'] + option['strike'] - live_price - params.commish)/live_price * 100

    if daysSinceLastTrade < params.maxDaysSinceLastTrade : # and option[8] > params.minVolume:
        if np.min([noExerciseReturn, exerciseReturn]) > params.minReturn:
            # print('Tick: %s, Date: %s, Price: %.2f, Strike %.2f, No: %.2f%%, Exc: %.2f%%, Bid: $%.2f' %(ticker, date, live_price, option['strike'], noExerciseReturn, exerciseReturn, option['bid']))
            out = [ticker, date, live_price, option['strike'], np.round(noExerciseReturn,2), np.round(exerciseReturn,2), np.round(np.min([noExerciseReturn, exerciseReturn]), 2), option['bid']]
            return out
    return []


def analyzeOptions(params, downloadOption, ticker):
    goodOptions = []


    try:
        if downloadOption:
            option_chain, live_price, _ = getOptions(ticker, params.endDate)
        else:
            option_chain, live_price, _ = loadOptions(ticker, params.endDate)

        if len(option_chain) == 0:
            return []

        # print('Scanning stock: ', ticker)

        for date in option_chain:
            for option in option_chain[date]['calls']:
                goodOptions.append(evaluateOption(params, live_price, ticker, date, option))

    except:
        return [x for x in goodOptions if len(x)>0 ]
    return [x for x in goodOptions if len(x)>0 ]
        

def findGoodOptions(tickers, params, downloadOption):
    good_options_pre = list(map(partial(analyzeOptions, params, downloadOption), tickers))


    # n_worker = multiprocessing.cpu_count()
    # # pool = multiprocessing.Pool(n_worker)
    # pool = multiprocessing.Pool(1)
    # functi = partial(analyzeOptions, params, downloadOption)
    # good_options = pool.map(functi, tickers)    
    # pool.close()
    # pool.join()

    good_options_pre = [opt for opt in good_options_pre if len(opt) > 0]

    good_options = []
    for option in good_options_pre:
        good_options = good_options + [opt for opt in option]
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

def getTickersWithData():
    fileNames = [f for f in os.listdir("options/data/") if os.path.isfile(os.path.join("options/data/", f))]
    fileNames.sort()
    
    tickers = [tick.split('_')[0] for tick in fileNames if tick.endswith('json')]
    return tickers

def saveToCsv(options):
    headers = ['Ticker', 'Expiration', 'Current Price', 'Strike', 'No Exercise %gain', 'Exercise %gain', 'Min Gain', 'Bid']
    with open("out.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(options)

if __name__ == "__main__":
    params = OptionScannerParams()
    all_tickers = getTickersWithData()
    # all_tickers = getAllTickers('nasdaq')
    # all_tickers = ['GME', 'AAPL', 'TSLA', 'BBBY']
    # all_tickers = ['GME']

    start = time.time()
    print("Starting Options Scan")

    goodOptions = findGoodOptions(all_tickers, params, False)

    for opt in goodOptions:
        print(opt)
    
    saveToCsv(goodOptions)


    print('Finished')
    print("Time Elapsed: ", time.time() - start)