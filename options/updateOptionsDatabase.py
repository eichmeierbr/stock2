#!/usr/bin/python
import multiprocessing
import numpy as np
import json
from optionsScanner import OptionScannerParams, getOptions, getAllTickers, getTradingDayString
from multiprocessing import Process, Value

import os


def cleanStaleData(ticker, printDebug=False):
    alreadyUpdated = False
    dayString = getTradingDayString()

    updatedFileName = f"{ticker}_{dayString}.json"
    fileNames = [f for f in os.listdir("options/data/") if os.path.isfile(os.path.join("options/data/", f))]

    for file in fileNames:
        fileTicker = file.split('_')[0]
        if file == updatedFileName:
            if printDebug:
                print(f"{ticker} already up to date")
            return True
        elif fileTicker == ticker:
            os.remove("options/data/" + file)
            if printDebug:
                print(f"Removed Stale Ticker: {ticker}")
            return False

    
    return alreadyUpdated


def downloadOption(ticker, api_calls_value, printDebug=False):
    params = OptionScannerParams()
    params.setMaxOptionsAway(20)

    dayString = getTradingDayString()

    if dayString == None:
        quit()

    options, live_price, api_calls = getOptions(ticker, params.endDate, delay=np.random.uniform(0.5,1.5))
    api_calls_value.value = api_calls
    
    if options is not None:
        out = {'option_chain':options, 'stock':ticker, 'day':dayString, 'live_price':live_price}
        # options["stock"] = ticker
        # options["day"] = dayString
        # options["live_price"] = live_price
        json_object = json.dumps(out)


        with open(f"options/data/{ticker}_{dayString}.json", "w") as outfile:
            outfile.write(json_object)
    else:
        api_calls_value.value = 1
        with open(f"options/data/empty-options_{dayString}.txt", "a") as emptyFile:
            emptyFile.write(f"{ticker}\n")

            

def downloadProcessManager(ticker, attempts=3, printDebug=False):
    for i in range(attempts):
        if printDebug:
            print(f"Updating {ticker}")
        api_calls_value = Value('i', -1)
        p = Process(target=downloadOption, args=(ticker, api_calls_value, printDebug))
        p.start()
        p.join(10)
        p.terminate()

        if api_calls_value.value > 0:
            return api_calls_value.value * (i+1)

        if printDebug:
            print("API call froze. Trying again")
    return attempts*5


def getEmptyTickers():
    empty_tickers = []
    yesterday_empty_tickers = []
    fileNames = ["options/data/" + f for f in os.listdir("options/data/") if os.path.isfile(os.path.join("options/data/", f)) if f.startswith('empty-options')]

    todayString = getTradingDayString()
    yesterdayString = getTradingDayString(1)

    # Load Today's Empty File
    if f"options/data/empty-options_{todayString}.txt" in fileNames:
        with open(f"options/data/empty-options_{todayString}.txt", "r") as emptyFile:
            empty_tickers = emptyFile.readlines()
        empty_tickers = [tick[:-1] for tick in empty_tickers]

    # Load Yesterday's Empty File
    if f"options/data/empty-options_{yesterdayString}.txt" in fileNames:
        with open(f"options/data/empty-options_{yesterdayString}.txt", "r") as emptyFile:
            yesterday_empty_tickers = emptyFile.readlines()
        yesterday_empty_tickers = [tick[:-1] for tick in yesterday_empty_tickers]

    [yesterday_empty_tickers.remove(f) for f in empty_tickers if f in yesterday_empty_tickers]


    # Remove Old Empty Files
    for file in fileNames:
        fileDate = file.split('_')[-1][:-4]
        if fileDate not in [todayString, yesterdayString]:
            os.remove(file)
    return empty_tickers, yesterday_empty_tickers

# Limited to 2000 Requests per hour

def getTickerData():
    all_tickers = getAllTickers('sp500') + getAllTickers('nasdaq')
    empty_tickers, yesterday_empty_tickers = getEmptyTickers() 

    # Remove Already scanned empty tickers
    [all_tickers.remove(f) for f in empty_tickers if f in all_tickers]

    # Push yesterdays empty tickers to back
    [all_tickers.append(all_tickers.pop(all_tickers.index(tick))) for tick in yesterday_empty_tickers if tick in all_tickers]

    # Remove .B tickers
    [all_tickers.remove(f) for f in all_tickers if '.' in f]
    return all_tickers

if __name__ == "__main__":
    call_total = 0
    max_calls = 1500

    all_tickers = getTickerData() 

    # all_tickers = ['GME', 'AAPL', 'TSLA', 'BBBY']
    # all_tickers = ['GME']
    # empty_tickers = []

    cleanStaleData(all_tickers, printDebug=False)

    for ticker in all_tickers:
        if not cleanStaleData(ticker, printDebug=False):
            call_total += downloadProcessManager(ticker, 3, True)
            # call_total += downloadOption(ticker, printDebug=True)
        
        if call_total > max_calls:
            break
    print(f"Total API Calls: {call_total}")
