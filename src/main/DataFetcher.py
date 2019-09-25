from pandas_datareader import data
import matplotlib.pyplot as plt
import pandas as pd

tickers = ['AAPL', 'MSFT', '^GSPC']
start_date = '2010-01-01'
end_date = '2010-12-31'
panel_data = data.DataReader('AAPL','yahoo', start_date, end_date)
# print(panel_data.head(9))
# panel_data = data.get_data_yahoo("AAPL",start=start_date,end=end_date)
print(panel_data.head(9))