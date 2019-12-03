from src.main.Analysis import Analysis
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class Strategy:

    def __init__(self, stock):
        self.stock = stock
        self.analysis = Analysis(stock)
        # self.signals = pd.DataFrame(index=stock.stockData().index)
        self.stockData = self.stock.stockData()
        self.stockData['signal'] = 0.0

    def movingAveCrossover(self, short_window=40, long_window=100):
        self.stockData['short_mavg'] = self.analysis.rollingClose(window_period=short_window, min_periods=1)
        self.stockData['long_mavg'] = self.analysis.rollingClose(window_period=long_window, min_periods=1)
        self.stockData['signal'][short_window:] = np.where(
            self.stockData['short_mavg'][short_window:] > self.stockData['long_mavg'][short_window:], 1.0, 0.0)
        self.stockData['positions'] = self.stockData['signal'].diff()
        return self.stockData

    def plotSignal(self):
        fig = plt.figure()
        ax1 = fig.add_subplot(111, ylabel='Price in $')
        signals = self.movingAveCrossover()
        self.stock.close().plot(ax=ax1, color='r', lw=2.)
        # Plot the short and long moving averages
        signals[['short_mavg', 'long_mavg']].plot(ax=ax1, lw=2.)
        # Plot the buy signals(black)
        ax1.plot(signals.loc[signals.positions == 1.0].index,
                 signals.short_mavg[signals.positions == 1.0],
                 '^', markersize=10, color='m')
        # Plot the sell signals(purple)
        ax1.plot(signals.loc[signals.positions == -1.0].index,
                 signals.short_mavg[signals.positions == -1.0],
                 'v', markersize=10, color='k')
        # Show the plot
        plt.show()


if __name__ == '__main__':
    from src.main.Stock import Stock

    apple = Stock('AAPL', '2006-10-01', '2012-01-01')
    s1 = Strategy(apple)
    # s1.plotSignal()
    print(s1.movingAveCrossover())
