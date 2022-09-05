import numpy as np
import talib

from traders.baseTrader import baseTrader

class simpleMovingAverageCrossTrader(baseTrader):
    def __init__(self):
        super().__init__()
        self.type = 'simpleMA'
        self.didPreviousCross = -1
        self.shortMAtime = 10
        self.longMAtime = 40


    def act(self, data):
        vals = data[0].history[:,1].astype(np.float)

        shortMa = talib.EMA(vals[-self.shortMAtime:], self.shortMAtime)[-1]
        longMa = talib.EMA(vals[-self.longMAtime:], self.longMAtime)[-1]

        if shortMa > longMa:
            desired = np.zeros_like(data)
            desired[0] = self.totalValue/vals[-1]
            if self.didPreviousCross == 0:
                print("Buy ")
            self.didPreviousCross = 1

        else:
            desired = np.zeros_like(data)
            if self.didPreviousCross == 1:
                print("Sell")
            self.didPreviousCross = 0
        return desired