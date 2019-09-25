import numpy as np


class Analysis:

    def __init__(self, stock):
        self.stock = stock

    def logReturns(self, pctChange):
        daily_log_return = np.log(pctChange['Adj Close'] + 1)
        return daily_log_return

    def dailyPctChange(self):
        daily_pct_change = self.stock.stockData().pct_change()
        daily_pct_change.fillna(0, inplace=True)
        return daily_pct_change

    def monthlyPctChange(self):
        # Resample `aapl` to business months, take last observation as value
        monthly = self.stock.stockData().resample('BM').apply(lambda x: x[-1])
        return monthly.pct_change()

    def quarterPctChange(self):
        # Resample `aapl` to quarters, take the mean as value per quarter
        quarter = self.stock.stockData().resample("4M").mean()
        return quarter.pct_change()


if __name__ == '__main__':
    from src.main.Stock import Stock

    apple = Stock('AAPL', '2010-01-01', '2012-12-31')
    a1 = Analysis(apple)
    dailyChange = a1.dailyPctChange()
    monthlyChange = a1.monthlyPctChange()
    quarterChange = a1.quarterPctChange()
    print(a1.logReturns(dailyChange))
