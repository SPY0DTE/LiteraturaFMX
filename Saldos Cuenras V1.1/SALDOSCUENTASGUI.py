import pandas as pd
import pyodbc
import yfinance as yf
from tkinter import *
from sympy.solvers import solve
from tkinter import ttk
import tkinter as tk
import os
from datetime import date,datetime
from sympy import Symbol
from playsound import playsound 
x=Symbol("x")
def format_int_with_commas(x):
    """
    Formats an integer with commas as thousand separators.
    """
    return f"{x:,}"
def PreciosCanastasCuentas(TamañoCanasta,CEF,TamañoTracker,DFmonto,Sentido,HEDGE,TRACKER):
    #Tamaño canasta es el tamaño actual de la canasta, la suma de todos sus componentes de hoy
    #CEF Es el componente de efectivo (es algo ya fijo pero que cambia con el tiempo)
    # Tamaño Tracker es el numero de etf que tienes que vender para poder hacer la creacion/redencion (Es algo ya fijo)
    # DF monto es un data frame ya filtrado con compras o ventas y que tiene precio y cantidad 
    DFmonto1=DFmonto[DFmonto["Sentido"]==Sentido]
    DFmonto2=DFmonto1[DFmonto1["Symbol"]!=HEDGE]
    DFmonto3=DFmonto2[DFmonto2["Symbol"]!=TRACKER]
    Totalcomps=sum(DFmonto3["Operado Asigna"])
    NumeroCanastas=Totalcomps/TamañoCanasta
    MontoTotal=sum(DFmonto3["Operado Asigna"]*DFmonto3["PPP Asigna"])
    Precio= (MontoTotal+NumeroCanastas*CEF)/(NumeroCanastas*TamañoTracker)
    NumeroCanastasV2=str(NumeroCanastas)
    if Sentido=="COMPRA":
        SentidoV2="Creacion"
    else:
        SentidoV2="Redencion"
    
    IndicativoPrint="Llevamos "+NumeroCanastasV2+" Unidades de "+SentidoV2
    Indicativo=NumeroCanastas
    return(Precio,IndicativoPrint,Indicativo)
def Saldito(Saldo,TamañoCanasta,Canceladas,Creadas,Compras,Ventas):
    SaldoFinal=(Saldo+Compras-Ventas)-TamañoCanasta*Canceladas+TamañoCanasta*Creadas  
    return SaldoFinal


def CanastasTeorico(SaldoCuenta,ComprasCuenta,VentasCuenta,TamanoCanasta):
    # El tamaño de la canasta va a ser el tamaño del tracker
    Redenciones=solve(SaldoCuenta+ComprasCuenta-VentasCuenta-TamanoCanasta*x-TamanoCanasta,x)
    Creaciones=solve(SaldoCuenta+ComprasCuenta-VentasCuenta+TamanoCanasta*x-TamanoCanasta,x)
    if Redenciones[0]<0:
        Accion="Creaciones"
        PorLlevar=Creaciones
    else:
        Accion="Redenciones"
        PorLlevar=Redenciones
    
    return PorLlevar[0]


def TitulosHedgear(SaldoFinal,SaldoHedge,PrecioTracker,PrecioHedge):
    MontoTracker=SaldoFinal*PrecioTracker
    MontoHedge=SaldoHedge*PrecioHedge
    Diferencia=-abs(MontoHedge)+abs(MontoTracker)
    TitulosPorCubrir=Diferencia/PrecioHedge*-1
    return TitulosPorCubrir

def AlgosTracker(DataFrame,Symbolo,Estatus1,Estatus2):
    DataFrameTracker=DataFrame[DataFrame["F55_SYMBOL"]==Symbolo]
    DataFrameCPAS=DataFrameTracker[DataFrameTracker["SIDE"]=="BUY"]
    DataFrameVTAS=DataFrameTracker[DataFrameTracker["SIDE"]=="SELL"]
    DataFrameCPASNew=DataFrameCPAS[DataFrameCPAS["ORDER STATUS"]==Estatus1]
    DataFrameCPASPat=DataFrameCPAS[DataFrameCPAS["ORDER STATUS"]==Estatus2]
    DataFrameVTASNew=DataFrameVTAS[DataFrameVTAS["ORDER STATUS"]==Estatus1]
    DataFrameVTASPat=DataFrameVTAS[DataFrameVTAS["ORDER STATUS"]==Estatus2]   
    TotalesCPAS=DataFrameCPASNew["LEAVESQTY"].sum()+DataFrameCPASPat["LEAVESQTY"].sum()
    TotalesVTAS=DataFrameVTASNew["LEAVESQTY"].sum()+DataFrameVTASPat["LEAVESQTY"].sum()
    return TotalesCPAS,TotalesVTAS
    
    

