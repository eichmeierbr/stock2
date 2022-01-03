import numpy as np
import matplotlib.pyplot as plt

class baseTrader:
    def __init__(self):
        self.type = 'base'
        self.cash = 10000
        self.ownedStock = []
        self.stockUniverse = []
        self.sizeUniverse = 0
        self.stockValue = []
        self.totalValue = self.cash
        self.totalValueHistory = []
        self.stockValueHistory = []

        ## Market Purchase Fees
        self.transactionFee = .05
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
            stockDiff = min(stockDiff, self.ownedStock[i])
            price = stockData[i].now_data[1] # 1: Open. 4: Close
            if stockDiff > 0:
                sellGain = stockDiff*price*(1-self.slippage) - self.transactionFee
                if self.cash + sellGain > 0: ## Make sure we can afford to sell
                    self.cash += sellGain
                    self.ownedStock[i] -= stockDiff
            self.stockValue[i] = self.ownedStock[i] * price             

        # Perform Buys
        for i in range(self.sizeUniverse):
            stockDiff = desiredPortfolio[i] - self.ownedStock[i]
            price = stockData[i].now_data[1] # 1: Open. 4: Close
            if stockDiff > 0:
                transactionCost = stockDiff*price*(1+self.slippage) + self.transactionFee
                if transactionCost > self.cash: # Check if we can afford the stock
                    stockDiff = (self.cash - self.transactionFee) / (price * (1+self.slippage)) # If not, buy the most we can afford
                if stockDiff < 0: ## Skip if we can't afford this buy
                    continue
                self.cash -= stockDiff*price*(1+self.slippage) + self.transactionFee
                self.ownedStock[i] += stockDiff
            self.stockValue[i] = self.ownedStock[i] * price

        self.totalValue = self.cash + np.sum(self.stockValue)
        pass


    def advanceTime(self):
        self.totalValueHistory.append(self.totalValue)
        self.stockValueHistory.append(np.copy(self.stockValue))


    def plotResults(self, days):
        print('%s Final Value: %.2f' %(self.type, self.totalValue))
        plt.plot(days, np.array(self.totalValueHistory)/self.totalValueHistory[0], label=self.type)
