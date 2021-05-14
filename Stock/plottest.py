import pandas_datareader as web
from datetime import datetime, date
import matplotlib.pyplot as plt

data='2021-04-04'
data1='2021-05-04'
ticker='AAL'
year, month, day = data.split('-')
start = datetime(int(year), int(month), int(day))
year, month, day = data1.split('-')
end = datetime(int(year), int(month), int(day))
df = web.DataReader(ticker, 'yahoo', start, end)
print(df)
title = ticker + ' Closing Price'
plt.figure(figsize=(10, 6))
plt.grid(True)
plt.xlabel('Dates')
plt.ylabel('Close Prices')
plt.plot(df['Close'])
plt.title(title)
plt.savefig('static/assets/images/plot.png')