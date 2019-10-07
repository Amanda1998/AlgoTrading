import matplotlib.pyplot as plt
from src.main.Analysis import Analysis


class Visualization:

    def __init__(self, stock):
        self.stock = stock
        self.analysis = Analysis(stock)
        self.dailyReturns = self.analysis.dailyPctChange()['Adj Close']
        self.monthlyReturns = self.analysis.monthlyPctChange()['Adj Close']
        self.quaterReturns = self.analysis.quarterPctChange()['Adj Close']

    def closePrice(self):
        self.stock.close().plot(grid=True)
        plt.show()

    def dailyReturnsHistogram(self):
        self.dailyReturns.hist(bins=50)
        plt.show()
        print('Daily percentage change:\n', self.dailyReturns.describe())

    def cumulativeReturns(self, type):
        cum_return = None
        if type == 'daily':
            cum_return = (1 + self.dailyReturns).cumprod()
        if type == 'monthly':
            cum_return = (1 + self.monthlyReturns).cumprod()
        if type == 'quarterly':
            cum_return = (1 + self.quaterReturns).cumprod()
        cum_return.fillna(0, inplace=True)
        cum_return.plot(figsize=(12, 8))
        plt.show()
        print(cum_return)

    def rollingWindow(self,window_period):
        self.stock.close().plot()
        self.analysis.rollingAdjClose(window_period).plot()
        plt.show()




if __name__ == '__main__':
    from src.main.Stock import Stock
    apple = Stock('AAPL', '2006-10-01', '2012-01-01')
    v1 = Visualization(apple)
    # v1.cumulativeReturns('monthly')
    v1.rollingWindow(42)
