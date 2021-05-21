# -*- coding: utf-8 -*-
"""
Created on Fri May 21 12:46:05 2021

@author: govind
"""

#Importing libraries for EDA 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

#Importing data
eth = pd.read_csv('./datasets/Ethereum Historical Data.csv')
btc = pd.read_csv('./datasets/BTC-USD.csv')
eos = pd.read_csv('./datasets/EOS-USD.csv')
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


fig.subplots_adjust(left=0.1,
                    bottom=0.1, 
                    right=0.9, 
                    top=0.9, 
                    wspace=0.4, 
                    hspace=0.4)

plt.tight_layout()
%config InlineBackend.figure_format = 'svg'

eth['close']=eth['Price']
eth['pct_chng']=eth['Change %']
eth['vol']=eth['Vol.']

eth_cleaned=eth.drop(eth.iloc[:,1:7], axis = 1)

eth_cleaned




eth_cleaned.to_csv('./datasets/eth.csv')

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

#taking a look at the data types
btc.info()

#plotting close, percentage change and volume for bitcoin
fig, (ax1,ax2,ax3) = plt.subplots(3,1)

ax1.plot(btc['Date'],btc['Close'])
ax2.plot(btc['Date'],btc['Change %'],color = 'g')
ax3.plot(btc['Date'],btc['Volume'],color = 'r')


fig.subplots_adjust(left=0.1,
                    bottom=0.1, 
                    right=0.9, 
                    top=0.9, 
                    wspace=0.4, 
                    hspace=0.4)

plt.tight_layout()
%config InlineBackend.figure_format = 'svg'

#removing all columns that are not required and renaming for easy use.
btc['close']=btc['Close']
btc['pct_chng']=btc['Change %']
btc['vol']=btc['Volume']

btc_cleaned=btc.drop(btc.iloc[:,1:8], axis = 1)

btc_cleaned

#creating a new dataset for cleaned file
btc_cleaned.to_csv('./datasets/btc.csv')

#Checking doge data
doge

#looking at datatype and nuill values
doge.info()

# a function with a for loop to fill missing values with forward fill ie. the previous value
def fill_missing_val(x):
        for col in x:
            x[col].fillna(method='ffill',inplace = True)
        return   x.isnull().any()


#creating a new function to clean data
def crypto_cleaner(x):
    x['Change %']= x['Close'].pct_change()
    x['Change %'].fillna(method = 'bfill',inplace = True)
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
    %config InlineBackend.figure_format = 'svg'
    plt.show()

#creating a function to drop unnecessary data
def crypto_dropper(x):
    x['close']=x['Close']
    x['pct_chng']=x['Change %']
    x['vol']=x['Volume']

    x.drop(x.iloc[:,1:8], axis = 1, inplace=True)

    return x

#creating a function to combine previous 3 functions
def crypto_processor(x):
    fill_missing_val(x)
    crypto_cleaner(x)
    crypto_plotter(x)
    crypto_dropper(x)
    return x

#Processing and saving dogecoin
crypto_processor(doge)
doge.to_csv('./datasets/doge.csv')

#processing and saving eos
crypto_processor(eos)
eos.to_csv('./datasets/eos.csv')

#processing and saving cardano
crypto_processor(ada)
ada.to_csv('./datasets/ada.csv')

#Can process more by adding yahoo data to datasets folder and running the processing function.
