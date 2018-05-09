from pandas_datareader import data as web
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import fix_yahoo_finance as yf

yf.pdr_override()
data = web.get_data_yahoo('NKE', start = "2017-04-11", end = "2018-04-11")
data.to_csv('output_NKE.csv')
data.head()

NKE = pd.read_csv('output_NKE.csv', sep = ',', header = 0, index_col = 0, parse_dates = True)
days = (NKE.index[-1] - NKE.index[0]).days
mu = (((NKE['Adj Close'][-1] / NKE['Adj Close'][1])) ** (252.0/days))-1

NKE['Returns'] = NKE['Adj Close'].pct_change()
sigma = NKE['Returns'].std()*(252.0**0.5)

n = 60
dt = 1/60
S0 = NKE['Adj Close'][-1]

for i in range(5):
    dRt = mu*dt + sigma*np.random.normal(0,dt,(1,n))*(252**0.5)
    St = S0*(1 + dRt.cumsum())
    plt.plot(St)

plt.xlabel("Time(day)")
plt.ylabel("Stock Price")
plt.title("60 Days Stock Price Prediction")
plt.show()

print(days)
print("Mean of Return rate = ",mu)
print("Volatility(Standard deviation)of Return rate = ",sigma)
