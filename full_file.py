#   Analysis - v0.1
#  author- Govind1997

##############################################################################
####################### IMPORTING ALL REQUIRED PACKAGES ######################
##############################################################################

#Importing all required packages
from pandas_datareader import data as pdr
from datetime import date
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf
from functools import reduce
from sklearn.preprocessing import MinMaxScaler
from scipy import stats
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

##############################################################################
###############IMPORTING AND CLEANING ALL THE REQUIRED DATA ##################
##############################################################################

#just 10 lines of code to import and clean all the necessary data
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

##############################################################################
################ CREATING A COMBINED DF WITH ALL THE VALUES ##################
##############################################################################

#renaming the columns to make combining easier
btc.columns= ['date','btc_price','btc_pct_chng','btc_vol']
eth.columns = ['date','eth_price','eth_pct_chng','eth_vol']
ada.columns = ['date','ada_price','ada_pct_chng','ada_vol']
xrp.columns = ['date','xrp_price','xrp_pct_chng','xrp_vol']
doge.columns = ['date','doge_price','doge_pct_chng','doge_vol']


#creating a combined df for further analysis
crypto_list = [btc,eth,ada,xrp,doge]

combined_prices= reduce(lambda  left,right: pd.merge(left,right,on=['date'],
                                            how='outer'), crypto_list)
combined_prices.head(5)

#creating a plot for percentage Change
plt.figure(figsize = (20,10))
plt.bar(combined_prices.date,combined_prices.btc_pct_chng)
plt.bar(combined_prices.date,combined_prices.eth_pct_chng)
plt.bar(combined_prices.date,combined_prices.ada_pct_chng)
plt.bar(combined_prices.date,combined_prices.xrp_pct_chng)
plt.bar(combined_prices.date,combined_prices.doge_pct_chng)
plt.legend(['Bitcoin','Etherium','Cardano','Ripple','Doge'])
plt.title('Crypto currency percentage Change')

#creating a plot for volume
plt.figure(figsize = (20,10))
plt.bar(combined_prices.date,combined_prices.btc_vol)
plt.bar(combined_prices.date,combined_prices.eth_vol)
plt.bar(combined_prices.date,combined_prices.ada_vol)
plt.bar(combined_prices.date,combined_prices.xrp_vol)
plt.bar(combined_prices.date,combined_prices.doge_vol)
plt.yscale('log')
plt.legend(['Bitcoin','Etherium','Cardano','Ripple','Doge'])
plt.title('Crypto currency volumes')

#creating plot to compare closing prices
plt.figure(figsize = (20,10))
plt.plot(combined_prices.date,combined_prices.btc_price)
plt.plot(combined_prices.date,combined_prices.eth_price)
plt.plot(combined_prices.date,combined_prices.ada_price)
plt.plot(combined_prices.date,combined_prices.xrp_price)
plt.plot(combined_prices.date,combined_prices.doge_price)
plt.legend(['Bitcoin','Etherium','Cardano','Ripple','Doge'])
plt.title('Crypto currency prices')



##############################################################################
####################     SCALING THE combined_prices     ######################
##############################################################################

#creating an index with just the prices for scaling
combined_prices_index = combined_prices.loc[:,['btc_price','eth_price',
                                            'ada_price','xrp_price',
                                            'doge_price']]

#Using MinMaxScaler to scale the prices between 0 and 1
scaler= MinMaxScaler()
print(scaler.fit(combined_prices_index))
scaled_prices = scaler.transform(combined_prices_index)
scaled_prices = pd.DataFrame(scaled_prices)

#naming the columns of the new data frame
scaled_prices.columns = ['btc_price','eth_price',
                        'ada_price','xrp_price',
                        'doge_price']

#adding date to the beginning of the new scaled prices
scaled_prices['date'] = combined_prices.date
first_column = scaled_prices.pop('date')
scaled_prices.insert(0,'date',first_column)
scaled_prices

#Plotting the scaled prices
plt.figure(figsize = (20,10))
plt.plot(scaled_prices.date,scaled_prices.btc_price)
plt.plot(scaled_prices.date,scaled_prices.eth_price)
plt.plot(scaled_prices.date,scaled_prices.ada_price)
plt.plot(scaled_prices.date,scaled_prices.xrp_price)
plt.plot(scaled_prices.date,scaled_prices.doge_price)
plt.legend(['Bitcoin','Etherium','Cardano','Ripple','Doge'])
plt.title('Cryptocurrency prices - Scaled then normalized')
#Findings- All crypto currencies seem to be correlated in some way but XRP and DOGE has some Change
#that are different from the others lets dig deeper

##############################################################################
###################      CORRELATION ANALYSIS     ############################
##############################################################################

#Setting up correlation and creating a Heatmap
plt.figure(figsize = (10,10))
crypto_corr = combined_prices_index.corr(method = 'pearson').round(2)
sns.heatmap(data = crypto_corr,
            cmap = 'inferno',
            square = True,
            annot = True,
            linecolor = 'black',
            linewidths = 0.5)

plt.title("""
Linear Correlation Heatmap for cryto currency prices
""")
plt.show()

#findings - XRP and doge are least correlated to BTC
#         - eth and ADA  are the most correlated.
#         - eth has the highest correlation with the other cryptos
#         - eth has more than 80% correlation with all other crypto in the portfolio

#pairplot for comparing
sns.pairplot(data = combined_prices,
             x_vars = ['eth_price', 'doge_price', 'xrp_price', 'ada_price'],
             y_vars = ['btc_price'],
             kind = 'scatter',
             palette = 'plasma')

sns.pairplot(data = combined_prices,
             x_vars = ['btc_price', 'doge_price', 'xrp_price', 'ada_price'],
             y_vars = ['eth_price'],
             kind = 'scatter',
             palette = 'plasma')
#findings - as we can see here etherium clearly has a less scattered correlation
#with the other cryptos in my portfolio

#Regression plots for etherium
fig, ((ax1, ax2), (ax3, ax4))= plt.subplots(nrows=2,ncols = 2, figsize= (12,8))
sns.regplot(x='eth_price',y='doge_price',data = combined_prices, ax = ax1)
sns.regplot(x='eth_price',y='btc_price',data = combined_prices, ax = ax2)
sns.regplot(x='eth_price',y='xrp_price',data = combined_prices, ax = ax3)
sns.regplot(x='eth_price',y='ada_price',data = combined_prices, ax = ax4)
fig.suptitle('Regression plots for etherium and other crypto currencies')
plt.show()
#There seems to be a linear relationship between etherium and the other cryptos


combined_prices.head(5)
