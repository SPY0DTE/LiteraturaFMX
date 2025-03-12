# -*- coding: utf-8 -*-
"""
Created on Fri Jun  9 10:51:19 2023

@author: fvfentanes
"""

import mplfinance as mpf
#import yfinance as yf
import pandas as pd
#spyder=yf.Ticker("SPY")
#Data=spyder.history()
Data=pd.read_excel("PrecioSPYBB.xlsx")
Data.index = pd.DatetimeIndex(Data['Date'])
#Data.index.name = 'Date'
Data.head(3)
Data.tail(3)
mpf.plot(Data,type="candle", volume=True)


