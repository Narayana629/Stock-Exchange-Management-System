import pandas as pd
import yfinance as yf
import datetime
import time
import requests
import io

start = datetime.datetime(2021,5,1)
end = datetime.datetime(2021,5,1)

url="https://pkgstore.datahub.io/core/nasdaq-listings/nasdaq-listed_csv/data/7665719fb51081ba0bd834fde71ce822/nasdaq-listed_csv.csv"
s = requests.get(url).content
companies = pd.read_csv(io.StringIO(s.decode('utf-8')))
print(companies['Company Name'])

Symbols = companies['Symbol'].tolist()
Name=companies['Company Name'].tolist()

stock_final = pd.DataFrame()
for i,j in zip(Symbols,Name):

    # print the symbol which is being downloaded
    print(str(Symbols.index(i)) + str(' : ') + i, sep=',', end=',', flush=True)

    try:
        # download the stock price
        stock = []
        stock = yf.download(i, start=start, end=end, progress=False)

        # append the individual stock prices
        if len(stock) == 0:
            None
        else:
            stock['Ticker'] = i
            stock['Name']=j
            stock_final = stock_final.append(stock, sort=False)
    except Exception:
        None
stock_final.rename(columns={'Adj Close':'Adj_Close'},inplace = True)
print(stock_final[['Name','Ticker','Adj_Close']])