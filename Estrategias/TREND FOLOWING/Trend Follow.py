#TREND FOLOWING#
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import plotly.offline as pyo
import numpy as np
from matplotlib import pyplot
pyo.init_notebook_mode(connected=True)

df=pd.read_excel("SPY_Minute_Data.xlsx")
df.columns=["Time","Op3n","High","Low","Clos3","Volum3"] #Definimos las columnas
#Vamos a checar si hay valors con volumen cero para quitarlos
#Con la data que he sacado, creo que no deberiamos de tener ese problema pero 
#Por cualquier cosa es bueno quitarlo
df=df[df["Volum3"]!=0]
df.reset_index(drop=True, inplace=True)
df.isna().sum()
df.head(10)
#El siguiente codigo es solo para ver como se ve la info y graficarla
dfpl=df[10000:10200]
fig=go.Figure(data=[go.Candlestick(x=dfpl.index,
                                   open=dfpl["Op3n"],
                                   high=dfpl["High"],
                                   low=dfpl["Low"],
                                   close=dfpl["Clos3"])])
fig.show()
backcandles=50 #Numero de velas que nos vamos a ir hacia atrás para ver la tend
wind=5 # Van a ser como los pasos
candleid=8800 #El numero de la vela que vamo a analizar, esto solo es para una
#Tenemos que hacerlo dinamico
#Vamos a ir creando arrays vacios y ahi vamos a ir metiendo los minimos de cada ventana

maxim=np.array([])#
minim=np.array([])#
xxmin=np.array([])#
xxmax=np.array([])#

#Elijes el id de la vela y te vas atras entonces ya tienes tu rango
#Despues vas llenando en los arrays vacios el minimo valor y ese lo obtienes con loc
#Y con iloc vas a obtener el numero de vela que es, esto lo vas a necesitar para depues
#Ajustar un polinomio de grado 1 
for i in range(candleid-backcandles,candleid+1,wind):
    minim=np.append(minim, df.Low.loc[i:i+wind].min())
    xxmin=np.append(xxmin,df.Low.iloc[i:i+wind].idxmin())
for i in range(candleid-backcandles,candleid+1,wind):
    maxim=np.append(maxim, df.High.loc[i:i+wind].max())
    xxmax=np.append(xxmax,df.High.iloc[i:i+wind].idxmax())
#Ajustando el polinomio 
slmin,itercmin=np.polyfit(xxmin,minim,1)
slmax,intercmax=np.polyfit(xxmax,maxim,1)
dfpl=df[candleid-backcandles:candleid+backcandles]
fig = go.Figure(data=[go.Candlestick(x=dfpl.index,
                                     open=dfpl["Op3n"],
                                     high=dfpl["High"],
                                     low=dfpl["Low"],
                                     close=["Clos3"])])

fig.add_trace(go.Scatter(x=xxmin,y=slmin*xxmin+itercmin,mode="lines",name="Min Slope"))
fig.add_trace(go.Scatter(x=xxmax,y=slmax*xxmax+intercmax,mode="lines",name="Max Slope"))


#Falta aun hacer las mejoras pendientes 







