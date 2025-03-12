import tkinter as tk
from datetime import datetime
import pandas as pd
import pyodbc
import os
from playsound import playsound
from openpyxl import Workbook
# Function to update the label with the current time
def update_time():
    Dir=os.getcwd()
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    # Schedule the update_time function to be called again after 1000 milliseconds (1 second)
    stored_proc_name = 'DataAnalisysGetAlgosByAccount'# Nombre del store procedure
    UCITS= '0100001785' #Nombre de la cuenta
    conn = pyodbc.connect('DRIVER={SQL Server};SERVER=120.23.2.48;DATABASE=receptor;UID=DataAnalysis;PWD=DataAnalysisPassword')
    query = f"EXEC {stored_proc_name}'{UCITS}'"
    ALGOSUCITS= pd.read_sql_query(query, conn)
    #ALGOSUCITS.set_index("F55_SYMBOL",drop=True,inplace=True)
    ALGOSUCITS=ALGOSUCITS[ALGOSUCITS["ORDER STATUS"]!="REJECTED"]
    ALGOSUCITS=ALGOSUCITS[ALGOSUCITS["ORDER STATUS"]!="CANCELED"]
    ALGOSUCITSDead=ALGOSUCITS[ALGOSUCITS["ORDER STATUS"]=="FILLED"]
    ALGOSUCITSLive=ALGOSUCITS[ALGOSUCITS["ORDER STATUS"]!="FILLED"]
    ########################################################
    ALGOSUCITSDeadCompras=ALGOSUCITSDead[ALGOSUCITS["SIDE"]=="BUY"]
    ALGOSUCITSDeadVentas=ALGOSUCITSDead[ALGOSUCITS["SIDE"]=="SELL"]
    ###########################################################
    ALGOSUCITSLiveCompras=ALGOSUCITSLive[ALGOSUCITS["SIDE"]=="BUY"]
    ALGOSUCITSLiveVentas=ALGOSUCITSLive[ALGOSUCITS["SIDE"]=="SELL"]
    #################################
    ALGOSUCITSLiveComprasBMV=ALGOSUCITSLiveCompras[ALGOSUCITSLiveCompras["EXCHANGE"]=="XMEX"]
    ALGOSUCITSLiveVentasBMV=ALGOSUCITSLiveVentas[ALGOSUCITSLiveVentas["EXCHANGE"]=="XMEX"]
    
    ALGOSUCITSLiveComprasBIVA=ALGOSUCITSLiveCompras[ALGOSUCITSLiveCompras["EXCHANGE"]=="BIVA"]
    ALGOSUCITSLiveVentasBIVA=ALGOSUCITSLiveVentas[ALGOSUCITSLiveVentas["EXCHANGE"]=="BIVA"]
    ##################################
    
    AlgosAmandar=pd.read_excel(Dir+"\\UCITSAMANDAR.xlsx")
    AlgosAmandarBRKBIVA=AlgosAmandar[AlgosAmandar["CLIENTE"]=="BKRK"]
    
    ##################################
    VivosComprasBMV=ALGOSUCITSLiveComprasBMV["F55_SYMBOL"].drop_duplicates().reset_index(drop=True)
    VivosVentasBMV=ALGOSUCITSLiveVentasBMV["F55_SYMBOL"].drop_duplicates().reset_index(drop=True)
    
    VivosComprasBIVA=ALGOSUCITSLiveComprasBIVA["F55_SYMBOL"].drop_duplicates().reset_index(drop=True)
    VivosVentasBIVA=ALGOSUCITSLiveVentasBIVA["F55_SYMBOL"].drop_duplicates().reset_index(drop=True)
    ##############################
    
    MuertosCompras=ALGOSUCITSDeadCompras["F55_SYMBOL"].drop_duplicates().reset_index(drop=True)
    MuertosVentas=ALGOSUCITSDeadVentas["F55_SYMBOL"].drop_duplicates().reset_index(drop=True)
        ###############################
    
    ComprasFaltantesBMV=set(AlgosAmandar["UCIT"])-set(VivosComprasBMV)
    VentasFaltantesBMV=set(AlgosAmandar["UCIT"])-set(VivosVentasBMV)
    ComprasFaltantesBIVA=set(AlgosAmandarBRKBIVA["UCIT"])-set(VivosComprasBIVA)
    VentasFaltantesBIVA=set(AlgosAmandarBRKBIVA["UCIT"])-set(VivosVentasBIVA)
    ###############################

    
    ComprasVivas="Algos de compra Vivos: "+str(len(VivosComprasBMV)+len(VivosComprasBIVA))
    VentasVivas="Algos de venta Vivos: "+str(len(VivosVentasBMV)+len(VivosVentasBIVA))
    
    if len(ComprasFaltantesBMV)>0:
        W1="Se tiene que dar refill de compra a los siguientes UCITs en BMV: "+str(ComprasFaltantesBMV)
        playsound('mixkit-winning-swoosh-2017.wav')
    else:
        W1="No hay refills pendientes de compra en BMV"
    if len(ComprasFaltantesBIVA)>0:
        W2="Se tiene que dar refill de compra a los siguientes UCITs en BIVA: "+str(ComprasFaltantesBIVA)
        playsound('mixkit-system-beep-buzzer-fail-2964.wav')
    else:
        W2="No hay refills pendientes de compra en BIVA"
        
        
    if len(VentasFaltantesBMV)>0:
        W3="Se tiene que dar refill de venta a los siguientes UCITs en BMV: "+str(VentasFaltantesBMV)
        playsound('mixkit-winning-swoosh-2017.wav')
    else:
        W3="No hay refills pendientes de venta en BMV"
    if len(VentasFaltantesBIVA)>0:
        W4="Se tiene que dar refill de compra a los siguientes UCITs en BIVA: "+str(VentasFaltantesBIVA)
        playsound('mixkit-system-beep-buzzer-fail-2964.wav')
    else:
        W4="No hay refills pendientes de venta en BIVA"
        
    
        
    
    label.config(text=current_time) #Hora actual
    lbl1.config(text=ComprasVivas) #Numero de algos que estan vivos de compra
    lblfaltantesComprasBMV.config(text=W1) 
    lblfaltantesComprasBIVA.config(text=W2) 
    lbl2.config(text=VentasVivas)#Numero de algos que estan vivos de Venta
    lblfaltantesVentasBMV.config(text=W3)
    lblfaltantesVentasBIVA.config(text=W4)

    
    root.after(1000, update_time)
