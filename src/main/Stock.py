from pandas_datareader import data

class Stock:

    def __init__(self, ticker, startDate, endDate, source='yahoo'):
        self.ticker = ticker
        self.startDate = startDate
        self.endDate = endDate
        self.source = source
        # self.readData = data.DataReader(name=ticker, start=startDate, end=endDate)

    def stockData(self):
        '''return a pandas dataFrame object'''
        return data.DataReader(name=self.ticker, data_source=self.source, start=self.startDate, end=self.endDate)

    def high(self):
        return self.stockData().get('High')

    def low(self):
        return self.stockData().get('Low')

    def close(self):
        return self.stockData().get('Close')

    def volume(self):
        return self.stockData().get('Volume')

    def adjClose(self):
        return self.stockData().get('Adj Close')

    def open(self):
        return self.stockData().get('Open')

    def diff(self):
        return self.open() - self.close()

if __name__ == '__main__':
    apple = Stock('AAPL','2006-10-01', '2012-01-01')
    print(apple.close())