import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup


# # 1. The company I choose is "Alphabet Inc. (GOOG)". I collected its stock price from Oct 27, 2017 to Mar 22, 2018.

# In[2]:


def get_historical_data(name, number_of_days):
    data = []
    url = 'https://finance.yahoo.com/quote/' + name + '/history/'
    print('Download data from:', url)
    respond = requests.get(url)
    content = respond.text
    soup = BeautifulSoup(content, 'html.parser')
    rows = soup.findAll('table')[0].tbody.findAll('tr')

    for each_row in rows:
        divs = each_row.findAll('td')
        if divs[1].span.text  != 'Dividend': #Ignore this row in the table
            #I'm only interested in 'Open' price; For other values, play with divs[1 - 5]
            data.append({'Date': divs[0].span.text, 
                         'Open': float(divs[1].span.text.replace(',','')), 
                         'High': float(divs[2].span.text.replace(',','')), 
                         'Low': float(divs[3].span.text.replace(',','')), 
                         'Close': float(divs[4].span.text.replace(',','')), 
                        'Adj Close': float(divs[5].span.text.replace(',','')),
                        'Volume': float(divs[6].span.text.replace(',',''))})

    return data[:number_of_days]

data = []
for i in get_historical_data('GOOG', 100):
    data.append(i)
data.reverse()
df = pd.DataFrame(data)
df.to_csv('Google-Stock-Price.csv')
print('Save stock price as Google-Stock-Price.csv')
df = pd.read_csv('Google-Stock-Price.csv', sep=',',header=0,index_col=0, parse_dates=True)


# In[3]:


df.head()


# In[4]:


df.tail()


# In[5]:


df.shape


# # 2. The mean and std of its stock price is 0.000640 and 0.0146

# In[6]:


return_rate = []
for i in range(df.shape[0] - 1):
    return_rate.append((df['Close'][i + 1] - df['Close'][i]) / df['Close'][i])
    
std = np.std(return_rate)
mean = np.mean(return_rate)


# In[7]:


print('mean: ', mean, 'std: ', std)


# In[8]:


predicted_rr = [return_rate[-1]]
for t in range(1, 61):
    predicted_rr.append(predicted_rr[-1] + mean * 1 + std * np.sqrt(1) * np.random.normal())         

predicted_price = [df['Close'][df.shape[0]-1]]
for t in range(1, 61):
    predicted_price.append((1 + predicted_rr[t]) * predicted_price[t - 1]) 


# # 3. Following is the plot of predicted return rate and predicted stock price

# In[9]:


plt.figure(figsize=(12, 9))
plt.plot(predicted_rr, 'c')
plt.xlabel('day', fontsize=18)
plt.ylabel('return rate', fontsize=18)
plt.title('Plot of Predicted Return Rate', fontsize=24)
plt.show()


# In[10]:


plt.figure(figsize=(12, 9))
plt.plot(predicted_price, 'm')
plt.xlabel('day', fontsize=18)
plt.ylabel('stock price', fontsize=18)
plt.title('Plot of Predicted Stock Price', fontsize=24)
plt.show()
