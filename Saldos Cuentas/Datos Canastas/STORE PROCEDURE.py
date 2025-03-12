import pandas as pd
import pyodbc
import os
from datetime import date
from datetime import datetime,timedelta
Data=pd.read_excel("Datos Canastas.xlsx").set_index("Name")
stored_proc_name = 'DataAnalisysGetMatchFixVsAsignaByAccount'
#"Cuenta 0100001796"

def String2Time(x):
    W="16/12/2024 "+x
    W=datetime.strptime(W,"%d/%m/%Y %H:%M:%S:%f")
    return(W)

def PrecioCanasta(Cuenta,Tracker,Sentido,Motor):
    DIRRECCIONAL=Cuenta
    conn = pyodbc.connect('DRIVER={SQL Server};SERVER=120.23.2.48;DATABASE=receptor;UID=DataAnalysis;PWD=DataAnalysisPassword')
    query = f"EXEC {stored_proc_name}'{DIRECCIONAL}'"
    CuentaDF= pd.read_sql_query(query, conn)
    conn.close()
    Componentes=Data.loc[Tracker]["Size"]
    Cash=Data.loc[Tracker]["Efectivo"]
    SizeModo="Operado "+Motor
    PrecioModo="PPP "+Motor
    Size=Data.loc[Tracker]["SIZES"]
    DIRRECCIONALC=CuentaDF[CuentaDF["Sentido"]==Sentido]
    DIRRECCIONALComp=DIRRECCIONALC[DIRRECCIONALC["Symbol"]==Tracker]
    CanastasLlevadas=(DIRRECCIONALComp[SizeModo].sum())/Componentes
    Monto=DIRRECCIONALComp[SizeModo]*DIRRECCIONALComp[PrecioModo]
    PrecioTotal=(Monto.sum()+CanastasLlevadas*Cash)/(CanastasLlevadas*Size)
    

    
    

    






#stored_proc_name = 'DataAnalisysGetMatchFixVsAsignaByAccountByTrade'
DIRECCIONAL= '0100001796'
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




