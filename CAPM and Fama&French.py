## Portfolio Management Project

# It creates a three & five factors model for a given stock using Fama and French models

import datetime 
from datetime import timedelta
import matplotlib.pyplot as plt 
import numpy as np
import pandas as pd
import pandas_datareader.data as web # enter data module
import statsmodels.formula.api as sm # regression module
from statsmodels.iolib.summary2 import summary_col # data presentation mode


f_f_model = web.DataReader('F-F_Research_Data_5_Factors_2x3_daily', 'famafrench')[0] # download Fama and French Data
f_f_model.rename(columns={'Mkt-RF': 'MKT'}, inplace=True) # Rename 
f_f_model = f_f_model /100 # Divide by 100 because we had percentages
start = str(datetime.date.today()-datetime.timedelta(days=2190)) # start date 6 years ago which is 365 days * 6 years
today = str(datetime.date.today()) # today as end date
ticker_name = input("Please give a valid Yahoo Finance Ticker for a Stock: ") # User choice for a stock
data =web.get_data_yahoo(ticker_name,start,today) # Download date from Yahoo Finance
def price2ret(prices,retType='simple'): #Function from prices to percentages
    """
    This converts prices to arithmetic or log returns
    """
    if retType == 'simple':
        ret = (prices/prices.shift(1))-1
    else:
        ret = np.log(prices/prices.shift(1))
    return ret
data['Returns'] = price2ret(data[['Adj Close']]) 
data = data.dropna() # Take out non available
sd = f_f_model.index[0] # First Day of Fama and French
datestr_start = sd.strftime("%Y-%m-%d") # time stamp to string
n = f_f_model.shape[0] 
ed = f_f_model.index[n-1] # Last day of Fama & French
datestr_end = ed.strftime("%Y-%m-%d") 
data = data[datestr_start:datestr_end] #now the have the same number of rows
df_stock_factor = pd.merge(data,f_f_model,left_index=True,right_index=True) # Thus they could be merged
df_stock_factor['XsRet'] = df_stock_factor['Returns'] - df_stock_factor['RF'] #Finds Risk Premium and Risk Free
# Least Square Regression 
CAPM = sm.ols(formula = 'XsRet ~ MKT', data=df_stock_factor).fit(cov_type='HAC',cov_kwds={'maxlags':1}) 
FF3 = sm.ols( formula = 'XsRet ~ MKT + SMB + HML', data=df_stock_factor).fit(cov_type='HAC',cov_kwds={'maxlags':1})
FF5 = sm.ols( formula = 'XsRet ~ MKT + SMB + HML + RMW + CMA', data=df_stock_factor).fit(cov_type='HAC',cov_kwds={'maxlags':1})
CAPMtstat = CAPM.tvalues
FF3tstat = FF3.tvalues
FF5tstat = FF5.tvalues

CAPMcoeff = CAPM.params
FF3coeff = FF3.params
FF5coeff = FF5.params
# DataFrame with Statistical Results
results_df = pd.DataFrame({'CAPMcoeff':CAPMcoeff,'CAPMtstat':CAPMtstat,
                            'FF3coeff':FF3coeff, 'FF3tstat':FF3tstat,
                            'FF5coeff':FF5coeff, 'FF5tstat':FF5tstat},
index = ['Intercept', 'MKT', 'SMB', 'HML', 'RMW', 'CMA'])

# Format data

dfoutput = summary_col([CAPM,FF3, FF5],stars=True,float_format='%0.4f',
            model_names=['CAPM','FF3','FF5'],
            info_dict={'N':lambda x: "{0:d}".format(int(x.nobs)),
                        'Adjusted R2':lambda x: "{:.4f}".format(x.rsquared_adj)}, 
                        regressor_order = ['Intercept', 'MKT', 'SMB', 'HML', 'RMW', 'CMA'])

print(dfoutput)

# Regression variables
FF3 = results_df["FF3coeff"] 
FF5 = results_df["FF5coeff"]

# T-test and P - Value Test
if CAPMtstat[1] > 1.646:
    print("Rexp-Rf = ", str(CAPMcoeff[1]) ,"* Risk Premium")
else:
    print("Beta of CAPM not statistically significant")

	for i in range (1,4):
    if FF3tstat[i] < 1.646:
        FF3[i] = 0

print("Rexp-Rf = ", str(FF3[1]) ,"*Risk Premium+(",str(FF3[2]),")* SMB +(",str(FF3[3]),")* HML")
for i in range (1,6):
    if FF5tstat[i] < 1.646:
        FF5[i] = 0

print("Rexp-Rf = ", str(FF5[1]) ,"*Risk Premium+(",str(FF5[2]),")* SMB +(",str(FF5[3]),")* HML+(",str(FF5[4]),")*RMW+(",str(FF5[5]),")*CMA")

