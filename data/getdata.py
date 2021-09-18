from datetime import date
import yfinance as yf
import os.path
import pandas as pd
import workdays as wd

path_prefix = ''
tickers = ['msft']
end = date.today()

for tick in tickers:
    file_name = path_prefix + tick + '.csv'
    if not os.path.isfile(file_name): 
        start = date(1990,1,1)
    else:
        data = pd.read_csv(file_name)
        last_day = data['Date'].iloc[-1]
        ld = date.fromisoformat(last_day)
        start = wd.workday(ld, 1)



    t = yf.Ticker(tick)
    h = t.history(start=start,end=end, period='1d')
    h =  h.drop("Dividends", 1)
    h =  h.drop("Stock Splits", 1)
    h['Adj Close'] = h['Close']

    h = h[['Open','High','Low','Close','Adj Close', 'Volume']]
    # print(h.head)

    if not os.path.isfile(file_name): 
        h.to_csv(file_name)
    else:
        h.to_csv('temp'+'.csv')
        data2 = pd.read_csv('temp.csv')
        os.remove('temp.csv')

        data3 = pd.concat([data,data2], axis=0)
        data3.to_csv(file_name, index=False)