
from yahoo_fin import stock_info as si


dow_list = si.tickers_nasdaq()
for i in dow_list:
    print(si.get_data(i))

print(dow_list)