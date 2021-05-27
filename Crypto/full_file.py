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

closing_prices= reduce(lambda  left,right: pd.merge(left,right,on=['date'],
                                            how='outer'), crypto_list)
closing_prices



#creating plot to compare closing prices
plt.plot(closing_prices.date,closing_prices.btc_price)
plt.plot(closing_prices.date,closing_prices.eth_price)
plt.plot(closing_prices.date,closing_prices.ada_price)
plt.plot(closing_prices.date,closing_prices.xrp_price)
plt.plot(closing_prices.date,closing_prices.doge_price)
plt.legend(['Bitcoin','Etherium','Cardano','Ripple','Doge'])
plt.show()

##############################################################################
####################     SCALING THE CLOSING_PRICES     ######################
##############################################################################

#creating an index with just the prices for scaling
closing_prices_index = closing_prices.loc[:,['btc_price','eth_price',
                                            'ada_price','xrp_price',
                                            'doge_price']]

#Using MinMaxScaler to scale the prices between 0 and 1
scaler= MinMaxScaler()
print(scaler.fit(closing_prices_index))
scaled_prices = scaler.transform(closing_prices_index)
scaled_prices = pd.DataFrame(scaled_prices)

#naming the columns of the new data frame
scaled_prices.columns = ['btc_price','eth_price',
                        'ada_price','xrp_price',
                        'doge_price']

#adding date to the beginning of the new scaled prices
scaled_prices['date'] = closing_prices.date
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

##############################################################################
###################      CORRELATION ANALYSIS     ############################
##############################################################################

crypto_corr = scaled_prices.corr(method = 'pearson').round(2)
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



sns.pairplot(data = closing_prices,
             x_vars = ['eth_price', 'doge_price', 'xrp_price', 'ada_price'],
             y_vars = ['btc_price'],
             kind = 'scatter',
             palette = 'plasma')

sns.pairplot(data = closing_prices,
             x_vars = ['btc_price', 'doge_price', 'xrp_price', 'ada_price'],
             y_vars = ['eth_price'],
             kind = 'scatter',
             palette = 'plasma')

plt.show()


sns.lmplot(x='eth_price',y='doge_price',data = closing_prices)







#                    ___________________________________¶¶¶¶          
#                    ________________________¶¶1¶¶_¶¶¶¶1111¶             
#                    _______________________¶¶111¶¶¶1111111¶             
#                    ___________________¶¶¶_¶1111¶¶1111111¶              
#                    ___________________¶11¶¶111¶¶111111¶¶               
#                    ___________________¶11¶1111¶111111¶¶                
#                    __________________¶¶11¶111¶111111¶¶                 
#                    __________________¶11¶111¶¶111111¶                  
#                    __________________¶11¶111¶1111111¶                  
#                    _________________¶11¶111¶11111111¶                  
#                    _________________¶1¶111¶¶1111111¶¶                  
#                    ________________¶1¶¶111¶1111111¶¶                   
#                    _______________¶¶1¶111¶1111111¶¶                    
#                    _______________¶¶¶111¶11111111¶                     
#                    ______________¶¶¶11¶¶111111111¶                     
#                    ______________¶¶11¶¶111111¶¶¶1¶¶                    
#                    _____________¶11¶¶1111111¶111111¶¶                  
#                    ___________¶¶¶¶¶1111111¶¶11111111¶¶¶                
#                    __________¶¶¶1111111¶¶1111111111111¶¶¶              
#                    _________¶¶111111¶¶¶11111111111111111¶¶¶¶           
#                    _________¶111111¶¶1111111111111111111111¶¶¶         
#                    _________¶111111¶1111111111¶¶¶1111111111111¶        
#                    ________¶11111111111111111¶¶_¶¶¶¶¶¶¶¶111111¶        
#                    _______¶¶111111111111111¶¶¶________¶111111¶¶        
#                    _______¶11111111111¶¶¶¶¶¶__________¶111111¶         
#                    ______¶¶11111111111¶¶_____________¶¶11111¶¶        
#                    ______¶111111111111¶______________¶¶11111¶         
#                    _____¶¶111111111111¶________________¶¶¶¶¶¶¶¶¶¶¶¶   
#                    _____¶1111111111111¶________________¶¶¶111111¶¶¶¶  
#                    _____¶1111111111111¶¶_____________¶¶¶111111¶¶¶11¶  
#                    ____¶¶1111111111111¶¶¶_________¶¶¶1111111¶¶11111¶  
#                    ____¶1111111111111111¶¶¶¶¶¶¶¶¶¶¶111111111¶1111¶¶ 
#                    ____¶111111111111111111¶¶¶¶11111111111111¶¶¶¶¶¶  
#                    ___¶111111111111111111111111111111111111111¶¶¶   
#                    __¶111111111111111111111111111111111111111¶¶     
#                    ¶¶11111111111111111111111111111111111111¶¶¶      
#                    111111111111111111111111111111111¶¶¶¶¶¶¶¶        
#                    111111111111111111111111111111¶¶¶¶               
#                   1111111111111111111111111111¶¶¶                  
#                   111111111111111111111111111¶¶                    
#                   1111111111111111111111111¶¶                      
#                   111111111111111111111111¶¶                       
#                   1111111111111111111111¶¶                         
#                   111111111111111111¶¶¶¶                           
#                    111111111¶¶¶¶¶¶¶¶¶¶                              
#                   111111¶¶¶                                        
#                   ¶¶¶¶¶¶¶






















