"THE BROGING BACK-TESTER"
import random
import pandas as pd
from scipy.stats import bernoulli
import yfinance as yf
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import math

def ResultadoPorVelaFinal(O,C):#Calcula cuantas veces ha harbido arriba y cuantas abajo en una ventada de tiempo
    if C-O>0:
        x=1
    else:
        x=0
    return(x)

Variable="SPY"
Ticker=yf.Ticker(Variable)
Ventana="1Y"#1Y, 5d,1MO
Data=Ticker.history(Ventana) #Informacion Diaria A una ventana de tiempo.
Data=Data.reset_index()
Dist=[]
for i in Data.index:
    if Data["Close"][i]-Data["Open"][i]>0:
        Dist.append(1)       
    else:
        Dist.append(0)
Total=len(Dist)
Arriba=Dist.count(1)
Abajo=Dist.count(0)
Theta=Arriba/Total

Titulos=1
Portafolios=[]
Proporcion=[]
for a in range(1000):
    Evolucion=[]
    Portafolio=10000
    for i in Data.index:
        Operacion=random.choice(["LONG","SHORT"])
        if Operacion=="LONG":
            Portafolio=Portafolio+Titulos*(Data["Close"][i]-Data["Open"][i])
            print("Comprando a apertura y tu P&L es de ",Data["Close"][i]-Data["Open"][i])
            Evolucion.append(Portafolio)
        else:
            Portafolio=Portafolio-Titulos*(Data["Close"][i]-Data["Open"][i])
            print("Vendiendo a Cierre y tu P&L es de ",-Data["Close"][i]+Data["Open"][i])
            Evolucion.append(Portafolio)
    plt.scatter(Data.index,Evolucion)
    plt.show()
    Proporcion.append(Portafolio/1000-1)
Acumulada=[]
for i in Proporcion:
    Acumulada.append(math.floor(i))

    
    #Portafolios.append(Portafolio)
Proporcion.sort()
#a=range(1,1000)
#plt.scatter(a,Portafolios)