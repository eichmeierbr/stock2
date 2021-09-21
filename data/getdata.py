from datetime import date
import yfinance as yf
import os.path
import pandas as pd
import workdays as wd


class Ticker_history:
    def __init__(self, ticker, interval, start_day=date(1990,1,1)):
        self.period = self.verify_interval(interval)
        self.ticker = ticker
        self.interval = interval
        self.start_day = start_day

        if interval in ['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h']:
            self.end_day = wd.workday(self.start_day, 5)
        else:
            self.end_day = date.today()
        pass

    ## Need to figure out how to get granular data before 1 month. YF only supports last 30 days of intraday data
    # def download_day_stock_data(self):
    #     if not self.interval in ['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h']:
    #         print('Given interval is not intra-day. Changing to 15m')
    #         self.interval = '15m'
    #         self.end_day = wd.workday(self.start_day,5)
        
    #     ## Download data. Add header. Save file
        
    #     pass

    def download_daily_stock_data(self):
        path_prefix = 'data/'
        file_name = path_prefix + self.ticker + '_' + self.interval + '.csv'
        if not os.path.isfile(file_name): 
            start = date(1990,1,1)
        else:
            data = pd.read_csv(file_name)
            last_day = data['Date'].iloc[-1]
            ld = date.fromisoformat(last_day)
            start = wd.workday(ld, 1)

        ## Check if we're up to date
        if start == date.today():
            self.data = data
            print(data)
            return


        t = yf.Ticker(self.ticker)
        h = t.history(start=start, end=date.today(), period='1d', interval=self.interval)

        ## Lines for Backtrader format
        # h =  h.drop("Dividends", 1)
        # h =  h.drop("Stock Splits", 1)
        # h['Adj Close'] = h['Close']
        # h = h[['Open','High','Low','Close','Adj Close', 'Volume']]


        if not os.path.isfile(file_name): 
            h.to_csv(file_name)
        else:
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


if __name__ == "__main__":
    interval = '1d'
    # ticker = 'aapl'
    # test = Ticker_history(ticker, interval)

    tickers = ['f']

    for tick in tickers:
        ticker = Ticker_history(tick, interval=interval)
        ticker.download_daily_stock_data()
        # ticker.download_day_stock_data()