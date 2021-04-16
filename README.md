# CAPM, Fama And French Factors Models
 The implementation creates CAPM, a three &amp; five factors model for a given stock (you choose a ticker) using Fama and French models
 CAPM is a financial model that describes the relationship between systematic risk and expected return assets. CAPM is widely used throughout finance for pricing risky securities and generating expected returns for assets given the risk of those assets and cost of capital.(https://www.investopedia.com/terms/c/capm.asp). 
 As systematic risk we define the risk that cannot be further diversified. 
 
E(R) = rf + beta (rm - rf)
Where: rf is the risk free rate
       beta is the systematic risk 
       rm-rf is the risk premium
       
Fama and French Factors Model

Eugene Fama and Keneth French found out that CAPM is not the best model to describe the expected returns of a security as it does not model some behavioural patterns. They found out that there are 3 factors that are statistically important The "three factor" β is analogous to the classical β but not equal to it, since there are now two additional factors to do some of the work. SMB stands for "Small [market capitalization] Minus Big" and HML for "High [book-to-market ratio] Minus Low"; they measure the historic excess returns of small caps over big caps and of value stocks over growth stocks.

In 2015, Fama and French extended the model, adding a further two factors -- profitability and investment. Defined analogously to the HML factor, the profitability factor (RMW) is the difference between the returns of firms with robust (high) and weak (low) operating profitability; and the investment factor (CMA) is the difference between the returns of firms that invest conservatively and firms that invest aggressively. In the US (1963-2013), adding these two factors makes the HML factors redundant since the time series of HML returns are completely explained by the other four factors (most notably CMA which has a -0.7 correlation with HML).
