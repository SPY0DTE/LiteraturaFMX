import pandas as pd
import  pyodbc
stored_proc_name ="DataAnalisysGetFXByAccount"
Arbitrajes="51797"
conn = pyodbc.connect('DRIVER={SQL Server};SERVER=120.23.2.48;DATABASE=receptor;UID=DataAnalysis;PWD=DataAnalysisPassword')
query = f"EXEC {stored_proc_name}'{Arbitrajes}'"
DOLARES = pd.read_sql_query(query, conn)
conn.close()
print(DOLARES)
