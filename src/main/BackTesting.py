from src.main.Strategy import Strategy
from src.main.Analysis import Analysis
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class BackTesting:
    def __init__(self,stock):
        self.stock = stock
        self.stockData = self.stock.stockData()
        self.analysis = Analysis(stock)
        self.strategy = Strategy(stock)
        self.data = self.strategy.movingAveCrossover(short_window=15,long_window=80)


    def compareToMarket(self):
        self.data['Market Returns'] = self.data['Adj Close'].pct_change()
        self.data['Strategy'] = self.data['Market Returns'] * self.data['signal'].shift(1)
        fig = plt.figure()
        ax1 = fig.add_subplot(111, ylabel='Price in $')
        self.data[['Market Returns','Strategy']].cumsum().plot(grid=True,figsize=(8,5))
        plt.show()

    def portfolio(self):
        # Set the initial capital
        initial_capital= float(100000.0)
        positions = pd.DataFrame(index=self.stockData.index).fillna(0.0)
        positions['signal'] = self.data['signal']
        positions['Adj Close'] = self.data['Adj Close']
        # buy 10 shares
        positions[self.stock.ticker] = 100*positions['signal']
        # Initialize the portfolio with value owned
        portfolio = positions.multiply(positions['Adj Close'], axis=0)
        # Store the difference in shares owned
        pos_diff = positions.diff()
        # Add `holdings` to portfolio
        portfolio['holdings'] = (positions.multiply(positions['Adj Close'], axis=0)).sum(axis=1)
        # Add `cash` to portfolio
        portfolio['cash'] = initial_capital - (pos_diff.multiply(positions['Adj Close'], axis=0)).sum(axis=1).cumsum()

        # Add `total` to portfolio
        portfolio['total'] = portfolio['cash'] + portfolio['holdings']

        # Add `returns` to portfolio
        portfolio['returns'] = portfolio['total'].pct_change()
        portfolio['initial capital'] = initial_capital
        return portfolio

    def plotPorfolio(self):
        portfolio = self.portfolio()
        # Create a figure
        fig = plt.figure()

        ax1 = fig.add_subplot(111, ylabel='Portfolio value in $')

        # Plot the equity curve in dollars
        portfolio['total'].plot(ax=ax1, lw=2.)
        # plot initial capital to compare
        # portfolio['initial capital'].plot(ax=ax1)

        ax1.plot(portfolio.loc[self.data.positions == 1.0].index,
                 portfolio.total[self.data.positions == 1.0],
                 '^', markersize=10, color='m')
        ax1.plot(portfolio.loc[self.data.positions == -1.0].index,
                 portfolio.total[self.data.positions == -1.0],
                 'v', markersize=10, color='k')

        # Show the plot
        plt.show()


if __name__ == '__main__':
    from src.main.Stock import Stock
    from datetime import date
    today = date.today()
    apple = Stock('AAPL', '2019-01-01', today)
    bt = BackTesting(apple)
    # bt.compareToMarket()
    # print(bt.portfolio())
    bt.plotPorfolio()
