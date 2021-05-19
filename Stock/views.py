import json

import plotly
from django.db.models import Sum
from django.contrib import auth, messages
from django.contrib.sites import requests
from django.shortcuts import render, redirect
import pandas_datareader as web
from datetime import datetime, date
import matplotlib.pyplot as plt
from plotly.offline import plot
import pandas as pd
import datetime as dt
import pandas_datareader.data as web
import plotly.express as px
import plotly.graph_objects as go
from .models import Profile, Buystock, Activity, Stockd, Wallet
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import timedelta
from pandas_datareader import data
import yfinance as yf
from django.http import HttpResponse, JsonResponse
# Create your views here.
from urllib3.connectionpool import xrange
import plotly.graph_objects as go
from plotly.graph_objs import Scatter

def index(request):
    ins=Profile.objects.get(email=request.user.email)
    return render(request,'Stock/index.html',{'pho':ins})
def overview(request):
    if not Profile.objects.filter(email=request.user.email).exists():
        ins = Profile(first_name=request.user.first_name,email=request.user.email)

        ins.save()
    if request.user.is_authenticated:
        if(Buystock.objects.filter(username=request.user.username).exists()):
            all=Buystock.objects.filter(username=request.user.username)
            for i in all:
                from yahoo_fin import stock_info as si
                r = si.get_live_price(i.ticker)
                r=round(r,2)
                s = Stockd.objects.get(ticker=i.ticker,username=request.user.username)
                s.lastprice = r
                s.change = (s.lastprice / s.price)*100
                s.save()
                if (s.lastprice > s.price):
                    s.type='Profit'
                    s.profit = s.quantity * (s.lastprice - s.price)
                    s.change-=100
                elif(s.lastprice < s.price):
                    s.type='Loss'
                    s.profit = s.quantity * (s.price - s.lastprice)
                    s.change=100-s.change
                else:
                    s.type='Stable'
                    s.profit=0.00
                    s.change=0.00
                s.profit=round(s.profit,2)
                print(s.profit)
                s.save()
        else:
            messages.warning(request, "Till Now No Stocks are bought")
        from yahoo_fin import stock_info as si
        r = si.get_day_most_active().head(5)
        r.rename(columns = {'Market Cap':'Market','Price (Intraday)':'Price'}, inplace = True)
        json_records = r.reset_index().to_json(orient='records')
        data = []
        data = json.loads(json_records)
        g = si.get_day_gainers().head(5)
        g.rename(columns={'Market Cap': 'Market', 'Price (Intraday)': 'Price','% Change':'change'}, inplace=True)
        json_records = g.reset_index().to_json(orient='records')
        datag = []
        datag = json.loads(json_records)

        lost = si.get_day_losers().head(5)
        lost.rename(columns={'Market Cap': 'Market', 'Price (Intraday)': 'Price', '% Change': 'change'}, inplace=True)
        json_records = lost.reset_index().to_json(orient='records')
        datal = []
        datal = json.loads(json_records)

        if Stockd.objects.filter(username=request.user.username).exists() and Buystock.objects.filter(username=request.user.username).exists():
            st=Stockd.objects.filter(username=request.user.username)
            po=Profile.objects.get(email=request.user.email)
            return render(request, 'Stock/overview.html', {'d': st,'r':data,'g':datag,'l':datal,'pho':po,'title':'Invest N Grow'})
        else:
            po = Profile.objects.get(email=request.user.email)
            return render(request,'Stock/overview.html',{'r':data,'g':datag,'l':datal,'pho':po,'title':'Invest N Grow'})
    else:
        auth.logout(request)
        return render(request, 'login/login.html')

