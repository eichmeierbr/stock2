from kDayClassifier import *
from evaluateClassifier import *
from datetime import date, timedelta
import numpy as np
import stock_market as sm

apple = kDayMean('aapl', days=5)
year = 2019
month = 12
day = 31

# endDay = date.today()
endDay = date(year,month,day)

numDays = 1

# sm.dayPrices('aapl')
gain = evaluateClassifier(apple, numDays, endDay, which='Open')
print(gain)