# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#Importing all required packages
from pandas_datareader import data as pdr
from datetime import date
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf
from functools import reduce
yf.pdr_override()


##############################################################################
############### FUNCTIONS FOR QUICK DATA IMPORTING AND CLEANING ##############                            
##############################################################################


#A function to import data from yahoo finance-
def y_importer(y):
    start_date = '2018-05-24'
    end_date = '2021-05-24'
    x = pdr.get_data_yahoo(y, start=start_date, end=end_date)
    return x

# a function with a for loop to fill missing values with forward fill 
#ie. the previous value
def fill_missing_val(x):
        for col in x:
            x[col].fillna(method='ffill',inplace = True)
        return   x.isnull().any()


#creating a new function to clean data
def crypto_cleaner(x):
    x['Change %']= x['Close'].pct_change()
    x['Change %'].fillna(method = 'bfill',inplace = True)
    x.reset_index(inplace=True,drop=False)
    x.Date = x.Date.astype('datetime64')
    return x.info()
    
#creating a new function to plot data
def crypto_plotter(x):
    fig, (ax1,ax2,ax3) = plt.subplots(3,1)

    ax1.plot(x['Date'],x['Close'])
    ax2.plot(x['Date'],x['Change %'],color = 'g')
    ax3.plot(x['Date'],x['Volume'],color = 'r')


    fig.subplots_adjust(left=0.1,
                    bottom=0.1, 
                    right=0.9, 
                    top=0.9, 
                    wspace=0.4, 
                    hspace=0.4)

    plt.tight_layout()
    plt.show()

#creating a function to drop unnecessary data
def crypto_dropper(x):
    x['date']=x['Date']
    x['close']=x['Close']
    x['pct_chng']=x['Change %']
    x['vol']=x['Volume']

    x.drop(x.iloc[:,0:8], axis = 1, inplace=True)

    return x

#creating a function to combine previous 3 functions
def crypto_processor(x):
    fill_missing_val(x)
    crypto_cleaner(x)
    #crypto_plotter(x)
    crypto_dropper(x)
    return x


#Importing and cleaning all required crypto currencies 
#WITH JUST 10 LINES OF CODE 

btc = y_importer('BTC-USD')
crypto_processor(btc)

eth = y_importer('ETH-USD')
crypto_processor(eth)

ada = y_importer('ADA-USD')
crypto_processor(ada)

doge = y_importer('DOGE-USD')
crypto_processor(doge)

xrp = y_importer('XRP-USD')
crypto_processor(xrp)



#renaming the columns to make combining easier
btc.columns= ['date','btc_price','btc_pct_chng','btc_vol']
eth.columns = ['date','eth_price','eth_pct_chng','eth_vol']
ada.columns = ['date','ada_price','ada_pct_chng','ada_vol']
xrp.columns = ['date','xrp_price','xrp_pct_chng','xrp_vol']
doge.columns = ['date','doge_price','doge_pct_chng','doge_vol']


#creating a combined df for further analysis
crypto_list = [btc,eth,ada,xrp,doge]

closing_prices= reduce(lambda  left,right: pd.merge(left,right,on=['date'],
                                            how='outer'), crypto_list)


closing_prices
closing_prices.isnull().any()