Fecha=date.today()
Direccion=os.getcwd()
Sonido=Direccion+"\\woosh.wav"
TickerIVV=yf.Ticker("IVV.MX").info
TickerIVVPESO=yf.Ticker("IVVPESOISHRS.MX").info
TickerESGMEX=yf.Ticker("ESGMEXISHRS.MX").info
TickerFIBRA=yf.Ticker("FIBRATC14.MX").info
TickerQVGMEX=yf.Ticker("QVGMEX18.MX").info
TICKERMEXTRAC=yf.Ticker("MEXTRAC09.MX").info
TICKERVMEX=yf.Ticker("VMEX19.MX").info #Vamo a usar toda esta info para calcular montos y el bid/ask spread
TickerNaftrac=yf.Ticker("NAFTRACISHRS.MX").info
TickerFuno11=yf.Ticker("FUNO11.MX").info
#RAZONES#
ESGMEXMid=(TickerESGMEX["bid"]+TickerESGMEX["ask"])/2
MextacMid=(TICKERMEXTRAC["bid"]+TICKERMEXTRAC["ask"])/2
VmexMid=(TICKERVMEX["bid"]+TICKERVMEX["ask"])/2
FibraMid=(TickerFIBRA["bid"]+TickerFIBRA["ask"])/2
NaftracMid=(TickerNaftrac["bid"]+TickerNaftrac["ask"])/2
Funo11Mid=(TickerFuno11["bid"]+TickerFuno11["ask"])/2
#Nombres de la cuenta
#####################
UCITScuenta= '0100001785'
ARBITRAJEScuenta= '0100051797'
MEXTRACcuenta= '0100001787'
DIRECCIONALcuenta= '0100001786'
VMEXcuenta= '0100001784'
FIBRAcuenta= '0100001801'
ESGMEXcuenta= '0100001796'
IVVPESOcuenta= '0100051800'
EMISORAS=["IVV","IVVPESO","ESGMEX","FIBRA","QVGMEX","MEXTRAC","VMEX","NAFTRAC"]
CUENTAS=["51800.1","51800","1796","1801","1786.0","1787","1784","1786"]
SIZESCANASTAS=[1,100000,50000,100000,50000,50000,100000,100000]
TrackersDF=pd.DataFrame({"EMISORA":EMISORAS,"SIZES":SIZESCANASTAS},index=CUENTAS)
###################################################################################
######### Abrimos la informacion de cada canastas relevante para procesarla en la data
DireccionSaldosCuentas=Direccion+"\\Saldos Cuentas\\"+"SALDOS"+" "+str(Fecha.day)+str(Fecha.month)+str(Fecha.year)+".xlsx"
DireccionCanasta=Direccion+"\\Datos Canastas\\Datos Canastas.xlsx"
DatosCanasta=pd.read_excel(DireccionCanasta) #Este archivo Proviene de Un webscrapper que saca toda la info de la BMV
SaldosCuentas=pd.read_excel(DireccionSaldosCuentas)
IVVxUnidad=DatosCanasta["Size"][7]
IVVInicial=SaldosCuentas["Saldo"][0]+1000 #Ojo, en teoria puede cambiar esto
IVVPesoInicial=SaldosCuentas["Saldo"][1] #Ojo, en teoria puede cambiar esto
### BALANCES IVVPESO AL DIA
# ABSOLUTAMENTE SIEMPRE, EL IVV* TIENES QUE SER NEGATIVO SIEMPRE 
#Si lo que traemos es mayor que el teorico--> Tenemos que comprar
#Si lo que tenemos es menor que el teorico -->Tenemos que vender
SaldoInicialIVVPESO=-IVVPesoInicial*IVVxUnidad/100000
DecuadreInicialIVV=round(SaldoInicialIVVPESO-IVVInicial,1)
if DecuadreInicialIVV>0:
    AccionIVV=" Hay que Comprar"
else:
    AccionIVV=" Hay que Vender"
#####################
BalanceCuentas= 'DataAnalisysGetMatchFixVsAsignaByAccount'
AlgoPorCuenta="DataAnalisysGetAlgosByAccount" # Nombre del store procedure
# conn = pyodbc.connect('DRIVER={SQL Server};SERVER=120.23.2.48;DATABASE=receptor;UID=DataAnalysis;PWD=DataAnalysisPassword')
# QueryESGMEX= f"{AlgoPorCuenta}'{ESGMEXcuenta}'"
# QueryMEXTRAC= f"{AlgoPorCuenta}'{MEXTRACcuenta}'"
# QueryFIBRA=f"{AlgoPorCuenta}'{FIBRAcuenta}'"
# QueryVMEX= f"{AlgoPorCuenta}'{VMEXcuenta}'"
# QueryIVVPESO= f"{AlgoPorCuenta}'{IVVPESOcuenta}'"
# QueryQVGMEX= f"{AlgoPorCuenta}'{DIRECCIONALcuenta}'"
# AlgosESGMEX= pd.read_sql_query(QueryESGMEX, conn)
# AlgosMEXTRAC= pd.read_sql_query(QueryMEXTRAC, conn)
# AlgosFIBRA= pd.read_sql_query(QueryFIBRA, conn)
# AlgosVMEX= pd.read_sql_query(QueryVMEX, conn)
# AlgosIVVPESO= pd.read_sql_query(QueryIVVPESO, conn)
# AlgosQVGMEX= pd.read_sql_query(QueryQVGMEX, conn)
# conn.close()



root=Tk()

content=ttk.Frame(root)
# LOS FRAMES ###############################
AlgosTrackers = ttk.Frame(content, borderwidth=5, relief="ridge", width=300, height=100) #Donde estan las compras Totales
CanastasRelizadas=ttk.Frame(content, borderwidth=5, relief="ridge", width=300, height=100)
TrackerHedges=ttk.Frame(content, borderwidth=5, relief="ridge", width=100, height=100)
DashIVV=ttk.Frame(content, borderwidth=5, relief="ridge", width=100, height=100)
FrameHora=ttk.Frame(content,borderwidth=5, relief="ridge", width=100, height=100)
##########################################################
#TREE VIEW CREADOS Y LABEL

