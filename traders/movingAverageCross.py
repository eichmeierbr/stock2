import numpy as np
import talib

from traders.baseTrader import baseTrader

class simpleMovingAverageCrossTrader(baseTrader):
    def __init__(self):
        super().__init__()
        self.type = 'simpleMA'
        self.didPreviousCross = -1
        self.shortMAtime = 50
        self.longMAtime = 200


    def act(self, data):
        vals = data[0].history[:,1].astype(np.float)
        shortMa = np.mean(vals[-self.shortMAtime:])
        longMa = np.mean(vals[-self.longMAtime:])

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