from datetime import date, datetime
import yfinance as yf
import os.path
import pandas as pd
import workdays as wd
import numpy as np
import csv

class Ticker_history:
    def __init__(self, ticker, interval, start_day=date(1900,1,1)):
        self.period = self.verify_interval(interval)
        self.ticker = ticker
        self.interval = interval
        self.start_day = start_day
        self.data = []
        self.now_data = []
        self.history = []
        self.future = []
        self.headers = None

        if interval in ['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h']:
            self.end_day = wd.workday(self.start_day, 5)
        else:
            self.end_day = date.today()

        self.get_daily_stock_data()
        pass

    ## Need to figure out how to get granular data before 1 month. YF only supports last 30 days of intraday data
    # def download_day_stock_data(self):
    #     if not self.interval in ['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h']:
    #         print('Given interval is not intra-day. Changing to 15m')
    #         self.interval = '15m'
    #         self.end_day = wd.workday(self.start_day,5)
        
    #     ## Download data. Add header. Save file
        
    #     pass

    def load_updated_csv(self):
        path_prefix = 'data/'
        file_name = path_prefix + self.ticker + '_' + '1d' + '.csv'

        with open(file_name, newline='') as csvfile:
            # reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            # for idx, row in enumerate(reader):
            #     if idx is 0:
            #         self.headers = row
            #     else:
            #         row[0] = datetime.date(datetime.strptime(row[0], '%Y-%m-%d'))
            #         for i in range(1,len(row)):
            #             row[i] = float(row[i])
            #         self.data.append(row)
            # self.data = np.array(self.data)


            file = np.loadtxt(csvfile, dtype=str, delimiter=',')
            self.headers = list(file[0])    

            ## Extract and convert dates
            dates = [datetime.date(datetime.strptime(day, '%Y-%m-%d')) for day in file[1:,0]]
            dates = np.array(dates).reshape([-1,1])

            ## Convert numbers
            nums = file[1:,1:].astype(np.float)

            ## Convert dates and data
            self.data = np.hstack((dates,nums))
            return self.data
                 
    def get_daily_stock_data(self):
        self.update_daily_stock_data()

        return self.load_updated_csv()

    def update_daily_stock_data(self):
        path_prefix = 'data/'
        file_name = path_prefix + self.ticker + '_' + '1d' + '.csv'
        exists = False
        if not os.path.isfile(file_name): 
            start = date(1900,1,1)
        else:
            data = pd.read_csv(file_name)
            last_day = data['Date'].iloc[-1]
            ld = date.fromisoformat(last_day)
            start = wd.workday(ld, 1)
            exists = True

        ## Check if we're up to date
        if wd.workday(wd.workday(start,-1),1) > date.today() or wd.workday(wd.workday(start,1),-1) < date.today() and exists:
            return


        t = yf.Ticker(self.ticker)
        h = t.history(start=start, end=date.today(), interval='1d')

        ## Lines for Backtrader format
        # h =  h.drop("Dividends", 1)
        # h =  h.drop("Stock Splits", 1)
        # h['Adj Close'] = h['Close']
        # h = h[['Open','High','Low','Close','Adj Close', 'Volume']]

        ## If the file dowsn't exist, just save all the data
        if not os.path.isfile(file_name): 
            h.to_csv(file_name)
        else: ## Append the new data to the old data and resave
            h.to_csv('temp'+'.csv')
            data2 = pd.read_csv('temp.csv')
            os.remove('temp.csv')

            self.data = pd.concat([data,data2], axis=0)
            self.data.to_csv(file_name, index=False)


    def verify_interval(self, interval):
        valid_intervals = ['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo']
        try:
            assert(interval in valid_intervals)
        except:
            print('Interval %s not available, defaulting to 1d' %(interval))
            interval = '1d'
        return interval

    def set_start_day(self, day):
        self.history = self.data[self.data[:,0] <= day]
        self.future = self.data[self.data[:,0] > day]
        self.start_day = day
        self.now_data = self.history[-1]
        a=3

    def advance_time(self):
        self.history = np.vstack((self.history, self.future[0]))
        self.now_data = self.history[-1]
        self.future = self.future[1:]


if __name__ == "__main__":
    interval = '1d'
    # ticker = 'aapl'
    # test = Ticker_history(ticker, interval)

    tickers = ['f']

    for tick in tickers:
        ticker = Ticker_history(tick, interval=interval)
        ticker.download_daily_stock_data()
        # ticker.download_day_stock_data()