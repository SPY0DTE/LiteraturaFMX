import pandas as pd
import pyodbc
import os
from datetime import date
from datetime import datetime,timedelta

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

