import pandas as pd
import pyodbc
import yfinance as yf
from tkinter import *
from tkinter import ttk
import tkinter as tk
import os
from datetime import date
from datetime import datetime,timedelta
def String2Time(x):
    W="16/12/2024 "+x
    W=datetime.strptime(W,"%d/%m/%Y %H:%M:%S:%f")
    return(W)





stored_proc_name = 'DataAnalisysGetMatchFixVsAsignaByAccount'
W="16/12/2024 "+"10:30:00:00"
Ventana=datetime.strptime(W,"%d/%m/%Y %H:%M:%S:%f")
CASH=2910.20

#stored_proc_name = 'DataAnalisysGetMatchFixVsAsignaByAccountByTrade'
DIRECCIONAL= '0100001796'
conn = pyodbc.connect('DRIVER={SQL Server};SERVER=120.23.2.48;DATABASE=receptor;UID=DataAnalysis;PWD=DataAnalysisPassword')
query = f"EXEC {stored_proc_name}'{DIRECCIONAL}'"
DIRECCIONAL= pd.read_sql_query(query, conn)
conn.close()
SizeModo="Operado Asigna"
PrecioModo="PPP Asigna"
DIRRECCIONALC=DIRECCIONAL[DIRECCIONAL["Sentido"]=="COMPRA"]
DIRRECCIONALComp=DIRRECCIONALC[DIRRECCIONALC["Symbol"]!="ESGMEXISHRS"]
TamañoComponentes=51421
SizeTRACKER=50000
CanastasLlevadas=(DIRRECCIONALComp[SizeModo].sum())/TamañoComponentes
print("Llevamos: ",CanastasLlevadas)
Monto=DIRRECCIONALComp[SizeModo]*DIRRECCIONALComp[PrecioModo]
PrecioTotal=(Monto.sum()+CanastasLlevadas*CASH)/(CanastasLlevadas*SizeTRACKER)
print("Precio final: ",PrecioTotal)






# CASH=7415.48
# TamañoCanasta=100000
TamañoComponentes=122563
# DIRECCIONAL=DIRECCIONAL[DIRECCIONAL["Sentido"]=="VENTA"]
# DIRECCIONAL["Hora"]=DIRECCIONAL["Hora"].apply(String2Time)
# DIRECCIONALV=DIRECCIONAL[DIRECCIONAL["Hora"]>Ventana]

# SizeModo="Operado FIX"
# PrecioModo="PPP FIX"
# Monto=DIRECCIONAL[SizeModo]*DIRECCIONAL[PrecioModo]


