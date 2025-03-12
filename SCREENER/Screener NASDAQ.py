import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import plotly.figure_factory as ff
import plotly.offline as pyo
Universe=pd.read_excel("TICKER UNIVERSE.xlsx")["Symbol"]
pyo.init_notebook_mode()
Req=100000000
Filter=[]
for i in Universe:
    Tick=yf.Ticker(i)
    HistM_Vol=Tick.history(period="1mo")["Volume"].mean()
    HistM_Price=Tick.history(period="1mo")["Close"].mean()
    Parametro=HistM_Vol*HistM_Price
    if Parametro>Req:
        Filter.append(i)