def profile(request):
    if request.user.is_authenticated:

        if not Profile.objects.filter(email=request.user.email).exists():
            ins=Profile(email=request.user.email)
            ins.save()
        insppp=Profile.objects.get(email=request.user.email)
        if request.method=="POST" and request.POST['update']=="updatevalue":
            po = Profile.objects.get(email=request.user.email)
            return render(request, 'Stock/profile.html', {'prof1': insppp,'pho':po})
        elif request.method == "POST" and request.POST['update'] == "updated":

            fname=request.POST['fname']
            lname=request.POST['lname']
            gender=request.POST['gender']

            dob=request.POST['dob']
            email=request.POST['email']

            #phone=request.POST['phone']
            qualification=request.POST['qualification']
            add1=request.POST['address1']
            add2=request.POST['address2']
            state=request.POST['state']
            photos=request.FILES
            photo=photos.get("photo1")
            #3photo.savefig('media/img.png')
            post=request.POST['postcode']
            city=request.POST['city']
            country=request.POST['country']

            insup = Profile.objects.get(email=request.user.email)
            Profile.objects.filter(email=request.user.email).update()
            
            insup.first_name=fname
            insup.last_name=lname
            insup.gender=gender

            insup.qualification=qualification
            insup.address1=add1
            insup.address2=add2
            insup.state=state

            insup.city=city
            insup.country=country
            if dob!='':
                insup.dateofbirth = dob
            #if phone != '' and phone!=None:
             #   insup.phone = phone
            if post != '' and post!=None:
                insup.postcode = post
            if photo is not None:
                insup.photo=photo
                insup.save()
                print("ohfiduvc",insup.photo)
            insup.save()
            messages.success(request,'Sucessfully Updated')
            insupp = Profile.objects.get(email=request.user.email)
            return render(request, 'Stock/profile.html', {'prof': insupp,'pho':insupp,'title':'Invest N Grow - Profile'})


        return render(request,'Stock/profile.html',{'prof':insppp,'pho':insppp,'title':'Invest N Grow - Profile'})
    else:
        auth.logout(request)
        return render(request, 'login/login.html')

def activity(request):
    if request.user.is_authenticated:
        po = Profile.objects.get(email=request.user.email)
        acty=Activity.objects.filter(username=request.user.username).order_by('-datebought')
        return render(request,'Stock/activity.html',{'activities':acty,'pho':po,'title':'Invest N Grow - Activity'})
    else:
        auth.logout(request)
        return render(request, 'login/login.html')

def wallet(request):
    if not Wallet.objects.filter(username=request.user.username).exists():
        ins = Wallet(username=request.user.username)
        ins.balance=0
        ins.save()

    if request.user.is_authenticated:

        pay=0
        payr = 0
        if request.method=='POST':

            if request.POST.get('topup') :
                price = request.POST['topup']
                price=float(price)
                wall = Wallet.objects.get(username=request.user.username)
                wall.balance=wall.balance+price
                wall.save()
                pay=price
                payr=-1
            else:
                ticker=request.POST['ticker']
                quantity=request.POST['quantity']
                quantity=int(quantity)
                name=request.POST['name']
                price=request.POST['price']
                price=float(price)
                pay=quantity*price
                pay=round(pay,2)
                payr=round(pay,2)

                username=None
                if request.user.is_authenticated:
                    username = request.user.username
                insac = Activity(name=name, type='Buy', quantity=int(quantity), datebought=date.today(),username=username)
                insac.save()
                if Buystock.objects.filter(username=username,ticker=ticker).exists():
                    insu=Buystock.objects.get(username=username,ticker=ticker)
                    insu.quantity=insu.quantity+quantity
                    insu.save()
                else:
                    ins=Buystock(username=username,ticker=ticker,quantity=int(quantity),datebought=date.today(),name=name,price=price)
                    ins.save()
                ins = Stockd(username=username, ticker=ticker, quantity=int(quantity), datebought=date.today(), name=name,
                               price=price,lastprice=price,change=0,type='Profit',profit=0)
                ins.save()


        if(Stockd.objects.filter(username=request.user.username)):
            allp = Stockd.objects.filter(username=request.user.username)
            pol=Profile.objects.get(email=request.user.email)
            sum = 0
            for i in allp:
                if (i.type == 'Profit'):
                    sum += i.profit
                else:
                    sum -= i.profit
            wall=Wallet.objects.get(username=request.user.username)
            return render(request, 'Stock/wallet.html', {'allp': round(sum,2),'pho':pol,'payrs':round(pay,2),'payds':round(pay/70,2),'payy':payr,'wall':round(wall.balance,2),'title':'Invest N Grow - Wallet'})
        else:
            messages.warning(request,"Nothing Traded Till Now")
            return render(request, 'Stock/wallet.html',{'title':'Invest N Grow - Wallet'})
    else:
        auth.logout(request)
        return render(request, 'login/login.html')



