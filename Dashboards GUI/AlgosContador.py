import tkinter as tk
from datetime import datetime
import pandas as pd
import pyodbc
import os
from tkinter import scrolledtext


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
    Mes="0"+str(datetime.today().month)
    Ano=str(datetime.today().year)
    Blotter="BLOTER UCITS DASHBOARD "+Dia+Mes+Ano+".xlsx"
    Direccion=os.getcwd()
    UCITS= '0100001785'
    ARBITRAJES= '0100051797'
    stored_proc_name1 = 'DataAnalisysGetMatchFixVsAsignaByAccount'
    UCITSIZES=pd.read_excel(Direccion+"\\SALDOS UCITS\\UCITS SIZES.xlsx")
    UCITSIZES.reset_index(drop=True,inplace=True)
    RawDashboard=pd.read_excel(Direccion+"\\UCITS\\"+Blotter) #Abrimos el Excel donde llevo mis operaciones
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
    Ucits=df1[df1["Operado Asigna"]>0] #Ucits es lo que pasa en la base de datos de FINAMEX TOMAMOS ASIGNA
    
    #Tabla=json.dumps(UcitDash.to_dict())
    CheckCPAS=pd.concat([DF1C,DF2C,DF3C]).groupby("SECURITY").sum()
    CheckCPAS["SIDE"]=CheckCPAS["SIDE"].apply(Lado)
    CheckCPAS=CheckCPAS[CheckCPAS["SHARES"]>=0]
    
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
    PonderadoraVTA.to_excel(Direccion+"\\PONDERACIONES\\VentasPonderadas.xlsx")
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
    PonderadoraCPA.to_excel(Direccion+"\\PONDERACIONES\\ComprasPonderadas.xlsx")
    CheckVTAS=pd.concat([DF4V,DF5V,DF6V]).groupby("SECURITY").sum()
    CheckVTAS["SIDE"]=CheckVTAS["SIDE"].apply(Lado)
    CheckVTAS=CheckVTAS[CheckVTAS["SHARES"]>0]
    
    ############################################################
    PosicionesActuales=Remanentes["Operado"]
    # Vamos a sumar los operados de hoy a las posiciones actuales de los remanentes"
    UcitsCompras=Ucits[Ucits["Sentido"]=="COMPRA"]
    UcitsVentas=Ucits[Ucits["Sentido"]=="VENTA"]
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
    Modo="Operado FIX"
    ### Totales de compras a realizar####
    for j in INDXFinal:
        if j in INDX2:   
            for k in INDX2:
                if j==k:
                    try:
                        Remanentes.loc[j,"Operado"]
                    except:
                        W=UcitsVentas.loc[j,Modo]
                        SIZESPORCUBRIRCPAS.append(W)
                        NamesCPAS.append(j)
                        
                    else:
                        if Remanentes.loc[j,"Operado"]<=0:
                            SumaTemp=-Remanentes.loc[j,"Operado"]
                        else:
                            SumaTemp=0 
                        W=SumaTemp+UcitsVentas.loc[j,Modo]
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
                        W=UcitsCompras.loc[j,Modo]
                        SIZESPORCUBRIRVTAS.append(W)
                        NamesVTAS.append(j)
                    else:
                        if Remanentes.loc[j,"Operado"]>=0:
                            SumaTemp=Remanentes.loc[j,"Operado"]
                        else:
                            SumaTemp=0
                        W=SumaTemp+UcitsCompras.loc[j,Modo]
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
                    
                        
                        
       # elif j in INDX3:
        #    if Remanentes.loc[j,"Operado"]<0: 
         #       W=-Remanentes.loc[j,"Operado"]
          #      SIZESPORCUBRIRCPAS.append(W)
           #     NamesCPAS.append(j)
            
            #elif Remanentes.loc[j,"Operado"]>0: 
             #   W=Remanentes.loc[j,"Operado"]
              #  SIZESPORCUBRIRVTAS.append(W)
               # NamesVTAS.append(j)
        #else:
         #   if Remanentes.loc[j,"Operado"]<0: 
          #      W=-Remanentes.loc[j,"Operado"]
           #     SIZESPORCUBRIRCPAS.append(W)
            #    NamesCPAS.append(j)       

      ### Totales de ventas a realizar####
      #TEMPORAL "
    # for j in INDXFinal:
    #     if j in INDX1:   
    #         for k in INDX1:
    #             if j==k:
    #                 if Remanentes.loc[j,"Operado"]>=0:
    #                     SumaTemp=Remanentes.loc[j,"Operado"]
    #                 else:
    #                     SumaTemp=0
    #                 W=SumaTemp+UcitsCompras.loc[j,Modo]
    #                 SIZESPORCUBRIRVTAS.append(W)
    #                 NamesVTAS.append(j)
    #     else:
    #         if Remanentes.loc[j,"Operado"]>0: 
    #             W=Remanentes.loc[j,"Operado"]
    #             SIZESPORCUBRIRVTAS.append(W)
    #             NamesVTAS.append(j)
                
    #Creamos un dataframe que se encarga de mostrar tanto ventas como compras totales :)                        
    ComprasTotalesUcits={"Name":NamesCPAS,"Size":SIZESPORCUBRIRCPAS}
    VentasTotalesUcits={"Name":NamesVTAS,"Size":SIZESPORCUBRIRVTAS}
    ComprasFinales=pd.DataFrame(ComprasTotalesUcits)
    VentasFinales=pd.DataFrame(VentasTotalesUcits)
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
    FrameCompras=pd.DataFrame(w)
    FrameCompras["Sentido"]="COMPRA"
    w={"UCIT":NameUCITVta,"Size":DiferenciasVentas}
    FrameVentas=pd.DataFrame(w)                  
    FrameVentas["Sentido"]="VENTA"
    ComprasPrint=FrameCompras[FrameCompras["Size"]>25]
    VentasPrint=FrameVentas[FrameVentas["Size"]>25]
    TextoCPAS1=""
    TextoVTAS1=""
    for i in ComprasPrint.index:
        Wtext="Tienes que Comprar"+str(FrameCompras.loc[i,"UCIT"])+":"+str(FrameCompras.loc[i,"Size"])+"\n"
        TextoCPAS1=TextoCPAS1+Wtext
    for i in VentasPrint.index:
        Wtext="Tienes que Vender"+str(FrameVentas.loc[i,"UCIT"])+":"+str(FrameVentas.loc[i,"Size"])+"\n"
        TextoVTAS1=TextoVTAS1+Wtext   
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
    label.config(text=current_time)
    lbl1.config(text=ComprasVivas)
    lblfaltantesCompras.config(text=W1)
    lbl2.config(text=VentasVivas)
    lblfaltantesVentas.config(text=W2)
    lblCPAS.config(text=TextoCPAS1)
    #text_widget.config(text=TextoCPAS1)
    lblVTAS.config(text=TextoVTAS1)
    
    #TextoCPAS.insert(tk.END,TextoCPAS1)
    #TextoVTAS.insert(tk.END,TextoVTAS1)
    
    root.after(1000, update_time)
