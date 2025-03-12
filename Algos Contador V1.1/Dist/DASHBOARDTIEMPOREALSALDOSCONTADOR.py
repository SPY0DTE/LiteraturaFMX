from tkinter import *
from tkinter import ttk
import tkinter as tk
from datetime import datetime
import pandas as pd
import pyodbc
import os
import time
import io
from playsound import playsound #Funciona con la 1.2.2
#

def Enteros(x):
    w=x
    try:
        float(w)
    except:
        w=x
    else:
        w=float(x)
    return(w)  
def Lado(x):
    W=x
    if W[0:3]=="BUY":
        x="VENTA"
    else:
        x="COMPRA"
    return(x)
# Function to update the label with the current time
def update_time():
    
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    Dia=str(datetime.today().day)
    MesPrueba=datetime.today().month
    if MesPrueba<10:
        Mes="0"+str(datetime.today().month)
    else:
        Mes=str(datetime.today().month)
    Ano=str(datetime.today().year)
    Blotter="BLOTER UCITS DASHBOARD "+Dia+Mes+Ano+".xlsx"
    Direccion=os.getcwd()
    Modo=pd.read_excel(Direccion+"\\Modo.xlsx")
    Motor="Operado "+Modo["Modo a operar"][0]
    UCITS= '0100001785'
    ARBITRAJES= '0100051797'
    stored_proc_name1 = 'DataAnalisysGetMatchFixVsAsignaByAccount'
    UCITSIZES=pd.read_excel(Direccion+"\\SALDOS UCITS\\UCITS SIZES.xlsx")
    UCITSIZES.reset_index(drop=True,inplace=True)     
    try:
        with open(Direccion+"\\UCITS\\"+Blotter,"rb") as f:
            file_io_obj=io.BytesIO(f.read())
           
        df_input_file = pd.read_excel(file_io_obj, engine='openpyxl', sheet_name=None)
        RawDashboard=df_input_file["Hoja1"]
        
    except:
        time.sleep(1)
        with open(Direccion+"\\UCITS\\"+Blotter,"rb") as f:
            file_io_obj=io.BytesIO(f.read())
        df_input_file = pd.read_excel(file_io_obj, engine='openpyxl', sheet_name=None)
        RawDashboard=df_input_file["Hoja1"]
        
    else:
        time.sleep(1)
        with open(Direccion+"\\UCITS\\"+Blotter,"rb") as f:
            file_io_obj=io.BytesIO(f.read())
        df_input_file = pd.read_excel(file_io_obj, engine='openpyxl', sheet_name=None)
        RawDashboard=df_input_file["Hoja1"]
    
    # with open(Direccion+"\\UCITS\\"+Blotter,"rb") as f:
    #     file_io_obj=io.BytesIO(f.read())
    # file_io_obj=io.BytesIO(f.read())
    # df_input_file = pd.read_excel(file_io_obj, engine='openpyxl', sheet_name=None)
    # RawDashboard=df_input_file["Hoja1"]

    
    
        

    #file=pd.ExcelFile(Direccion+"\\UCITS\\"+Blotter) #Abrimos el Excel donde llevo mis operaciones, Como estamos trabajando con un programa recurrente aveces cuando guardo el archivo este coincide con la ejecucion del programa lo que hace que se rompa
    #RawDashboard=file
    #file.close()
    
    
    Remanentes=pd.read_excel(Direccion+"\\SALDOS UCITS\\REMANENTES UCITS.xlsx") #Arbimos los remanentes que tenemos
    Remanentes.set_index("Symbol",inplace=True)
    INDX=RawDashboard["Indices"]
    Separadores=[]
    for i in RawDashboard.index:
        if RawDashboard["Indices"][i]==">":
            Separadores.append(i)
            
    RawDashboard=RawDashboard[["SECURITY","SIDE","SHARES","FX","PRICE (USD)","TOTAL USD","Mensaje"]]  
    RawDashboard=RawDashboard.applymap(Enteros)#Quiero convertir los numeros a enterso y lo demas dejarlo igual
    DF1C=RawDashboard[Separadores[0]:Separadores[1]].applymap(Enteros) #Ucits normales
    W=DF1C["SHARES"]*DF1C["PRICE (USD)"]
    DF1C=DF1C.join(W.rename("Monto"))   
    DF2C=RawDashboard[Separadores[2]:Separadores[3]+1].applymap(Enteros) #Ucits en pesos          En este bloque de codigo lo que hacemos es partir todo entre compras y ventas
    W=DF2C["SHARES"]*DF2C["PRICE (USD)"]                               #
    DF2C=DF2C.join(W.rename("Monto"))    
    DF3C=RawDashboard[Separadores[4]:Separadores[5]].applymap(Enteros) #Otros UCITS
    W=DF3C["SHARES"]*DF3C["PRICE (USD)"]
    DF3C=DF3C.join(W.rename("Monto"))    
    DF4V=RawDashboard[Separadores[6]:Separadores[7]].applymap(Enteros) #Ucits normales
    W=DF4V["SHARES"]*DF4V["PRICE (USD)"]
    DF4V=DF4V.join(W.rename("Monto"))    
    DF5V=RawDashboard[Separadores[8]:Separadores[9]].applymap(Enteros) #Ucits en pesos
    W=DF5V["SHARES"]*DF5V["PRICE (USD)"]
    DF5V=DF5V.join(W.rename("Monto"))    
    DF6V=RawDashboard[Separadores[10]:Separadores[11]].applymap(Enteros) #Otros Ucits
    W=DF6V["SHARES"]*DF6V["PRICE (USD)"]
    DF6V=DF6V.join(W.rename("Monto"))
    conn = pyodbc.connect('DRIVER={SQL Server};SERVER=120.23.2.48;DATABASE=receptor;UID=DataAnalysis;PWD=DataAnalysisPassword')
    query = f"EXEC {stored_proc_name1}'{UCITS}'"
    df1 = pd.read_sql_query(query, conn)
    query = f"EXEC {stored_proc_name1}'{ARBITRAJES}'"
    Arbitrajes= pd.read_sql_query(query, conn)
    conn.close()
    df1.set_index("Symbol", inplace=True)
    Ucits=df1[df1[Motor]>0] #Ucits es lo que pasa en la base de datos de FINAMEX TOMAMOS ASIGNA
    ComprasArbitrajes=Arbitrajes[Arbitrajes["Sentido"]=="COMPRA"]
    ComprasTotalesArbitrajeMexico=ComprasArbitrajes[Motor].sum()
    VentasArbitrajes=Arbitrajes[Arbitrajes["Sentido"]=="VENTA"]
    VentasTotalesArbitrajesMexico=VentasArbitrajes[Motor].sum()
    TotalesArbitraje=ComprasTotalesArbitrajeMexico+VentasTotalesArbitrajesMexico
    TextoArbitrajes="Total 51797: "+str(TotalesArbitraje)

    #Tabla=json.dumps(UcitDash.to_dict())
    CheckCPAS=pd.concat([DF1C,DF2C,DF3C]).groupby("SECURITY").sum()
    CheckCPAS["SIDE"]=CheckCPAS["SIDE"].apply(Lado)
    CheckCPAS=CheckCPAS[CheckCPAS["SHARES"]>=0]
    UcitsCompras=Ucits[Ucits["Sentido"]=="COMPRA"]
    UcitsVentas=Ucits[Ucits["Sentido"]=="VENTA"]
    ################PONDERACIONES########################################
    ##################VENTAS#############################################
    PonderadoraVTA=pd.concat([DF4V,DF5V,DF6V])
    PonderadoraVTA=PonderadoraVTA[PonderadoraVTA["Mensaje"]=="EU"]
    PonderadoraVTA=PonderadoraVTA[PonderadoraVTA["SHARES"]>0]
    W=PonderadoraVTA["FX"]*PonderadoraVTA["SHARES"]
    PonderadoraVTA=PonderadoraVTA.join(W.rename("FXAPONDERAR"))
    W=PonderadoraVTA["PRICE (USD)"]*PonderadoraVTA["SHARES"]
    PonderadoraVTA=PonderadoraVTA.join(W.rename("PRECIOAPONDERAR"))         
    PonderadoraVTA=PonderadoraVTA.groupby("SECURITY").sum()
    W=PonderadoraVTA["FXAPONDERAR"]/PonderadoraVTA["SHARES"]
    PonderadoraVTA=PonderadoraVTA.join(W.rename("Dollis Ponderados"))
    W=PonderadoraVTA["PRECIOAPONDERAR"]/PonderadoraVTA["SHARES"]
    PonderadoraVTA=PonderadoraVTA.join(W.rename("Precio Ponderado"))
    PonderadoraVTA=PonderadoraVTA[["SHARES","Dollis Ponderados","Precio Ponderado"]]
    PonderadoraVTA["SIDE"]="Venta"
    PonderadoraVTA["PreciosMex"]=0
    for i in UcitsCompras.index:    
        W=UcitsCompras["PPP Asigna"][i]
        PonderadoraVTA.loc[i,"PreciosMex"]=W
    PonderadoraVTA["Precio Ponderado Con Comision"]=PonderadoraVTA["Precio Ponderado"]-.002
    PonderadoraVTA["Precio en Pesos"]=PonderadoraVTA["Precio Ponderado Con Comision"]*PonderadoraVTA["Dollis Ponderados"]
    PonderadoraVTA["P&L"]=PonderadoraVTA["SHARES"]*(-PonderadoraVTA["PreciosMex"]+PonderadoraVTA["Precio en Pesos"])

    #PonderadoraVTA.to_excel(Direccion+"\\PONDERACIONES\\VentasPonderadas.xlsx")
    ###########COMPRAS#############################
    PonderadoraCPA=pd.concat([DF1C,DF2C,DF3C])
    PonderadoraCPA=PonderadoraCPA[PonderadoraCPA["Mensaje"]=="EU"]
    PonderadoraCPA=PonderadoraCPA[PonderadoraCPA["SHARES"]>0]
    W=PonderadoraCPA["FX"]*PonderadoraCPA["SHARES"]
    PonderadoraCPA=PonderadoraCPA.join(W.rename("FXAPONDERAR"))
    W=PonderadoraCPA["PRICE (USD)"]*PonderadoraCPA["SHARES"]
    PonderadoraCPA=PonderadoraCPA.join(W.rename("PRECIOAPONDERAR"))         
    PonderadoraCPA=PonderadoraCPA.groupby("SECURITY").sum()
    W=PonderadoraCPA["FXAPONDERAR"]/PonderadoraCPA["SHARES"]
    PonderadoraCPA=PonderadoraCPA.join(W.rename("Dollis Ponderados"))
    W=PonderadoraCPA["PRECIOAPONDERAR"]/PonderadoraCPA["SHARES"]
    PonderadoraCPA=PonderadoraCPA.join(W.rename("Precio Ponderado"))
    PonderadoraCPA=PonderadoraCPA[["SHARES","Dollis Ponderados","Precio Ponderado"]]
    PonderadoraCPA["SIDE"]="Compra"
    PonderadoraCPA["PreciosMex"]=0
    for i in UcitsVentas.index:    
        W=UcitsVentas["PPP Asigna"][i]
        PonderadoraCPA.loc[i,"PreciosMex"]=W
    
    PonderadoraCPA["Precio Ponderado Con Comision"]=PonderadoraCPA["Precio Ponderado"]+.002
    PonderadoraCPA["Precio en Pesos"]=PonderadoraCPA["Precio Ponderado Con Comision"]*PonderadoraCPA["Dollis Ponderados"]
    PonderadoraCPA["P&L"]=PonderadoraCPA["SHARES"]*(PonderadoraCPA["PreciosMex"]-PonderadoraCPA["Precio en Pesos"])

    PonderadosTotales=pd.concat([PonderadoraCPA,PonderadoraVTA])
    PonderadosTotalesRes=PonderadosTotales[PonderadosTotales["PreciosMex"]>0]
    PonderadosTotales=PonderadosTotales[PonderadosTotales["SHARES"]!="nan"]
    PonderadosTotales.dropna(axis=0,how="any",inplace=True)
    PonderadosTotales.to_excel(Direccion+"\\PONDERACIONES\\UCITJAM.xlsx")
    ResultadoCuenta="Resultado: $"+str(round(PonderadosTotalesRes["P&L"].sum()))
    
    #PonderadoraCPA.to_excel(Direccion+"\\PONDERACIONES\\ComprasPonderadas.xlsx")
    CheckVTAS=pd.concat([DF4V,DF5V,DF6V]).groupby("SECURITY").sum()
    CheckVTAS["SIDE"]=CheckVTAS["SIDE"].apply(Lado)
    CheckVTAS=CheckVTAS[CheckVTAS["SHARES"]>0]
    
    ############################################################
    PosicionesActuales=Remanentes["Operado"]
    
    # Vamos a sumar los operados de hoy a las posiciones actuales de los remanentes"
    # UcitsCompras=Ucits[Ucits["Sentido"]=="COMPRA"]
    # UcitsVentas=Ucits[Ucits["Sentido"]=="VENTA"]
    # Antes de sumar todo, queremos crear un indice con todos los elementos de las posiciones actuales y lo operado en el fix
    INDX1=UcitsCompras.index.tolist()          #SERIA VENDER EN EUROPA
    INDX2=UcitsVentas.index.tolist() # SERIA COMPRAR EN EUROPA
    INDX3=PosicionesActuales.index.tolist()
    #De los indices sacamos todos y los pasamos a una lista de python, ahora vamos a crear la lista final
    INDXFinal=set(INDX1+INDX2+INDX3)
    SIZESPORCUBRIRCPAS=[]
    NamesCPAS=[]
    SIZESPORCUBRIRVTAS=[]
    NamesVTAS=[]
    
    Modo="Operado Asigna" #Elegimos el modo 
    
    
    ### Totales de compras a realizar####
    for j in INDXFinal:
        if j in INDX2:   
            for k in INDX2:
                if j==k:
                    try:
                        Remanentes.loc[j,"Operado"]
                    except:
                        W=UcitsVentas.loc[j,Motor]
                        SIZESPORCUBRIRCPAS.append(W)
                        NamesCPAS.append(j)
                        
                    else:
                        if Remanentes.loc[j,"Operado"]<=0:
                            SumaTemp=-Remanentes.loc[j,"Operado"]
                        else:
                            SumaTemp=0 
                        W=SumaTemp+UcitsVentas.loc[j,Motor]
                        SIZESPORCUBRIRCPAS.append(W)
                        NamesCPAS.append(j)
        else:
            try:
                Remanentes.loc[j,"Operado"]
            except:
                pass
            else:    
                if Remanentes.loc[j,"Operado"]<0:
                    W=-Remanentes.loc[j,"Operado"]
                    SIZESPORCUBRIRCPAS.append(W)
                    NamesCPAS.append(j)
        
        
    for j in INDXFinal:
        if j in INDX1:   
            for k in INDX1:
                if j==k:
                    try:
                        Remanentes.loc[j,"Operado"]
                    except:
                        W=UcitsCompras.loc[j,Motor]
                        SIZESPORCUBRIRVTAS.append(W)
                        NamesVTAS.append(j)
                    else:
                        if Remanentes.loc[j,"Operado"]>=0:
                            SumaTemp=Remanentes.loc[j,"Operado"]
                        else:
                            SumaTemp=0
                        W=SumaTemp+UcitsCompras.loc[j,Motor]
                        SIZESPORCUBRIRVTAS.append(W)
                        NamesVTAS.append(j)
        else:
            try:
                Remanentes.loc[j,"Operado"]
            except:
                pass
            else:
                if Remanentes.loc[j,"Operado"]>0:   
                    W=Remanentes.loc[j,"Operado"]
                    SIZESPORCUBRIRVTAS.append(W)
                    NamesVTAS.append(j)
                    
                        
    ComprasTotalesUcits={"Name":NamesCPAS,"Size":SIZESPORCUBRIRCPAS}
    VentasTotalesUcits={"Name":NamesVTAS,"Size":SIZESPORCUBRIRVTAS}
    ComprasFinales=pd.DataFrame(ComprasTotalesUcits) #El total de lo que vas a comprar/vender
    VentasFinales=pd.DataFrame(VentasTotalesUcits) #El total de lo que vas a comprar/vender
    ComprasFinales.set_index("Name",inplace=True,drop=True) 
    VentasFinales.set_index("Name",inplace=True,drop=True)    
    ComprasFinalesINDX=ComprasFinales.index.tolist()
    CheckCPASINDX=CheckCPAS.index.tolist()
    VentasFinalesINDX=VentasFinales.index.tolist()
    CheckVTASINDX=CheckVTAS.index.tolist()
    CheckCPASINDXFaltantes=list(set(ComprasFinalesINDX)-set(CheckCPASINDX))
    FaltantesCpas=dict.fromkeys(CheckCPASINDXFaltantes,0)
    CheckVTASINDXFaltantes=list(set(VentasFinalesINDX)-set(CheckVTASINDX))
    FaltantesVtas=dict.fromkeys(CheckVTASINDXFaltantes,0)
    
    CheckCPASINDXFaltantes
    CheckVTASINDXFaltantes
    
    DFCPASFaltantes=pd.DataFrame(FaltantesCpas.items(),columns=["SECURITY","SHARES"])
    DFVTASFaltantes=pd.DataFrame(FaltantesVtas.items(),columns=["SECURITY","SHARES"])
    DFCPASFaltantes.set_index("SECURITY",inplace=True,drop=True) 
    DFVTASFaltantes.set_index("SECURITY",inplace=True,drop=True) 
    CheckCPASFinal=pd.concat([CheckCPAS,DFCPASFaltantes])
    CheckVTASFinal=pd.concat([CheckVTAS,DFVTASFaltantes]) 
    DiferenciasCompras=[]
    NameUCITCpa=[]
    DiferenciasVentas=[]
    NameUCITVta=[]
    
    for i in ComprasFinales.index:
        for k in CheckCPASFinal.index:
            if i==k:
                DifTemp=ComprasFinales.loc[k,"Size"]-CheckCPASFinal.loc[k,"SHARES"]
                DiferenciasCompras.append(DifTemp)
                NameUCITCpa.append(i)
    for i in VentasFinales.index:
        for k in CheckVTASFinal.index:
            if i==k:
                DifTemp=VentasFinales.loc[k,"Size"]-CheckVTASFinal.loc[k,"SHARES"]
                DiferenciasVentas.append(DifTemp)
                NameUCITVta.append(i)
   
    
   #Pasamos Todo a un dataframe para imprimirl
    w={"UCIT":NameUCITCpa,"Size":DiferenciasCompras}
    DFrameCompras=pd.DataFrame(w)
    DFrameCompras["Sentido"]="COMPRA"
    w={"UCIT":NameUCITVta,"Size":DiferenciasVentas}
    DFrameVentas=pd.DataFrame(w)                  
    DFrameVentas["Sentido"]="VENTA"
    UcitsMenores=["IBTAN","LQDAN","IHYAN","EWSPN","SDIAN"]
    
    ComprasPrint=DFrameCompras[DFrameCompras["Size"]>=50].sort_values(by="Size",ascending=False)
    ComprasPrintMenos50=DFrameCompras[DFrameCompras["Size"]<50].sort_values(by="Size",ascending=False)
    VentasPrint=DFrameVentas[DFrameVentas["Size"]>=50].sort_values(by="Size",ascending=False)
    VentasPrintMenos50=DFrameVentas[DFrameVentas["Size"]<50].sort_values(by="Size",ascending=False)    
    TextoCPAS1=""
    TextoCPAS1Menos50=""
    TextoVTAS1=""
    TextoVTAS1Menos50=""
    Sonido=Direccion+"\\mixkit-hard-pop-click-2364.wav"
    for i in ComprasPrint.index:
        Wtext="Comprar"+" "+str(DFrameCompras.loc[i,"UCIT"])+":"+str(DFrameCompras.loc[i,"Size"])+"\n"
        TextoCPAS1=TextoCPAS1+Wtext
        if DFrameCompras.loc[i,"UCIT"] not in UcitsMenores and DFrameCompras.loc[i,"Size"]>100:
            playsound(Sonido)
        else:
            if DFrameCompras.loc[i,"Size"]>500:
                playsound(Sonido)
                
        
             
            
            
        
    for i in VentasPrint.index:
        Wtext="Vender"+" "+str(DFrameVentas.loc[i,"UCIT"])+":"+str(DFrameVentas.loc[i,"Size"])+"\n"
        TextoVTAS1=TextoVTAS1+Wtext
        if DFrameVentas.loc[i,"UCIT"] not in UcitsMenores and DFrameVentas.loc[i,"Size"]>100:
            playsound(Sonido)
        else:
            if DFrameVentas.loc[i,"Size"]>500:
                playsound(Sonido)
            
            
    
    for i in ComprasPrintMenos50.index:
        Wtext="Comprar"+" "+str(DFrameCompras.loc[i,"UCIT"])+":"+str(DFrameCompras.loc[i,"Size"])+"\n"
        TextoCPAS1Menos50=TextoCPAS1Menos50+Wtext
    for i in VentasPrintMenos50.index:
        Wtext="Vender"+" "+str(DFrameVentas.loc[i,"UCIT"])+":"+str(DFrameVentas.loc[i,"Size"])+"\n"
        TextoVTAS1Menos50=TextoVTAS1Menos50+Wtext
        
    
        
    #ALGOS# 
    # Schedule the update_time function to be called again after 1000 milliseconds (1 second)
    stored_proc_name = 'DataAnalisysGetAlgosByAccount'# Nombre del store procedure
    UCITS= '0100001785' #Nombre de la cuenta
    conn = pyodbc.connect('DRIVER={SQL Server};SERVER=120.23.2.48;DATABASE=receptor;UID=DataAnalysis;PWD=DataAnalysisPassword')
    query = f"EXEC {stored_proc_name}'{UCITS}'"
    ALGOSUCITS= pd.read_sql_query(query, conn)
    #ALGOSUCITS.set_index("F55_SYMBOL",drop=True,inplace=True)
    #############################################################
    
    #############################################################
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
    ##################################
    VivosCompras=ALGOSUCITSLiveCompras["F55_SYMBOL"].drop_duplicates().reset_index(drop=True)
    VivosVentas=ALGOSUCITSLiveVentas["F55_SYMBOL"].drop_duplicates().reset_index(drop=True)
    ##############################
    MuertosCompras=ALGOSUCITSDeadCompras["F55_SYMBOL"].drop_duplicates().reset_index(drop=True)
    MuertosVentas=ALGOSUCITSDeadVentas["F55_SYMBOL"].drop_duplicates().reset_index(drop=True)
        ###############################
    ComprasFaltantes=set(MuertosCompras)-set(VivosCompras)
    VentasFaltantes=set(MuertosVentas)-set(VivosVentas)
    
    ComprasFaltantesString=""
    VentasFaltantesString=""

    
    
    for i in ComprasFaltantes:
        ComprasFaltantesString=ComprasFaltantesString+i+"\n"
    
    for i in ComprasFaltantes:
        ComprasFaltantesStringM=ComprasFaltantesString+i+"\n"
    
    
        
        
    
    ###############################
    
    ComprasVivas="Algos de compra Vivos: "+str(len(VivosCompras))
    VentasVivas="Algos de venta Vivos: "+str(len(VivosVentas))
    
    if len(ComprasFaltantes)>0:
        W1="Se tiene que dar refill de compra a los siguientes UCITs: "+str(ComprasFaltantes)
    else:
        W1="No hay refills pendientes de compra"
    
    if len(VentasFaltantes)>0:
        W2="Se tiene que dar refill de venta a los siguientes UCITs: "+str(VentasFaltantes)
    else:
        W2="No hay refills pendientes de venta"
    ComprasDelDia=""
    for j in ComprasFinales.index:
        ComprasDelDia=ComprasDelDia+j+" "+str(ComprasFinales.loc[j,"Size"])+"\n"
    
    VentasDelDia=""
    for j in VentasFinales.index:
        VentasDelDia=VentasDelDia+j+" "+str(VentasFinales.loc[j,"Size"])+"\n"
    
    AlgosVivosCPAS.config(text=ComprasVivas,foreground="green",font="bold")
    AlgosVivosVTAS.config(text=VentasVivas,foreground="red",font="bold")
    Hora.config(text=current_time,foreground="mediumpurple",font=("Arial",12,"bold"))
    
    ArbitrajesCheck.config(text=TextoArbitrajes,foreground="mediumpurple",font=("Arial",12,"bold"))
    Resultado.config(text=ResultadoCuenta,foreground="mediumpurple",font=("Arial",12,"bold"))
    
    VentasFaltantesTextMas50.delete("1.0",END) 
    ComprasFaltantesTextMas50.delete("1.0",END)
    VentasFaltantesTextMenos50.delete("1.0",END) 
    ComprasFaltantesTextMenos50.delete("1.0",END)
    AlgosFaltantesCPAText.delete("1.0",END)
    AlgosFaltantesVTAText.delete("1.0",END)
    ComprasFaltantesTextMas50.insert("1.0",TextoCPAS1)
    ComprasFaltantesTextMenos50.insert("1.0",TextoCPAS1Menos50)
    VentasFaltantesTextMas50.insert("1.0",TextoVTAS1)
    VentasFaltantesTextMenos50.insert("1.0",TextoVTAS1Menos50)   
    AlgosFaltantesCPAText.insert("1.0",ComprasFaltantesString)
    AlgosFaltantesVTAText.insert("1.0",VentasFaltantesString)
    #Esto se actualiza cada minuto con el fin de poder tener tiempo para revisar la info de la pantalla
    ComprasFinales1.delete("1.0",END)
    VentasFinales1.delete("1.0",END)
    ComprasFinales1.insert('1.0',ComprasDelDia)
    VentasFinales1.insert("1.0",VentasDelDia) 
   # TextoCPAS1
    #TextoVTAS1    
    root.after(1000, update_time)

