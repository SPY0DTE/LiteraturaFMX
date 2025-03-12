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

def PrecioCanasta(Cuenta,Tracker,Sentido,Motor,ParOpcional): 
    DIRECCIONAL=Cuenta
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
    DIRRECCIONALComp=DIRRECCIONALC[DIRRECCIONALC["Symbol"]!=Tracker]
    DIRRECCIONALComp=DIRRECCIONALComp[DIRRECCIONALComp["Symbol"]!=ParOpcional]
    CanastasLlevadas=(DIRRECCIONALComp[SizeModo].sum())/Componentes
    Monto=DIRRECCIONALComp[SizeModo]*DIRRECCIONALComp[PrecioModo]
    PrecioTotal=(Monto.sum()+CanastasLlevadas*Cash)/(CanastasLlevadas*Size)
   
    return PrecioTotal,CanastasLlevadas,DIRRECCIONALComp

def DolaresCuenta(Cuenta,Fecha):
    stored_proc_name ="DataAnalisysGetFXByAccount"
    Arbitrajes=Cuenta # No se da con "000" solo dar los 4 digitos, ie 1785
    Date=Fecha # Es una fecha que se da en formato "2025-01-31"
    conn = pyodbc.connect('DRIVER={SQL Server};SERVER=120.23.2.48;DATABASE=receptor;UID=DataAnalysis;PWD=DataAnalysisPassword')
    query = f"EXEC {stored_proc_name}'{Arbitrajes}','{Date}'"
 #   query2 = f"EXEC {stored_proc_name}'{Arbitrajes}'"
    DOLARES=pd.read_sql_query(query, conn)
    conn.close()
    return DOLARES



"EJEMPOS"
#PrecioCanasta("0100001787","MEXTRAC09","COMPRA","Asigna","QVGMEX18")
#PrecioCanasta("0100001787","MEXTRAC09","VENTA","Asigna","QVGMEX18")