OperacionesTracker=ttk.Treeview(AlgosTrackers,columns=("Cuenta","EMISORA","SALDOS","CANASTA","CANCELADAS","CREADAS","COMPRAS","VENTAS","SALDO FIN"))
OperacionesTracker.tag_configure("COMPRAS",background="gray",foreground="yellow")
OperacionesTracker.tag_configure("VENTAS",foreground="blue",background="White")
OperacionesTracker.heading("#0",text="")
OperacionesTracker.column("#0",width=0)
OperacionesTracker.heading("Cuenta",text="CUENTA")
OperacionesTracker.column("Cuenta",width=60)
OperacionesTracker.heading("EMISORA",text="EMISORA")
OperacionesTracker.column("EMISORA",width=80)
OperacionesTracker.heading("SALDOS",text="SALDO-I")
OperacionesTracker.column("SALDOS",width=80)
OperacionesTracker.heading("CANASTA",text="SIZE")
OperacionesTracker.column("CANASTA",width=50)
OperacionesTracker.heading("CREADAS",text="CREADAS")
OperacionesTracker.column("CREADAS",width=80)
OperacionesTracker.heading("CANCELADAS",text="CANCELADAS")
OperacionesTracker.column("CANCELADAS",width=90)
OperacionesTracker.heading("COMPRAS",text="COMPRAS")
OperacionesTracker.column("COMPRAS",width=80)
OperacionesTracker.heading("VENTAS",text="VENTAS")
OperacionesTracker.column("VENTAS",width=80)
OperacionesTracker.heading("SALDO FIN",text="SALDO-F")
OperacionesTracker.column("SALDO FIN",width=80)
#VACIAMOS LOS DATOS#############################################################################
Fil1=OperacionesTracker.insert("","end",values=("51800"," IVVPESO",format_int_with_commas(SaldosCuentas["Saldo"][1]),"100,000","0","0","400","33","50"),tags=("COMPRAS"))
Fil2=OperacionesTracker.insert("","end",values=("1796"," ESGMEX",format_int_with_commas(SaldosCuentas["Saldo"][2]),"50,000","0","0","400","33","50"),tags=("VENTAS"))
Fil3=OperacionesTracker.insert("","end",values=("1801"," FIBRA",format_int_with_commas(SaldosCuentas["Saldo"][3]),"100,000","0","0","400","33","50"),tags=("COMPRAS"))
Fil4=OperacionesTracker.insert("","end",values=("1786"," QVGMEX",format_int_with_commas(SaldosCuentas["Saldo"][4]),"50,000","0","0","400","33","50"),tags=("VENTAS"))
Fil5=OperacionesTracker.insert("","end",values=("1787"," MEXTRAC",format_int_with_commas(SaldosCuentas["Saldo"][5]),"100,000","0","0","400","33","50"),tags=("COMPRAS"))
Fil6=OperacionesTracker.insert("","end",values=("1784"," VMEX",format_int_with_commas(SaldosCuentas["Saldo"][6]),"100,000","0","0","400","33","50"),tags=("VENTAS"))
Fil7=OperacionesTracker.insert("","end",values=("1786"," NAFTRAC",format_int_with_commas(SaldosCuentas["Saldo"][7]),"100,000","0","0","400","33","50"),tags=("COMPRAS"))
#OperacionesTracker.column("EMISORA",width=100)
PreciosCanastas=ttk.Treeview(CanastasRelizadas,columns=("Tracker","CREACIONES","PRECIO CREACION","REDENCIONES","PRECIO REDENCIONES","NETOS","CPA ALGOS","VTA ALGOS"))
PreciosCanastas.tag_configure("COMPRAS",foreground="blue",background="grey")
PreciosCanastas.tag_configure("VENTAS",foreground="red",background="white")
PreciosCanastas.heading("#0",text="")
PreciosCanastas.column("#0",width=0)
PreciosCanastas.heading("Tracker",text="TRACKER")
PreciosCanastas.column("Tracker",width=80)
PreciosCanastas.heading("CREACIONES",text="CREACIONES")
PreciosCanastas.column("CREACIONES",width=80)
PreciosCanastas.heading("PRECIO CREACION",text="PRECIO C")
PreciosCanastas.column("PRECIO CREACION",width=80)
PreciosCanastas.heading("REDENCIONES",text="REDENCIONES")
PreciosCanastas.column("REDENCIONES",width=90)
PreciosCanastas.heading("PRECIO REDENCIONES",text="PRECIO V")
PreciosCanastas.column("PRECIO REDENCIONES",width=80)
PreciosCanastas.heading("NETOS",text="NETOS")
PreciosCanastas.column("NETOS",width=80)
PreciosCanastas.heading("CPA ALGOS",text="CPA ALGOS")
PreciosCanastas.column("CPA ALGOS",width=80)
PreciosCanastas.heading("VTA ALGOS",text="VTA ALGOS")
PreciosCanastas.column("VTA ALGOS",width=80)
Fil8=PreciosCanastas.insert("","end",values=(" ESGMEX",0,0,0,0,0,0,0,0),tags=("COMPRAS"))
Fil9=PreciosCanastas.insert("","end",values=(" FIBRA",0,0,0,0,0,0,0,0),tags=("VENTAS"))
Fil11=PreciosCanastas.insert("","end",values=(" MEXTRAC",0,0,0,0,0,0,0,0),tags=("COMPRAS"))
Fil12=PreciosCanastas.insert("","end",values=(" VMEX",0,0,0,0,0,0,0,0),tags=("VENTAS"))
Fil10=PreciosCanastas.insert("","end",values=(" QVGMEX",0,0,0,0,0,0,0,0),tags=("COMPRAS"))
Fil13=PreciosCanastas.insert("","end",values=(" NAFTRAC",0,0,0,0,0,0,0,0),tags=("VENTAS"))
###################################################################
#IVVPESO=ttk.Treeview(DashIVV)
IvvsPorUnidad="IVV* por Unidad: "+str(IVVxUnidad)
IVVPESOXUNIDAD=ttk.Label(DashIVV,text=IvvsPorUnidad)
IVVALFINALDELDIA=ttk.Label(DashIVV,text="IVV* al Inicio del día: "+str(format_int_with_commas(IVVInicial)))
IVVALINICIODELDIA=ttk.Label(DashIVV,text="IVV peso al inicio del día: "+str(format_int_with_commas(IVVPesoInicial)))
IVVHEDGEINICIODELDIA=ttk.Label(DashIVV,text="IVV* TEORICO"+str(format_int_with_commas(round(SaldoInicialIVVPESO))))
DESCUADREINICIODELDIA=ttk.Label(DashIVV,text="Descuadre: "+str(format_int_with_commas(DecuadreInicialIVV))+AccionIVV)
DIFERENCIAFINALDELDIA=ttk.Label(DashIVV,text="Diferencia total final del dia operada: ")
IVVALFINALDELDIAOPERADO=ttk.Label(DashIVV,text="Saldo IVV* operado final: ")
# COMPRASDOLARES1785
# VENTADOLARES1785
# COMPRASDOLARES51797
# VENTADOLARES51797
Hedges=ttk.Treeview(TrackerHedges,columns=("Cuenta","Hedge","Acciones a Hedgear"))
Hedges.heading("#0",text="")
Hedges.column("#0",width=0)
Hedges.heading("Cuenta",text="Cuenta")
Hedges.column("Cuenta",width=50)
Hedges.heading("Hedge",text="Hedge")
Hedges.column("Hedge",width=80)
Hedges.heading("Acciones a Hedgear",text="Acciones a Hedgear")
Hedges.column("Acciones a Hedgear",width=120)
Fil14=Hedges.insert("","end",values=("1796","NAFTRAC",0))
Fil15=Hedges.insert("","end",values=("1801","FUNO11",0))
Fil16=Hedges.insert("","end",values=("1787","NAFTRAC",0))
Fil17=Hedges.insert("","end",values=("1784","NAFTRAC",0))
########################################################################
Resultado=ttk.Label(content,text="P&L 1785: ")
HeaderTrackerOperadas=ttk.Label(AlgosTrackers,text="Tracker Operados")
HeaderVentas=ttk.Label(CanastasRelizadas,text="Pecios Canastas")
HeaderAlgosPendientes=ttk.Label(DashIVV,text="HEDGES CUENTAS")
HeaderHedges=ttk.Label(TrackerHedges,text="HEDGE CUENTAS")
AlgosVivosCPAS=ttk.Label(content,text="Cazadoras de compra Vivas: ")
AlgosVivosVTAS=ttk.Label(content,text="Cazadoras de ventas Vivas: ")
Hora=ttk.Label(content,text="Hora :o")
ArbitrajesCheck=ttk.Label(content,text="Arbitrajes: ")
#########################################################################################
# Priteamos los frames
content.grid(column=0, row=0,padx=1,pady=1) # Es el frame
AlgosTrackers.grid(column=2, row=5, columnspan=3, rowspan=2) # Primer Frame
CanastasRelizadas.grid(column=2, row=7, columnspan=3, rowspan=2) # Segundo Frame
TrackerHedges.grid(column=5,row=5,columnspan=3,rowspan=2) # Tercer Frame
DashIVV.grid(column=5,row=7,columnspan=3,rowspan=2) #Cuarto Frame
##############################################################################
# Printeamos los headers de cada uno de los recuadros
HeaderTrackerOperadas.grid()
HeaderVentas.grid()
HeaderAlgosPendientes.grid()
HeaderHedges.grid()
###################################################
Hedges.grid()
OperacionesTracker.grid()
PreciosCanastas.grid()
IVVPESOXUNIDAD.grid()
IVVALFINALDELDIA.grid()
IVVALINICIODELDIA.grid()
IVVHEDGEINICIODELDIA.grid()
DESCUADREINICIODELDIA.grid()
DIFERENCIAFINALDELDIA.grid()
IVVALFINALDELDIAOPERADO.grid()
# Printeamos data adicional que no corresponder a las tablas ni a los frames, esta data vive en el Frame Principal
AlgosVivosCPAS.grid(column=3,row=0,columnspan=3,rowspan=1)
AlgosVivosVTAS.grid(column=3,row=1,columnspan=3,rowspan=1)
Hora.grid(column=7,row=1)
Resultado.grid(column=7,row=4)
ArbitrajesCheck.grid(column=7,row=0)
def TrackerSaldo(CUENTA,SENTIDO,TRACKER):
    w=len(CUENTA[CUENTA["Symbol"]==TRACKER])
    if w==0:
        d={"Symbol":TRACKER,"Sentido":SENTIDO,"Operado FIX":0,"Operado Asigna":0,"PPP FIX":0,"PPP Asigna":0,"Diferencia":0}
        CUENTALADOTracker=pd.DataFrame(d,index=[0])
    else:
        CUENTALADO=CUENTA[CUENTA["Sentido"]==SENTIDO]
        CUENTALADOTracker=CUENTALADO[CUENTALADO["Symbol"]==TRACKER].reset_index(drop=True)
    return CUENTALADOTracker


