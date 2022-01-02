import numpy as np

from traders.baseTrader import baseTrader

class holdTrader(baseTrader):
    def __init__(self, desiredSpread=-1):
        super().__init__()
        self.type = 'hold'
        self.spread = desiredSpread
        self.hasBought = False


    def act(self, data):
        if self.hasBought:
            return self.ownedStock

        self.hasBought = True
        stockPrices = self.getStockPrices(data)

        if self.spread == -1:
            desired = np.ones(self.sizeUniverse) * self.cash / self.sizeUniverse
        else:
            desired = self.spread
        desired /= stockPrices
        return desired