from kDayClassifier import *

apple = kDayMean('aapl')
print apple.predict(minute=True)