def buystocks(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            stock=request.POST['search']
            print(stock)
            import pandas as pd
            import yfinance as yf
            import datetime
            import time
            import requests
            import io
            data = yf.download(stock, date.today(), date.today())
            url = "http://d.yimg.com/autoc.finance.yahoo.com/autoc?query={}&region=1&lang=en".format(stock)

            result = requests.get(url).json()
            sslist=[]
            name="aaaaa"
            print(result['ResultSet']['Result'])
            for x in result['ResultSet']['Result']:
                if x['symbol'] == stock:
                    name=x['name']
                    break
                if stock in x['symbol']:
                    sslist.append(x['name'])

            print(sslist)
            if(name!="aaaaa"):
                from yahoo_fin import stock_info as si
                price=si.get_live_price(stock)
                print("bdsvkjbkjijbb",price)


                alldata = [{'Name':name,'Ticker':stock,'Adj_Close':round(price,2)}]



                context = {'d': alldata}
                print(alldata)
                ins=Activity(name=name,type='search',quantity=0,datebought=date.today(),username=request.user.username)
                ins.save()
                po = Profile.objects.get(email=request.user.email)

                return render(request, 'Stock/buystocks.html', {'d': alldata,'pho':po,'title':'Invest N Grow - Buy'})

            elif sslist:
                url = "https://pkgstore.datahub.io/core/nasdaq-listings/nasdaq-listed_csv/data/7665719fb51081ba0bd834fde71ce822/nasdaq-listed_csv.csv"
                s = requests.get(url).content
                companies = pd.read_csv(io.StringIO(s.decode('utf-8')))
                companies = companies.drop_duplicates(subset=["Symbol"])
                bool = companies['Symbol'].str.startswith(stock, na=False)
                companies=companies[bool]
                companies=companies[1:20]
                print(companies)

                Symbols = companies['Symbol'].tolist()
                Name = companies['Company Name'].tolist()
                stock_final = pd.DataFrame()
                for i, j in zip(Symbols, Name):

                    # print the symbol which is being downloaded
                    print(str(Symbols.index(i)) + str(' : ') + i, sep=',', end=',', flush=True)

                    try:
                        # download the stock price
                        stock = []
                        stock = yf.download(i, start='2021-5-12', end='2021-5-13', progress=False)

                        # append the individual stock prices
                        if len(stock) == 0:
                            None
                        else:
                            stock['Ticker'] = i
                            stock['Name'] = j
                            stock_final = stock_final.append(stock, sort=False)
                    except Exception:
                        None
                # stock_final = stock_final.sort_values(by='Adj Close', ascending=False)
                stock_final.rename(columns={'Adj Close': 'Adj_Close'}, inplace=True)
                print("sjbvjdjddddddddd", stock_final)
                stock_final = stock_final.drop_duplicates(subset=["Ticker"])
                stock_final = stock_final.head(10)
                stock_final = stock_final.round(2)
                alldata = []
                for i in range(stock_final.shape[0]):
                    temp = stock_final.iloc[i]
                    alldata.append(dict(temp))
                    context = {'d': alldata}
                print(alldata)
                po = Profile.objects.get(email=request.user.email)

                return render(request, 'Stock/buystocks.html', {'d': alldata,'pho':po,'title':'Invest N Grow - Buy'})


            else:

                po = Profile.objects.get(email=request.user.email)
                from yahoo_fin import stock_info as si
                g = si.get_day_gainers().head(5)
                g.rename(columns={'Market Cap': 'Market', 'Price (Intraday)': 'Price', '% Change': 'change'},
                         inplace=True)
                json_records = g.reset_index().to_json(orient='records')
                datag = []
                datag = json.loads(json_records)
                messages.error(request, "Stock doesn't exist! Please enter valid Stock Ticker")
                return render(request, 'Stock/buystocks.html', {'pho': po,'datag': datag,'title':'Invest N Grow - Buy'})


        else:
            import pandas as pd
            import yfinance as yf
            import datetime
            import time
            import requests
            import io
            end = date.today()
            start = yesterday = end - timedelta(days = 1)


            url = "https://pkgstore.datahub.io/core/nasdaq-listings/nasdaq-listed_csv/data/7665719fb51081ba0bd834fde71ce822/nasdaq-listed_csv.csv"
            s = requests.get(url).content
            companies = pd.read_csv(io.StringIO(s.decode('utf-8')))
            companies=companies.drop_duplicates(subset = ["Symbol"])
            companies = companies.sample(n=10)
            print(companies)

            Symbols = companies['Symbol'].tolist()
            Name = companies['Company Name'].tolist()

            stock_final = pd.DataFrame()
            for i, j in zip(Symbols, Name):

                # print the symbol which is being downloaded
                print(str(Symbols.index(i)) + str(' : ') + i, sep=',', end=',', flush=True)

                try:
                    # download the stock price
                    stock = []
                    stock = yf.download(i, start='2021-5-12', end='2021-5-13', progress=False)

                    # append the individual stock prices
                    if len(stock) == 0:
                        None
                    else:
                        stock['Ticker'] = i
                        stock['Name'] = j
                        stock_final = stock_final.append(stock, sort=False)
                except Exception:
                    None
            # stock_final = stock_final.sort_values(by='Adj Close', ascending=False)
            stock_final.rename(columns={'Adj Close': 'Adj_Close'}, inplace=True)
            print("sjbvjdjddddddddd", stock_final)
            stock_final = stock_final.drop_duplicates(subset = ["Ticker"])
            stock_final = stock_final.head(20)
            stock_final=stock_final.round(2)
            alldata = []
            for i in range(stock_final.shape[0]):
                temp = stock_final.iloc[i]
                alldata.append(dict(temp))
                context = {'d': alldata}
            print(alldata)
            po = Profile.objects.get(email=request.user.email)

            from yahoo_fin import stock_info as si
            g = si.get_day_gainers().head(5)
            g.rename(columns={'Market Cap': 'Market', 'Price (Intraday)': 'Price', '% Change': 'change'}, inplace=True)
            json_records = g.reset_index().to_json(orient='records')
            datag = []
            datag = json.loads(json_records)
            return render(request,'Stock/buystocks.html',{'pho':po,'d': alldata,'datag':datag,'title':'Invest N Grow - Buy'})
    else:
        auth.logout(request)
        return render(request, 'login/login.html')

def sellstocks(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            sellqty=request.POST.get('sellqty')
            ticker=request.POST.get('ticker')
            name=request.POST.get('name')

            sellqty=int(sellqty)

            s=Buystock.objects.get(ticker=ticker,username=request.user.username)
            if(s.quantity<sellqty):
                messages.error(request, "You Don't Have that much Stocks to Sell")
            elif(s.quantity==sellqty):
                s.delete()
                s = Stockd.objects.get(ticker=ticker, username=request.user.username)
                wall = Wallet.objects.get(username=request.user.username)
                if wall.balance==None or wall.balance=='':
                    wall.balance=0
                wall.balance = wall.balance + sellqty *s.lastprice
                print("wiufiuewb",wall.balance)
                wall.save()
                s.delete()

                ins = Activity(name=name, type='Sell', quantity=sellqty, datebought=date.today(),username=request.user.username)
                ins.save()
                messages.success(request, "Sucessfully Sold the Stocks")
            else:
                s.quantity=s.quantity-sellqty
                s.save()
                s = Stockd.objects.get(ticker=ticker,username=request.user.username)
                wall = Wallet.objects.get(username=request.user.username)
                if wall.balance==None or wall.balance=='':
                    wall.balance=0
                wall.balance = wall.balance + sellqty * s.lastprice
                print("wiufiuewb", wall.balance)
                wall.save()
                s.quantity = s.quantity - sellqty
                s.save()
                ins = Activity(name=name, type='Sell', quantity=sellqty, datebought=date.today(),username=request.user.username)
                ins.save()
                messages.success(request, "Sucessfully Sold the Stocks")

        if(Buystock.objects.filter(username=request.user.username).exists()):
            stocks = Buystock.objects.filter(username=request.user.username)
            sip=Stockd.objects.filter(username=request.user.username)

            po = Profile.objects.get(email=request.user.email)
            return render(request, 'Stock/sellstocks.html', {'d': stocks,'pho':po,'sip':sip,'title':'Invest N Grow - Sell'})
        else:
            messages.warning(request,"No Stocks are bought Till Now")
            po = Profile.objects.get(email=request.user.email)
            return render(request, 'Stock/sellstocks.html',{'pho':po,'title':'Invest N Grow - Sell'})
    else:
        auth.logout(request)
        return render(request, 'login/login.html')


def viewstock(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            ticker=request.POST['ticker']
            name=request.POST['name']
            print(ticker)
            messages.info(request, ticker)
            data='2021-04-07'
            data1=date.today()
            year, month, day = data.split('-')
            start = datetime(int(year), int(month), int(day))
            #year, month, day = data1.split('-')
            #end = datetime(int(year), int(month), int(day))
            df = web.DataReader(ticker, 'yahoo', start, data1)

            ins = Activity(name=name, type='Analyse', quantity=0, datebought=date.today(),username=request.user.username)
            ins.save()
            po = Profile.objects.get(email=request.user.email)
            print(df.index.tolist())
            return render(request,'Stock/viewstock.html',{'pho':po,'cls':df['Close'].tolist(),'hgh':df['High'].tolist(),'lw':df['Low'].tolist(),'date':df.index.tolist()})
        else:
            po = Profile.objects.get(email=request.user.email)
            return render(request, 'Stock/viewstock.html',{'pho':po,'title':'Invest N Grow - Details'})
    else:
        auth.logout(request)
        return render(request, 'login/login.html')


class ChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        labels = [
            'January',
            'February',
            'March',
            'April',
            'May',
            'June',
            'July'
        ]
        chartLabel = "my data"
        chartdata = [0, 10, 5, 2, 20, 30, 45]
        data = {
            "labels": labels,
            "chartLabel": chartLabel,
            "chartdata": chartdata,
        }
        return Response(data)

def logout(request):
    auth.logout(request)
    return render(request,'login/login.html')

def paytwallet(request):
    amount=request.POST['paytwallet']
    wall=Wallet.objects.get(username=request.user.username)
    if float(amount)<wall.balance:
        messages.success(request,"Stock Bought Sucessfully")

        wall.balance=wall.balance-float(amount)
        wall.save()
        return redirect ('wallet')
    else:
        messages.error(request,"Enough Balance is not there in wallet, Topup immediately")
        return redirect('wallet')

def autopay(request):
    if request.method=="POST":
        ticker = request.POST['ticker']
        quantity = 1
        quantity = int(quantity)
        name = request.POST['name']
        price = request.POST['price']
        price = float(price)
        wall = Wallet.objects.get(username=request.user.username)
        wall.balance = wall.balance - price
        wall.save()
        insac = Activity(name=name, type='Buy', quantity=int(quantity), datebought=date.today(), username=request.user.username)
        insac.save()
        if Buystock.objects.filter(username=request.user.username, ticker=ticker).exists():
            insu = Buystock.objects.get(username=request.user.username, ticker=ticker)
            insu.quantity = insu.quantity + quantity
            insu.save()
        else:
            ins = Buystock(username=request.user.username, ticker=ticker, quantity=int(quantity), datebought=date.today(), name=name,
                           price=price)
            ins.save()

        ins = Stockd(username=request.user.username, ticker=ticker, quantity=int(quantity), datebought=date.today(), name=name,
                     price=price, lastprice=price, change=0, type='Profit', profit=0)
        ins.save()
        messages.success(request,"Successfully bought the Stock")
        allp = Stockd.objects.filter(username=request.user.username)
        pol = Profile.objects.get(email=request.user.email)
        sum = 0
        for i in allp:
            if (i.type == 'Profit'):
                sum += i.profit
            else:
                sum -= i.profit
        wall = Wallet.objects.get(username=request.user.username)
        return render(request,"Stock/wallet.html",{'allp': round(sum,2),'pho':pol,'wall':round(wall.balance,2),'title':'Invest N Grow - Wallet'})
    else:

        import pandas as pd
        import yfinance as yf
        import datetime
        import time
        import requests
        import io
        end = date.today()
        start = yesterday = end - timedelta(days=1)
        wall=Wallet.objects.get(username=request.user.username)
        url = "https://pkgstore.datahub.io/core/nasdaq-listings/nasdaq-listed_csv/data/7665719fb51081ba0bd834fde71ce822/nasdaq-listed_csv.csv"
        s = requests.get(url).content
        companies = pd.read_csv(io.StringIO(s.decode('utf-8')))
        companies = companies.drop_duplicates(subset=["Symbol"])
        companies = companies.sample(n=20)
        print(companies)

        Symbols = companies['Symbol'].tolist()
        Name = companies['Company Name'].tolist()

        stock_final = pd.DataFrame()
        for i, j in zip(Symbols, Name):

            # print the symbol which is being downloaded
            print(str(Symbols.index(i)) + str(' : ') + i, sep=',', end=',', flush=True)

            try:
                # download the stock price
                stock = []
                stock = yf.download(i, start='2021-5-12', end='2021-5-13', progress=False)

                # append the individual stock prices
                if len(stock) == 0:
                    None
                else:
                    stock['Ticker'] = i
                    stock['Name'] = j
                    stock_final = stock_final.append(stock, sort=False)
            except Exception:
                None
        # stock_final = stock_final.sort_values(by='Adj Close', ascending=False)
        stock_final.rename(columns={'Adj Close': 'Adj_Close'}, inplace=True)
        print("sjbvjdjddddddddd", stock_final)
        stock_final = stock_final.drop_duplicates(subset=["Ticker"])
        stock_final = stock_final.head(20)
        stock_final = stock_final.round(2)
        stock_final = stock_final.sort_values(by=["Adj_Close"], ascending=False)
        stock_final = stock_final[stock_final['Adj_Close'] < wall.balance]
        alldata = []
        for i in range(stock_final.shape[0]):
            temp = stock_final.iloc[i]
            alldata.append(dict(temp))
            context = {'d': alldata}
        print(alldata)
        po = Profile.objects.get(email=request.user.email)


        return render(request, 'Stock/autopay.html',
                      {'pho': po, 'd': alldata, 'title': 'Invest N Grow - Autopay'})
def stockprediction(request):
    if request.method=="POST":

        import math
        import pandas_datareader as web
        import numpy as np
        import pandas as pd
        from sklearn.preprocessing import MinMaxScaler
        from keras.models import Sequential
        from keras.layers import Dense, LSTM
        import matplotlib.pyplot as plt
        plt.style.use('fivethirtyeight')
        ticker=request.POST['predict']
        # Get the stock quote
        df = web.DataReader(ticker, data_source='yahoo', start='2021-01-01', end='2021-05-18')

        data = df.filter(['Close'])

        # Convert the dataframe to a numpy array
        dataset = data.values
        # Get the number of rows to train the model on
        training_data_len = math.ceil(len(dataset) * 0.8)

        training_data_len

        # Scale the data
        scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_data = scaler.fit_transform(dataset)

        scaled_data

        # Create the training data set
        # Create the scaled training data set
        train_data = scaled_data[0:training_data_len, :]
        # Split the data into x_train and y_train data sets
        x_train = []
        y_train = []
        # We create a loop
        for i in range(60, len(train_data)):
            x_train.append(train_data[i - 60:i, 0])  # Will conaint 60 values (0-59)
            y_train.append(train_data[i, 0])  # Will contain the 61th value (60)
            if i <= 60:
                print("pppp", x_train)
                print(y_train)
                print()

        # Convert the x_train and y_train to numpy arrays
        x_train, y_train = np.array(x_train), np.array(y_train)

        # Reshape the data
        x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
        x_train.shape

        # Build the LSTM model
        model = Sequential()
        model.add(LSTM(50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
        model.add(LSTM(50, return_sequences=False))
        model.add(Dense(25))
        model.add(Dense(1))

        # Compile the model
        model.compile(optimizer='adam', loss='mean_squared_error')

        # Train the model
        model.fit(x_train, y_train, batch_size=1, epochs=1)

        # Create the testing data set
        # Create a new array containing scaled values from index 1738 to 2247
        test_data = scaled_data[training_data_len - 60:]
        # Create the data set x_test and y_test
        x_test = []
        y_test = dataset[training_data_len:, :]
        for i in range(60, len(test_data)):
            x_test.append(test_data[i - 60:i, 0])

        # Convert the data to a numpy array
        x_test = np.array(x_test)

        # Reshape the data
        x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

        # Get the model's predicted price values for the x_test data set
        predictions = model.predict(x_test)
        predictions = scaler.inverse_transform(predictions)
        predictions

        # Evaluate model (get the root mean quared error (RMSE))
        rmse = np.sqrt(np.mean(predictions - y_test) ** 2)
        rmse

        # Plot the data
        train = data[:training_data_len]
        valid = data[training_data_len:]
        valid['Predictions'] = predictions
        # Visualize the data
        plt.figure(figsize=(16, 8))
        plt.title('Model')
        plt.xlabel('Date', fontsize=18)
        plt.ylabel('Close Price USD ($)', fontsize=18)
        plt.plot(train['Close'])
        plt.plot(valid[['Close', 'Predictions']])

        X_FUTURE = 10
        predictions = np.array([])
        last = x_test[-1]
        for i in range(X_FUTURE):
            curr_prediction = model.predict(np.array([last]))
            last = np.concatenate([last[1:], curr_prediction])
            predictions = np.concatenate([predictions, curr_prediction[0]])
        predictions = scaler.inverse_transform([predictions])[0]

        import datetime
        from datetime import timedelta
        dicts = []
        curr_date = data.index[-1]
        for i in range(X_FUTURE):
            curr_date = curr_date + timedelta(days=1)
            dicts.append({'Predictions': predictions[i], "Date": curr_date})

        new_data = pd.DataFrame(dicts).set_index("Date")
        new_data['Dat'] = new_data.index
        new_data['Dat'] = new_data['Dat'].dt.strftime('%Y-%m-%d')
        print(new_data)
        json_records = new_data.reset_index().to_json(orient='records')
        data = []
        data = json.loads(json_records)
        context = {'d': data}
        print(context)
        return render(request,"Stock/stockprediction.html",{'d':data,'t':ticker,'title': 'Invest N Grow - Predictions'})
    return render(request,"Stock/stockprediction.html",{'title': 'Invest N Grow - Predictions'})

def get_symbol(symbol):
    symbol_list = requests.get("http://chstocksearch.herokuapp.com/api/{}".format(symbol)).json()

    for x in symbol_list:
        if x['symbol'] == symbol:
            return x['company']


def stock(request,n):
    from yahoo_fin import stock_info as si
    r=si.get_live_price(n)
    s = Stockd.objects.get(ticker=n)
    s.lastprice=r
    s.change=(s.lastprice/s.price)*100
    s.save()

def get_symbol(symbol):
    symbol_list = requests.get("http://chstocksearch.herokuapp.com/api/{}".format(symbol)).json()

    for x in symbol_list:
        if x['symbol'] == symbol:
            return x['company']