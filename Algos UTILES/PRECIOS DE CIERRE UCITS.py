import pandas as pd
import pyodbc
import os
from datetime import date
from datetime import datetime,timedelta
stored_proc_name = 'DataAnalisysGetClosePxUCITs'
W="16/12/2024 "+"10:30:00:00"
conn = pyodbc.connect('DRIVER={SQL Server};SERVER=120.23.2.48;DATABASE=receptor;UID=DataAnalysis;PWD=DataAnalysisPassword')
query = f"EXEC {stored_proc_name}"
PRECIOSCIERRE= pd.read_sql_query(query, conn)
conn.close()
PRECIOSCIERRE.to_excel("PRECIOSCIERRE.xlsx")