# Create the main window
root = Tk()
content = ttk.Frame(root)
FrameCompras = ttk.Frame(content, borderwidth=5, relief="ridge", width=200, height=100) #Donde estan las compras Totales
FrameVentas =ttk.Frame(content, borderwidth=5, relief="ridge", width=200, height=100)
FrameAlgosPendientes=ttk.Frame(content, borderwidth=5, relief="ridge", width=100, height=100)
FrameAlgosPendientesVentas=ttk.Frame(content, borderwidth=5, relief="ridge", width=100, height=100)
FrameHora=ttk.Frame(content,borderwidth=5, relief="ridge", width=100, height=100)
FrameComprasAcubrir=ttk.Frame(content, borderwidth=5, relief="ridge", width=300, height=100)
FrameVentasAcubrir=ttk.Frame(content, borderwidth=5, relief="ridge", width=300, height=100)

ComprasFinales1=ttk.Label(FrameCompras,text="Compras Finales")
VentasFinales1=ttk.Label(FrameVentas,text="Algos Ventas Finales")
#Texto=Text(FrameAlgosPendientes,height=12,width=12,cursor="arrow")
ComprasFinales1=Text(FrameCompras,height=5,width=25,cursor="arrow")
VentasFinales1=Text(FrameVentas,height=5,width=25,cursor="arrow")
ComprasFaltantesTextMas50=Text(FrameComprasAcubrir,height=5,width=25,cursor="arrow",bg="gold") #Aqui se elige el tamaño y los colores del dashboard
ComprasFaltantesTextMenos50=Text(FrameComprasAcubrir,height=5,width=25,cursor="arrow",bg="goldenrod") #Aqui se elige el tamaño y los colores del dashboard
VentasFaltantesTextMas50=Text(FrameVentasAcubrir,height=5,width=25,cursor="arrow",bg="deepskyblue")
VentasFaltantesTextMenos50=Text(FrameVentasAcubrir,height=5,width=25,cursor="arrow",bg="dodgerblue")
AlgosFaltantesCPAText=Text(FrameAlgosPendientes,height=5,width=25,cursor="arrow",bg="gold")
AlgosFaltantesVTAText=Text(FrameAlgosPendientesVentas,height=5,width=25,cursor="arrow",bg="deepskyblue")
Resultado=ttk.Label(content,text="P&L 1785: ")