# Create the main window
root = tk.Tk()
root.title("Dashboard UCITs")
# Create a label to display the time
#####################################################################################

label = tk.Label(root, font=('Helvetica', 13), fg='black')
lbl1=tk.Label(root,text="Algos de Compra vivos: ",font=("Arial",13,"bold"),fg="green")
lblfaltantesComprasBMV=tk.Label(root,text="Algos de Compra vivos: ",font=("Arial",13,"bold"),fg="green")
lblfaltantesComprasBIVA=tk.Label(root,text="Algos de Compra vivos: ",font=("Arial",13,"bold"),fg="green")
lbl2=tk.Label(root,text="Algos de Venta vivos: ",font=("Arial",13,"bold"),fg="red")
lblfaltantesVentasBMV=tk.Label(root,text="Algos de Compra vivos: ",font=("Arial",13,"bold"),fg="red")
lblfaltantesVentasBIVA=tk.Label(root,text="Algos de Compra vivos: ",font=("Arial",13,"bold"),fg="red")

####################################################################################
label.pack()
lbl1.pack()
lblfaltantesComprasBMV.pack()
lblfaltantesComprasBIVA.pack()
lbl2.pack()
lblfaltantesVentasBMV.pack()
lblfaltantesVentasBIVA.pack()
#####################################################################################


# Start the time update function for the first time
update_time()
root.attributes("-topmost",True)
root.geometry("500x200")
# Start the Tkinter event loop 
root.mainloop()