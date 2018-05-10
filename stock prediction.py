from pandas_datareader import data as web
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import fix_yahoo_finance as yf
yf.pdr_override()
data = web.get_data_yahoo('NKE', start = "2017-04-11", end = "2018-04-11")
data.to_csv('output_NKE.csv')
data.head()