# Create the main window




root = tk.Tk()
root.title("Dashboard UCITs")
#FrameCPAS=tk.Frame(root)
#FrameVTAS=tk.Frame(root)
# Create a label to display the time
#####################################################################################
label = tk.Label(root, font=('Helvetica', 13), fg='black')
lbl1=tk.Label(root,text="Algos de Compra vivos: ",font=("Arial",13,"bold"),fg="green")
lblfaltantesCompras=tk.Label(root,text="Algos de Compra vivos: ",font=("Arial",13,"bold"),fg="green")
lbl2=tk.Label(root,text="Algos de Venta vivos: ",font=("Arial",13,"bold"),fg="red")
lblfaltantesVentas=tk.Label(root,text="Algos de Compra vivos: ",font=("Arial",13,"bold"),fg="red")
#TextoCPAS=tk.Text(root,bg="light yellow")
#TextoVTAS=tk.Text(root,bg="light cyan")
lblCPAS=tk.Label(root,text="Algos de Compra vivos: ",font=("Arial",10,"bold"),fg="green")
lblVTAS=tk.Label(root,text="Algos de Compra vivos: ",font=("Arial",10,"bold"),fg="red")

#T=tk.Text(root,height=25,width=50)
####################################################################################
label.pack()
lbl1.pack()
lblfaltantesCompras.pack()
lbl2.pack()
lblfaltantesVentas.pack()
########################################
lblCPAS.pack()

lblVTAS.pack()

#lblCPAS=tk.Label(frame,text="Algos de Compra vivos: ",font=("Arial",10,"bold"),fg="green")
#FrameCPAS
#lblCPAS.pack()
#FrameVTAS

#text_widget = scrolledtext.ScrolledText(frame, width=40, height=10)
#text_widget.pack(side=tk.LEFT)

#lblVTAS.pack()
#image_label.pack()
#frame.config(bg="lightyellow",width=300,height=300)


#####################################################################################


# Start the time update function for the first time
update_time()
root.attributes("-topmost",True)

root.mainloop()