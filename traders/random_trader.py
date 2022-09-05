import numpy as np

from traders.baseTrader import baseTrader

class randomTrader(baseTrader):
    def __init__(self):
        super().__init__()
        self.type = 'random'


    def act(self, data):
        if len(data) > 1:
            desired =np.random.random(len(data))
            desired *= self.totalValue / np.sum(desired)
        else:
            desired = np.random.randint(0,2,2)[:1] * self.totalValue
        stockPrices = self.getStockPrices(data)
        desired = desired/stockPrices
        return desired