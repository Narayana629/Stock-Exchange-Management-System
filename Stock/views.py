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
    '''if not Profile.objects.filter(email=request.user.email).exists():
        ins = Profile(email=request.user.email)

        ins.save()'''
    if request.user.is_authenticated:
        if(Buystock.objects.filter(username=request.user.username).exists()):
            all=Buystock.objects.filter(username=request.user.username)
            for i in all:
                from yahoo_fin import stock_info as si
                r = si.get_live_price(i.ticker)

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
            return render(request, 'Stock/overview.html', {'d': st,'r':data,'g':datag,'l':datal,'pho':po})
        else:
            po = Profile.objects.get(email=request.user.email)
            return render(request,'Stock/overview.html',{'r':data,'g':datag,'l':datal,'pho':po})
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
            phone=request.POST['phone']
            qualification=request.POST['qualification']
            add1=request.POST['address1']
            add2=request.POST['address2']
            state=request.POST['state']
            post=request.POST['postcode']
            city=request.POST['city']
            country=request.POST['country']
            photo=request.POST['photo']
            print("ppppppppppppp",photo)
            insup = Profile.objects.get(email=request.user.email)
            Profile.objects.filter(email=request.user.email).update()
            insup.first_name=fname
            insup.last_name=lname
            insup.gender=gender
            insup.dateofbirth=dob
            insup.phone=phone
            insup.qualification=qualification
            insup.address1=add1
            insup.address2=add2
            insup.state=state
            insup.postcode=post
            insup.city=city
            insup.country=country
            if photo != '':
                insup.photo=photo
                insup.save()
                print("ohfiduvc",insup.photo)

            insup.save()
            messages.success(request,'Sucessfully Updated')
            insupp = Profile.objects.get(email=request.user.email)
            return render(request, 'Stock/profile.html', {'prof': insupp,'pho':insupp})


        return render(request,'Stock/profile.html',{'prof':insppp,'pho':insppp})
    else:
        auth.logout(request)
        return render(request, 'login/login.html')

def activity(request):
    if request.user.is_authenticated:
        po = Profile.objects.get(email=request.user.email)
        acty=Activity.objects.filter(username=request.user.username).order_by('-datebought')
        return render(request,'Stock/activity.html',{'activities':acty,'pho':po})
    else:
        auth.logout(request)
        return render(request, 'login/login.html')

def wallet(request):
    if not Wallet.objects.filter(username=request.user.username).exists():
        ins = Wallet(username=request.user.username)
        ins.save()

    if request.user.is_authenticated:

        pay=0
        if request.method=='POST':
            ticker=request.POST['ticker']
            quantity=request.POST['quantity']
            quantity=int(quantity)
            name=request.POST['name']
            price=request.POST['price']
            price=float(price)
            pay=quantity*price
            pay=round(pay,2)
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
            return render(request, 'Stock/wallet.html', {'allp': round(sum,2),'pho':pol,'payrs':round(pay,2),'payds':round(pay/70,2),'wall':wall.balance})
        else:
            messages.warning(request,"Nothing Traded Till Now")
            return render(request, 'Stock/wallet.html',)
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

            for x in result['ResultSet']['Result']:
                if x['symbol'] == stock:
                    name=x['name']
                    break
            from yahoo_fin import stock_info as si
            price=si.get_live_price(stock)
            '''start = date.today()
            end = date.today()
            url = "https://pkgstore.datahub.io/core/nasdaq-listings/nasdaq-listed_csv/data/7665719fb51081ba0bd834fde71ce822/nasdaq-listed_csv.csv"
            s = requests.get(url).content
            companies = pd.read_csv(io.StringIO(s.decode('utf-8')))
    
            companies = companies.loc[companies['Symbol'] == stock]
            Symbols = companies['Symbol'].tolist()
            Name = companies['Company Name'].tolist()
            stock_final = pd.DataFrame()
            for i, j in zip(Symbols, Name):
    
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
                        stock['Name'] = j
                        stock_final = stock_final.append(stock, sort=False)
                except Exception:
                    None
            # stock_final = stock_final.sort_values(by='Adj Close', ascending=False)
            stock_final.rename(columns={'Adj Close': 'Adj_Close'}, inplace=True)
            data = stock_final[['Name','Ticker','Adj_Close']]'''

            alldata = [{'Name':name,'Ticker':stock,'Adj_Close':price}]



            context = {'d': alldata}
            print(alldata)
            ins=Activity(name=name,type='search',quantity=0,datebought=date.today(),username=request.user.username)
            ins.save()
            po = Profile.objects.get(email=request.user.email)
            return render(request, 'Stock/buystocks.html', {'d': alldata,'pho':po})

        else:
            import pandas as pd
            import yfinance as yf
            import datetime
            import time
            import requests
            import io

            start = datetime.datetime(2021, 5, 1)
            end = datetime.datetime(2021, 5, 1)

            url = "https://pkgstore.datahub.io/core/nasdaq-listings/nasdaq-listed_csv/data/7665719fb51081ba0bd834fde71ce822/nasdaq-listed_csv.csv"
            s = requests.get(url).content
            companies = pd.read_csv(io.StringIO(s.decode('utf-8')))
            companies = companies[1:6]
            print(companies['Company Name'])

            Symbols = companies['Symbol'].tolist()
            Name = companies['Company Name'].tolist()

            stock_final = pd.DataFrame()
            for i, j in zip(Symbols, Name):

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
                        stock['Name'] = j
                        stock_final = stock_final.append(stock, sort=False)
                except Exception:
                    None
            #stock_final = stock_final.sort_values(by='Adj Close', ascending=False)
            stock_final.rename(columns={'Adj Close': 'Adj_Close'}, inplace=True)
            data=stock_final[['Name', 'Ticker', 'Adj_Close']].head(20)

            alldata=[]
            for i in range(data.shape[0]):
                temp=data.iloc[i]
                alldata.append(dict(temp))
                context={'d':alldata}
            print(alldata)
            po = Profile.objects.get(email=request.user.email)

            from yahoo_fin import stock_info as si
            g = si.get_day_gainers().head(5)
            g.rename(columns={'Market Cap': 'Market', 'Price (Intraday)': 'Price', '% Change': 'change'}, inplace=True)
            json_records = g.reset_index().to_json(orient='records')
            datag = []
            datag = json.loads(json_records)
            return render(request,'Stock/buystocks.html',{'d':alldata,'pho':po,'datag':datag})
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
            po = Profile.objects.get(email=request.user.email)
            return render(request, 'Stock/sellstocks.html', {'d': stocks,'pho':po})
        else:
            messages.warning(request,"No Stocks are bought Till Now")
            po = Profile.objects.get(email=request.user.email)
            return render(request, 'Stock/sellstocks.html',{'pho':po})
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
            return render(request, 'Stock/viewstock.html',{'pho':po})
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