def UpdateTime():
    global MEXTRACuenta
    global BalanceCuentas
    # Hora en tiempo real
    now=datetime.now()
    current_time=now.strftime("%H:%M:%S")
    # Cuentas
    conn = pyodbc.connect('DRIVER={SQL Server};SERVER=120.23.2.48;DATABASE=receptor;UID=DataAnalysis;PWD=DataAnalysisPassword')
    query = f"EXEC {BalanceCuentas}'{MEXTRACcuenta}'"
    MEXTRAC=pd.read_sql_query(query, conn)
    query = f"EXEC {BalanceCuentas}'{ESGMEXcuenta}'"
    ESGMEX=pd.read_sql_query(query, conn)
    query = f"EXEC {BalanceCuentas}'{FIBRAcuenta}'"
    FIBRA=pd.read_sql_query(query, conn)
    query = f"EXEC {BalanceCuentas}'{VMEXcuenta}'"
    VMEX=pd.read_sql_query(query, conn)
    query = f"EXEC {BalanceCuentas}'{DIRECCIONALcuenta}'"
    DIRECCIONAL=pd.read_sql_query(query, conn)
    query = f"EXEC {BalanceCuentas}'{IVVPESOcuenta}'"
    IVVPESO=pd.read_sql_query(query, conn)
    query = f"EXEC {BalanceCuentas}'{ARBITRAJEScuenta}'"
    Arbitrajes=pd.read_sql_query(query, conn)   
    conn.close()
    conn = pyodbc.connect('DRIVER={SQL Server};SERVER=120.23.2.48;DATABASE=receptor;UID=DataAnalysis;PWD=DataAnalysisPassword')
    QueryESGMEX= f"{AlgoPorCuenta}'{ESGMEXcuenta}'"
    QueryMEXTRAC= f"{AlgoPorCuenta}'{MEXTRACcuenta}'"
    QueryFIBRA=f"{AlgoPorCuenta}'{FIBRAcuenta}'"
    QueryVMEX= f"{AlgoPorCuenta}'{VMEXcuenta}'"
    QueryIVVPESO= f"{AlgoPorCuenta}'{IVVPESOcuenta}'"
    QueryQVGMEX= f"{AlgoPorCuenta}'{DIRECCIONALcuenta}'"
    AlgosESGMEX= pd.read_sql_query(QueryESGMEX, conn)
    AlgosMEXTRAC= pd.read_sql_query(QueryMEXTRAC, conn)
    AlgosFIBRA= pd.read_sql_query(QueryFIBRA, conn)
    AlgosVMEX= pd.read_sql_query(QueryVMEX, conn)
    AlgosIVVPESO= pd.read_sql_query(QueryIVVPESO, conn)
    AlgosQVGMEX= pd.read_sql_query(QueryQVGMEX, conn)
    conn.close()
    #### Aqui obtenemos todos los trackers existentes 
    #Printeamos Todo lo que llevamos operado :) 
    MEXTRACCOMPRASTracker=TrackerSaldo(MEXTRAC,"COMPRA","MEXTRAC09")
    MEXTRACVENTASTracker=TrackerSaldo(MEXTRAC,"VENTA","MEXTRAC09")
    ESGMEXCOMPRASTracker=TrackerSaldo(ESGMEX,"COMPRA","ESGMEXISHRS")
    ESGMEXVENTASTracker=TrackerSaldo(ESGMEX,"VENTA","ESGMEXISHRS")
    FIBRATCCOMPRASTracker=TrackerSaldo(FIBRA,"COMPRA","FIBRATC14")
    FIBRATCVENTASTracker=TrackerSaldo(FIBRA,"VENTA","FIBRATC14")
    VMEXCOMPRASTracker=TrackerSaldo(VMEX,"COMPRA","VMEX19")
    VMEXVENTASTracker=TrackerSaldo(VMEX,"VENTA","VMEX19")
    IVVPESOCOMPRASTracker=TrackerSaldo(IVVPESO,"COMPRA","IVVPESOISHRS")
    IVVPESOVENTASTracker=TrackerSaldo(IVVPESO,"VENTA","IVVPESOISHRS")   
    QVGMEXCOMPRASTracker=TrackerSaldo(DIRECCIONAL,"COMPRA","QVGMEX18")
    QVGMEXVENTASTracker=TrackerSaldo(DIRECCIONAL,"VENTA","QVGMEX18")
    NAFTRACCOMPRASTracker=TrackerSaldo(DIRECCIONAL,"COMPRA","NAFTRACISHRS")
    NAFTRACVENTASTracker=TrackerSaldo(DIRECCIONAL,"VENTA","NAFTRACHISHRS")
    #Calculamos todas nuestras canastas hechas y los salgos
    ESGMEXCOMPRASComponentes=ESGMEX[ESGMEX["Symbol"]!="ESGMEXISHRS"]
    #TimeWindow=current_time-timedelta(minutes=2)
    COMPRASMEXTRAC,VENTASMEXTRAC=AlgosTracker(AlgosMEXTRAC,DatosCanasta["Name"][3],"NEW","PATIALLY FILLED")
    COMPRASFIBRA,VENTASFIBRA=AlgosTracker(AlgosFIBRA,DatosCanasta["Name"][0],"NEW","PATIALLY FILLED")
    COMPRASVMEX,VENTASVMEX=AlgosTracker(AlgosVMEX,DatosCanasta["Name"][5],"NEW","PATIALLY FILLED")
    COMPRASESGMEX,VENTASESGMEX=AlgosTracker(AlgosESGMEX, DatosCanasta["Name"][4],"NEW","PATIALLY FILLED")
    COMPRASQVGMEX,VENTASQVGMEX=AlgosTracker(AlgosQVGMEX, DatosCanasta["Name"][1],"NEW","PATIALLY FILLED")
    TotalesArbitraje=format_int_with_commas(Arbitrajes["Operado Asigna"].sum())
    TextArbitraje="Total Arbitrajes: "+TotalesArbitraje
    #Operaciones De canastas --------------------------------------------
    PrecioComprasESGMEX,IndicativoCPAPrintESG,IndicativoCPAESG=PreciosCanastasCuentas(DatosCanasta["Size"][4],DatosCanasta["Efectivo"][4],TrackersDF["SIZES"]["1796"],ESGMEX,"COMPRA",DatosCanasta["HEDGE"][4],DatosCanasta["Name"][4])
    PrecioVentasESGMEX,IndicativoVTAprintESGMEX,IndicativoVTAESGMEX=PreciosCanastasCuentas(DatosCanasta["Size"][4],DatosCanasta["Efectivo"][4],TrackersDF["SIZES"]["1796"],ESGMEX,"VENTA",DatosCanasta["HEDGE"][4],DatosCanasta["Name"][4])
    PrecioComprasMEXTRAC,IndicativoCPAPrintMEXTRAC,IndicativoCPAMEXTRAC=PreciosCanastasCuentas(DatosCanasta["Size"][3],DatosCanasta["Efectivo"][3],TrackersDF["SIZES"]["1787"],MEXTRAC,"COMPRA",DatosCanasta["HEDGE"][3],DatosCanasta["Name"][3])
    PrecioVentasMEXTRAC,IndicativoVTAPrintMEXTRAC,IndicativoVTAMEXTRAC=PreciosCanastasCuentas(DatosCanasta["Size"][3],DatosCanasta["Efectivo"][3],TrackersDF["SIZES"]["1787"],MEXTRAC,"VENTA",DatosCanasta["HEDGE"][3],DatosCanasta["Name"][3])
    PrecioComprasFIBRATC,IndicativoCPAPrintFIBRATC,IndicativoCPAFIBRATC=PreciosCanastasCuentas(DatosCanasta["Size"][0],DatosCanasta["Efectivo"][0],TrackersDF["SIZES"]["1801"],FIBRA,"COMPRA",DatosCanasta["HEDGE"][0],DatosCanasta["Name"][0])
    PrecioVentasFIBRATC,IndicativoVTAPrintFIBRATC,IndicativoVTAFIBRATC=PreciosCanastasCuentas(DatosCanasta["Size"][0],DatosCanasta["Efectivo"][0],TrackersDF["SIZES"]["1801"],FIBRA,"VENTA",DatosCanasta["HEDGE"][0],DatosCanasta["Name"][0])
    PrecioComprasVMEX,IndicativoCPAPrintVMEX,IndicativoCPAVMEX=PreciosCanastasCuentas(DatosCanasta["Size"][5],DatosCanasta["Efectivo"][5],TrackersDF["SIZES"]["1784"],VMEX,"COMPRA",DatosCanasta["HEDGE"][5],DatosCanasta["Name"][5])
    PrecioVentasVMEX,IndicativoVTAPrintVMEX,IndicativoVTAVMEX=PreciosCanastasCuentas(DatosCanasta["Size"][5],DatosCanasta["Efectivo"][5],TrackersDF["SIZES"]["1784"],VMEX,"VENTA",DatosCanasta["HEDGE"][5],DatosCanasta["Name"][5])
    PrecioComprasQVGMEX,IndicativoCPAPrintQVGMEX,IndicativoCPAQVGMEX=PreciosCanastasCuentas(DatosCanasta["Size"][1],DatosCanasta["Efectivo"][1],TrackersDF["SIZES"]["1786.0"],DIRECCIONAL,"COMPRA",DatosCanasta["HEDGE"][1],DatosCanasta["Name"][1])
    PrecioVentasQVGMEX,IndicativoVTAPrintQVGMEX,IndicativoVTAQVGMEX=PreciosCanastasCuentas(DatosCanasta["Size"][1],DatosCanasta["Efectivo"][1],TrackersDF["SIZES"]["1786.0"],DIRECCIONAL,"VENTA",DatosCanasta["HEDGE"][1],DatosCanasta["Name"][1])
    PrecioComprasNAFTRAC,IndicativoCPAPrintNAFTRAC,IndicativoCPANAFTRAC=PreciosCanastasCuentas(DatosCanasta["Size"][6],DatosCanasta["Efectivo"][6],TrackersDF["SIZES"]["1786"],DIRECCIONAL,"COMPRA",DatosCanasta["HEDGE"][6],DatosCanasta["Name"][6])
    PrecioVentasNAFTRAC,IndicativoVTAPrintNAFTRAC,IndicativoVTANAFTRACX=PreciosCanastasCuentas(DatosCanasta["Size"][6],DatosCanasta["Efectivo"][6],TrackersDF["SIZES"]["1786"],DIRECCIONAL,"VENTA",DatosCanasta["HEDGE"][6],DatosCanasta["Name"][6])
    ###Saldos####
    SaldoMextrac=Saldito(SaldosCuentas["Saldo"][5],TrackersDF["SIZES"]["1787"],IndicativoVTAMEXTRAC,IndicativoCPAMEXTRAC,MEXTRACCOMPRASTracker["Operado FIX"][0],MEXTRACVENTASTracker["Operado FIX"][0])
    SaldoFibra=Saldito(SaldosCuentas["Saldo"][3],TrackersDF["SIZES"]["1801"],IndicativoVTAFIBRATC,IndicativoCPAFIBRATC,FIBRATCCOMPRASTracker["Operado FIX"][0],FIBRATCVENTASTracker["Operado FIX"][0])
    SaldoESGMEX=Saldito(SaldosCuentas["Saldo"][2],TrackersDF["SIZES"]["51800"],IndicativoVTAESGMEX,IndicativoCPAESG,ESGMEXCOMPRASTracker["Operado FIX"][0],ESGMEXVENTASTracker["Operado FIX"][0])
    SaldoVMEX=Saldito(SaldosCuentas["Saldo"][6],TrackersDF["SIZES"]["1784"],IndicativoVTAVMEX,IndicativoCPAVMEX,VMEXCOMPRASTracker["Operado FIX"][0],VMEXVENTASTracker["Operado FIX"][0])
    #SaldoIVVPEOS=Saldito(SaldoCuentas["Saldo"][1],TrackersDF["SIZES"]["51800"], Canceladas, Creadas, Compras, Ventas)
    TeoricoMextrac=CanastasTeorico(SaldoMextrac,MEXTRACCOMPRASTracker["Operado FIX"][0],MEXTRACVENTASTracker["Operado FIX"][0],TrackersDF["SIZES"]["1787"])
    TeoricoFibra=CanastasTeorico(SaldoFibra,FIBRATCCOMPRASTracker["Operado FIX"][0],FIBRATCVENTASTracker["Operado FIX"][0],TrackersDF["SIZES"]["1801"])
    TeoricoESGMEX=CanastasTeorico(SaldoESGMEX,ESGMEXCOMPRASTracker["Operado FIX"][0],ESGMEXVENTASTracker["Operado FIX"][0],TrackersDF["SIZES"]["1796"])
    TeoricoVMEX=CanastasTeorico(SaldoVMEX,VMEXCOMPRASTracker["Operado FIX"][0],VMEXVENTASTracker["Operado FIX"][0],TrackersDF["SIZES"]["1784"])
    #######Titulos a hedger####################
    HedgeEsgmex=TitulosHedgear(SaldoESGMEX,SaldosCuentas["HEDGE TITULOS"][2],ESGMEXMid,NaftracMid)
    HedgeFibra=TitulosHedgear(SaldoFibra,SaldosCuentas["HEDGE TITULOS"][3],FibraMid,Funo11Mid)
    HedgeMextrac=TitulosHedgear(SaldoMextrac,SaldosCuentas["HEDGE TITULOS"][5],MextacMid,NaftracMid)
    HedgeVMEX=TitulosHedgear(SaldoVMEX,SaldosCuentas["HEDGE TITULOS"][6],VmexMid,NaftracMid)
    #Vaciamos la data en la tablita
    OperacionesTracker.set(Fil1,"COMPRAS",format_int_with_commas(IVVPESOCOMPRASTracker["Operado FIX"][0]))
    OperacionesTracker.set(Fil1,"VENTAS",format_int_with_commas(IVVPESOVENTASTracker["Operado FIX"][0]))
    ########################################################################################################
    OperacionesTracker.set(Fil2,"COMPRAS",format_int_with_commas(ESGMEXCOMPRASTracker["Operado FIX"][0]))
    OperacionesTracker.set(Fil2,"VENTAS",format_int_with_commas(ESGMEXVENTASTracker["Operado FIX"][0]))
    OperacionesTracker.set(Fil2,"SALDO FIN",format_int_with_commas(SaldoESGMEX))
    OperacionesTracker.set(Fil2,"CREADAS",IndicativoCPAESG)
    OperacionesTracker.set(Fil2,"CANCELADAS",IndicativoVTAESGMEX)
    ###################
    OperacionesTracker.set(Fil3,"COMPRAS",format_int_with_commas(FIBRATCCOMPRASTracker["Operado FIX"][0]))
    OperacionesTracker.set(Fil3,"VENTAS",format_int_with_commas(FIBRATCVENTASTracker["Operado FIX"][0]))
    OperacionesTracker.set(Fil3,"SALDO FIN",format_int_with_commas(SaldoFibra))
    OperacionesTracker.set(Fil3,"CREADAS",IndicativoCPAFIBRATC)
    OperacionesTracker.set(Fil3,"CANCELADAS",IndicativoVTAFIBRATC)
    #######################
    OperacionesTracker.set(Fil4,"COMPRAS",format_int_with_commas(QVGMEXCOMPRASTracker["Operado FIX"][0]))
    OperacionesTracker.set(Fil4,"VENTAS",format_int_with_commas(QVGMEXVENTASTracker["Operado FIX"][0]))
    OperacionesTracker.set(Fil4,"CREADAS",IndicativoCPAQVGMEX)
    OperacionesTracker.set(Fil4,"CANCELADAS",IndicativoVTAQVGMEX)
    #MEXTRAC#
    OperacionesTracker.set(Fil5,"COMPRAS",format_int_with_commas(MEXTRACCOMPRASTracker["Operado FIX"][0]))
    OperacionesTracker.set(Fil5,"VENTAS",format_int_with_commas(MEXTRACVENTASTracker["Operado FIX"][0]))
    OperacionesTracker.set(Fil5,"SALDO FIN",format_int_with_commas(SaldoMextrac))
    OperacionesTracker.set(Fil5,"CREADAS",IndicativoCPAMEXTRAC)
    OperacionesTracker.set(Fil5,"CANCELADAS",IndicativoVTAMEXTRAC)
    ############
    OperacionesTracker.set(Fil6,"COMPRAS",format_int_with_commas(VMEXCOMPRASTracker["Operado FIX"][0]))
    OperacionesTracker.set(Fil6,"VENTAS",format_int_with_commas(VMEXVENTASTracker["Operado FIX"][0]))
    OperacionesTracker.set(Fil6,"SALDO FIN",format_int_with_commas(SaldoVMEX))
    OperacionesTracker.set(Fil6,"CREADAS",IndicativoCPAVMEX)
    OperacionesTracker.set(Fil6,"CANCELADAS",IndicativoVTAVMEX)
    OperacionesTracker.set(Fil7,"COMPRAS",format_int_with_commas(NAFTRACCOMPRASTracker["Operado FIX"][0]))
    OperacionesTracker.set(Fil7,"VENTAS",format_int_with_commas(NAFTRACVENTASTracker["Operado FIX"][0]))
    OperacionesTracker.set(Fil7,"CREADAS",IndicativoCPANAFTRAC)
    OperacionesTracker.set(Fil7,"CANCELADAS",IndicativoVTANAFTRACX)
    #Ponemos Los precios de las canastas que hemos hecho
    PreciosCanastas.set(Fil11,"CREACIONES",round(IndicativoCPAMEXTRAC,0))
    PreciosCanastas.set(Fil11,"PRECIO CREACION",round(PrecioComprasMEXTRAC,4))
    PreciosCanastas.set(Fil11,"REDENCIONES",round(IndicativoVTAMEXTRAC,0))
    PreciosCanastas.set(Fil11,"PRECIO REDENCIONES",round(PrecioVentasMEXTRAC,4))
    PreciosCanastas.set(Fil11,"NETOS",round(TeoricoMextrac,0))
    PreciosCanastas.set(Fil11,"CPA ALGOS",format_int_with_commas(COMPRASMEXTRAC))
    PreciosCanastas.set(Fil11,"VTA ALGOS",format_int_with_commas(VENTASMEXTRAC))
    PreciosCanastas.set(Fil9,"CREACIONES",round(IndicativoCPAFIBRATC,0))
    PreciosCanastas.set(Fil9,"PRECIO CREACION",round(PrecioComprasFIBRATC,4))
    PreciosCanastas.set(Fil9,"REDENCIONES",round(IndicativoVTAFIBRATC,0))
    PreciosCanastas.set(Fil9,"PRECIO REDENCIONES",round(PrecioVentasFIBRATC,4))
    PreciosCanastas.set(Fil9,"NETOS",round(TeoricoFibra,0))
    PreciosCanastas.set(Fil9,"CPA ALGOS",format_int_with_commas(COMPRASFIBRA))
    PreciosCanastas.set(Fil9,"VTA ALGOS",format_int_with_commas(VENTASFIBRA))  
    PreciosCanastas.set(Fil8,"CREACIONES",round(IndicativoCPAESG,0))
    PreciosCanastas.set(Fil8,"PRECIO CREACION",round(PrecioComprasESGMEX,4))
    PreciosCanastas.set(Fil8,"REDENCIONES",round(IndicativoVTAESGMEX,0))
    PreciosCanastas.set(Fil8,"PRECIO REDENCIONES",round(PrecioVentasESGMEX,4))
    PreciosCanastas.set(Fil8,"NETOS",round(TeoricoESGMEX,0))
    PreciosCanastas.set(Fil8,"CPA ALGOS",format_int_with_commas(COMPRASESGMEX))
    PreciosCanastas.set(Fil8,"VTA ALGOS",format_int_with_commas(VENTASESGMEX))
    PreciosCanastas.set(Fil12,"CREACIONES",round(IndicativoCPAVMEX,0))
    PreciosCanastas.set(Fil12,"PRECIO CREACION",round(PrecioComprasVMEX,4))
    PreciosCanastas.set(Fil12,"REDENCIONES",round(IndicativoVTAVMEX,0))
    PreciosCanastas.set(Fil12,"PRECIO REDENCIONES",round(PrecioVentasVMEX,4))
    PreciosCanastas.set(Fil12,"NETOS",round(TeoricoVMEX,0)) 
    PreciosCanastas.set(Fil12,"CPA ALGOS",format_int_with_commas(COMPRASVMEX))
    PreciosCanastas.set(Fil12,"VTA ALGOS",format_int_with_commas(VENTASVMEX))
    PreciosCanastas.set(Fil10,"CREACIONES",round(IndicativoCPAQVGMEX,0))
    PreciosCanastas.set(Fil10,"PRECIO CREACION",round(PrecioComprasQVGMEX,4))
    PreciosCanastas.set(Fil10,"REDENCIONES",round(IndicativoVTAQVGMEX,0))
    PreciosCanastas.set(Fil10,"PRECIO REDENCIONES",round(PrecioVentasQVGMEX,4))
    PreciosCanastas.set(Fil10,"CPA ALGOS",format_int_with_commas(COMPRASQVGMEX))
    PreciosCanastas.set(Fil10,"VTA ALGOS",format_int_with_commas(VENTASQVGMEX))
    PreciosCanastas.set(Fil13,"CREACIONES",round(IndicativoCPANAFTRAC,0))
    PreciosCanastas.set(Fil13,"PRECIO CREACION",round(PrecioComprasNAFTRAC,4))
    PreciosCanastas.set(Fil13,"REDENCIONES",round(IndicativoCPANAFTRAC,0))
    PreciosCanastas.set(Fil13,"PRECIO REDENCIONES",round(PrecioComprasNAFTRAC,4))
    Hedges.set(Fil14,"Acciones a Hedgear",format_int_with_commas(round(HedgeEsgmex)))
    Hedges.set(Fil15,"Acciones a Hedgear",format_int_with_commas(round(HedgeFibra)))
    Hedges.set(Fil16,"Acciones a Hedgear",format_int_with_commas(round(HedgeMextrac)))
    Hedges.set(Fil17,"Acciones a Hedgear",format_int_with_commas(round(HedgeVMEX)))
    ValidarCompras=COMPRASESGMEX<70000 or COMPRASFIBRA<70000 or COMPRASMEXTRAC<70000 or COMPRASQVGMEX<20000 or COMPRASVMEX<70000
    ValidarVentas=VENTASESGMEX<70000 or VENTASFIBRA<70000 or VENTASMEXTRAC<70000 or VENTASQVGMEX<20000 or VENTASVMEX<70000
    ValidarTotal=ValidarCompras or ValidarVentas
    IVVLong=-IVVPESOCOMPRASTracker["Operado FIX"][0]*DatosCanasta["Size"][7]/100000
    IVVShort=IVVPESOVENTASTracker["Operado FIX"][0]*DatosCanasta["Size"][7]/100000
    DifTotalIVV=round(IVVLong+IVVShort,0)
    TextoDIFFtotal="Diferencia Final del dia Operada: "+str(DifTotalIVV)
    if ValidarTotal == True:
        playsound(Sonido)
       
    
    
    #OperacionesTracker.insert("","end",values=("1787","MEXTRAC",format_int_with_commas(SaldosCuentas["Saldo"][5]),"100,000","1","1", MEXTRACCOMPRASTracker["Operado FIX"][0], MEXTRACVENTASTracker["Operado FIX"][1],"50"))
    #Lo primero es que los indices se tienen que resetear-....
    #Tambien tenemos que definir en caso de que no se haya operado nada.... y creo que ya, fuera de eso la impresion la hace en cascada en vez de que solo la modifique
    #ACTUALIZACION DE LA INFORMACION###
    Hora.config(text=current_time,foreground="green",font=("Cambria",12,"bold"))  
    ArbitrajesCheck.config(text=TextArbitraje,foreground="green",font=("Cambria",12,"bold"))  
    DIFERENCIAFINALDELDIA.config(text=TextoDIFFtotal)
    root.after(1000,UpdateTime)
    
#####################################################################################
# Start the time update function for the first time
UpdateTime()
root.attributes("-topmost",True)
root.mainloop()