HeaderCompras=ttk.Label(FrameCompras,text="Compras Totales")
HeaderVentas=ttk.Label(FrameVentas,text="VentasTotales")
HeaderComprasPendientes=ttk.Label(FrameComprasAcubrir,text="Compras Pendientes")
HeaderVentasPendientes=ttk.Label(FrameVentasAcubrir,text="Ventas Pendientes")
HeaderAlgosPendientes=ttk.Label(FrameAlgosPendientes,text="Algos de compra Pendientes")
HeaderAlgosPendientesVentas=ttk.Label(FrameAlgosPendientesVentas,text="Algos de venta Pendientes")



#Texto.insert("1.0",'VMCAX\nVMSTX\nVHYAN\nVDPA\nVJPA\nRFQE\nEQOB\nMAINECRAFT\nNVIDA\nETF\nFINAMEX\nGBM\nMORGAN STANLEY\nGOOGL')
#Texto.delete("1.0",END)
#Texto["state"]="disabled" #Desactiva el texto :) asi no puedes modificarlo
#ComprasFinales1.insert('1.0', 'VMCAX 12\nVMSTX 24\nVHYAN 47\nGOOGL 12511')
#ComprasFinales1["state"]="disabled" #Desactiva el texto :) asi no puedes modificarlo
#VentasFinales1.insert('1.0', 'VMCAX 12\nVMSTX 24\nVHYAN 47\nGOOGL 12511')
#VentasFinales1["state"]="disabled" #Desactiva el texto :) asi no puedes modificarlo
#ComprasFaltantes["state"]="disabled" #Desactiva el texto :) asi no puedes modificarlo
#VentasFaltantes["state"]="disabled" #Desactiva el texto :) asi no puedes modificarlo
name = ttk.Entry(content)
AlgosVivosCPAS=ttk.Label(content,text="Algos de compras Vivos: ")
AlgosVivosVTAS=ttk.Label(content,text="Algos de venta Vivos: ")
Hora=ttk.Label(content,text="Hora :o")
ArbitrajesCheck=ttk.Label(content,text="Arbitrajes")


