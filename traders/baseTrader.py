import numpy as np

class baseTrader:
    def __init__(self):
        self.type = 'base'
        self.cash = 1000
        self.ownedStock = []
        self.stockUniverse = []
        self.sizeUniverse = 0
        self.stockValue = []
        self.totalValue = self.cash
        self.totalValueHistory = []
        self.stockValueHistory = []

        ## Market Purchase Fees
        self.transactionFee = 1
        self.slippage = 0.5/100 * 0


    def act(self, data):
        return np.random.zeros(len(data))

    def getStockPrices(self, data):
        stockPrices = []
        for d in data:
            stockPrices.append(d.now_data[1])
        return stockPrices

    def initPortfolio(self, universe):
        self.ownedStock = np.zeros(len(universe))
        self.stockValue = np.zeros(len(universe))
        self.totalValue = self.cash
        self.stockUniverse = universe[:]
        self.sizeUniverse = len(universe)
        self.totalValueHistory.append(self.totalValue)
        self.stockValueHistory.append(np.copy(self.stockValue))


    def performTransactions(self, stockData, desiredPortfolio, isValue=True):
        # Perform Sells
        for i in range(self.sizeUniverse):
            stockDiff = self.ownedStock[i] - desiredPortfolio[i]
            price = stockData[i].now_data[1] # 1: Open. 4: Close
            if stockDiff > 0:
                self.cash += stockDiff*price*(1-self.slippage) - self.transactionFee
                self.ownedStock[i] -= stockDiff
            self.stockValue[i] = self.ownedStock[i] * price             

        # Perform Buys
        for i in range(self.sizeUniverse):
            stockDiff = desiredPortfolio[i] - self.ownedStock[i]
            price = stockData[i].now_data[1] # 1: Open. 4: Close
            if stockDiff > 0:
                transactionCost = stockDiff*price*(1+self.slippage) - self.transactionFee
                if transactionCost > self.cash:
                    stockDiff = (self.cash + self.transactionFee) / (price * (1+self.slippage))
                self.cash -= stockDiff*price*(1+self.slippage) - self.transactionFee
                self.ownedStock[i] += stockDiff
            self.stockValue[i] = self.ownedStock[i] * price

        self.totalValue = self.cash + np.sum(self.stockValue)
        pass


    def advanceTime(self):
        self.totalValueHistory.append(self.totalValue)
        self.stockValueHistory.append(np.copy(self.stockValue))
        a = 3
