# -*- coding: utf-8 -*-
"""
Created on Fri May 21 12:46:05 2021

@author: govin
"""

#Importing libraries for EDA 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np



#Importing data
eth = pd.read_csv('./datasets/Ethereum Historical Data.csv')
btc = pd.read_csv('./datasets/BTC-USD.csv')
eos = pd.read_csv('./datasets/EOS-USD .csv')
doge = pd.read_csv('./datasets/DOGE-USD.csv')
ada = pd.read_csv('./datasets/ADA-USD.csv')

#Taking a look at data for etherium
eth


#Checking to seee if there are any missing values
eth.isnull().any()

#Checking to see the data types of each column
eth.info()

#replacing the K and M in 'vol.' column to 0**3 and 0**6 to convert the dtype to float
eth['Vol.'] = eth['Vol.'].replace('-','0')

eth['Vol.'] = (eth['Vol.'].replace(r'[KM]+$', '', regex=True).astype(float) * eth['Vol.'].str.extract(r'[\d\.]+([KM]+)', expand=False).fillna(1).replace(['K','M'], [10**3, 10**6]).astype(int))


#changing the date column from a object to datetime
eth.Date = eth.Date.astype('datetime64')


#Creating a function to easily replace vlaues and make changes to columns.
def value_to_float(x):
    if type(x) == float or type(x) == int:
        return x
    if 'K' in x:
        if len(x) > 1:
            return float(x.replace('K', '')) * 1000
        return 1000.0
    if 'M' in x:
        if len(x) > 1:
            return float(x.replace('M', '')) * 1000000
        return 1000000.0
    if 'B' in x:
        return float(x.replace('B', '')) * 1000000000
    
    if '%' in x:
        return float(x.replace('%','')) / 100

eth['Change %'] = eth['Change %'].apply(value_to_float)

#checking if the function worked
eth.info()

#Plotting the close, Volume and pct. change of ETH

fig, (ax1,ax2,ax3) = plt.subplots(3,1)


ax1.plot(eth['Date'],eth['Price'])
ax2.plot(eth['Date'],eth['Change %'],color = 'g')
ax3.plot(eth['Date'],eth['Vol.'],color = 'r')

ax1.title.set_text('ETH price')
ax2.title.set_text('ETH Change %')
ax3.title.set_text('ETH Volume')

fig.subplots_adjust(left=0.1,
                    bottom=0.1, 
                    right=0.9, 
                    top=0.9, 
                    wspace=0.4, 
                    hspace=0.4)


plt.tight_layout()
%config InlineBackend.figure_format = 'svg'

#calling bittorrent data
btc 
    


#Checking data type
btc.info()

btc.isnull().any()

#Checking where we have null values
btc.iloc[:,1:6][btc['Close'].isnull()]


# a function with a for loop to fill missing values with forward fill ie. the previous value
def fill_missing_val(x):
        for col in x:
            x[col].fillna(method='ffill',inplace = True)
        return   x.isnull().any()

        
fill_missing_val(btc)


#creating a percentage change column
btc['Change %']= btc['Close'].pct_change()
btc['Change %']

#backwards filling for the first missing value in percentage change
btc['Change %'].fillna(method = 'bfill',inplace = True)
btc['Change %']

#changing date to date time format
btc.Date = btc.Date.astype('datetime64')

btc.info()


fig, (ax1,ax2,ax3) = plt.subplots(3,1)

ax1.plot(btc['Date'],btc['Close'])
ax2.plot(btc['Date'],btc['Change %'],color = 'g')
ax3.plot(btc['Date'],btc['Volume'],color = 'r')
ax1.title.set_text('BTC price')
ax2.title.set_text('BTC Change %')
ax3.title.set_text('BTC Volume')


fig.subplots_adjust(left=0.1,
                    bottom=0.1, 
                    right=0.9, 
                    top=0.9, 
                    wspace=0.4, 
                    hspace=0.4)

plt.tight_layout()
%config InlineBackend.figure_format = 'svg'