content.grid(column=0, row=0) # Es el frame

FrameCompras.grid(column=3, row=5, columnspan=3, rowspan=2) #Lo que hace esto es construirlo en dos partes
FrameVentas.grid(column=3, row=7, columnspan=3, rowspan=2) #Lo que hace esto es construirlo en dos partes

FrameAlgosPendientes.grid(column=6,row=5,columnspan=3,rowspan=2)
FrameAlgosPendientesVentas.grid(column=6,row=7,columnspan=3,rowspan=2)

FrameComprasAcubrir.grid(column=2,row=14,columnspan=3,rowspan=2)
FrameVentasAcubrir.grid(column=2,row=18,columnspan=3,rowspan=2)

#Texto.grid()
HeaderCompras.grid()
HeaderVentas.grid()
HeaderAlgosPendientes.grid()
HeaderAlgosPendientesVentas.grid()
HeaderComprasPendientes.grid()
HeaderVentasPendientes.grid()
ComprasFinales1.grid()
VentasFinales1.grid()
ComprasFaltantesTextMas50.grid()
ComprasFaltantesTextMenos50.grid()
VentasFaltantesTextMas50.grid()
VentasFaltantesTextMenos50.grid()

AlgosFaltantesCPAText.grid()
AlgosFaltantesVTAText.grid()

AlgosVivosCPAS.grid(column=3,row=0,columnspan=3,rowspan=1)
AlgosVivosVTAS.grid(column=3,row=1,columnspan=3,rowspan=1)
Hora.grid(column=7,row=1)
Resultado.grid(column=7,row=4)
ArbitrajesCheck.grid(column=7,row=0)
#AlgosPendientes.grid(column=4,row=0)
#####################################################################################
# Start the time update function for the first time
update_time()
root.attributes("-topmost",True)
root.mainloop()
