import pandas as pd
import pickle
import os
import chardet
Direccion=os.getcwd()
Lista=["FIBRATC14","QVGMEX18","GENIUS","MEXTRAC09","ESGMEXISHRS","VMEX19","NAFTRACISHRS","IVVPESOISHRS"]
Sizes=[100000,50000,1,50000,50000,100000,100000,100000]

Tamaño=[]
EFECTIVO=[]
def Localizadora(NombreArchivo,Columna,Indexador):
    DFArch=pd.read_excel(NombreArchivo)
    DFCol=DFArch[Columna]
    DFIndex=[]
    for i in DFCol.index:
        if DFCol[i]==Indexador:
            DFIndex.append(i)
    return DFArch,DFIndex
#La funcion a continuacion extrae df de un excell especifico con la informacion que requerimos
#Le tienes que dar el dataframe y la lista del valor de los indices donde esta tu info Y el valor final donde quieres que tu tabla termine
def Extractora(DataFrame,DFIndex,IndxFinal):
    DFExt=DataFrame[DFIndex:IndxFinal]
    return DFExt
def Comparadora(DF1,DF2,Col1,Col2):
    A=DF1[Col1]-DF2[Col2]
    C=A.sum()
    return C
#def STR(x):
 #   a=str(x)
  #  return(a)
#ESTE CODIGO ESTA MAL
#SOLO CALCULA LAS DIFERENCIAS TOTALES
#TIENE QUE CALCULARLAS UNO A UNO 
#Este codigo habre un excell y literalmente te dice donde esta cierto valor buscado
#Generalmente sirve para encontrar un valor especifico como referencia, tienes que darle el nombre del archivo
#La columna del excell y el dato exacto del valor y te da el index donde esta ese valor 
#Fibra,FibraINXD=("Fibra.xls","Unnamed: 4","Acciones")
#FIBRA TRAc
DirTemp=Direccion+"\\CANASTAS\\FIBRA.xls"
NombreArchivo=DirTemp
Columna="Unnamed: 4"
Indexador="Acciones"
Fibra,FIBRAIndx=Localizadora(NombreArchivo,Columna,Indexador)
DFFibra=Extractora(Fibra,FIBRAIndx[0]+1,len(Fibra)-1)#Aquie estas usando slice que siempre te toma uno menos 
DFFibra=DFFibra[["Unnamed: 1","Unnamed: 4","Unnamed: 2"]]
DFFibra["Unnamed: 2"]=DFFibra["Unnamed: 2"].apply(str)
DFFibra["Unnamed: 1"]=DFFibra["Unnamed: 1"]+DFFibra["Unnamed: 2"]
DFFibra=DFFibra.drop(labels="Unnamed: 2",axis=1)
DFFibra=DFFibra.sort_values("Unnamed: 1").set_index("Unnamed: 1",drop=True) 
CEFibra=Fibra[Columna][len(Fibra)-1]#Aqui estas tomando indices que siempre te toma el mismo dato que le das pq es un indice
DirTemp=Direccion+"\\CANASTAS\\FIBRA1.csv"
NombreArchivo=DirTemp
FibraDash=pd.read_csv(DirTemp)
FibraDash=FibraDash[["Emisora","Peso"]].sort_values("Emisora").set_index("Emisora")
A=FibraDash["Peso"]-DFFibra["Unnamed: 4"]
Data=["Tracker","FIBRA","Tamaño",sum(FibraDash["Peso"]),"Componente Efectivo",CEFibra]
Tamaño.append(sum(FibraDash["Peso"]))
EFECTIVO.append(CEFibra)
if (A==0).all():
    print("No hay diferencia en Fibra UwU")
else:
    print("Hay diferencias en FIBRA >:v ")
#QVGMEX #
DirTemp=Direccion+"\\CANASTAS\\QVGMEX.xls"
NombreArchivo=DirTemp
Columna="Unnamed: 4"
Indexador="# de títulos"
QVGMEX,QVGMEXIndx=Localizadora(NombreArchivo,Columna,Indexador)
DFQvgmex=Extractora(QVGMEX,QVGMEXIndx[0]+1,len(QVGMEX)-10)#Aquie estas usando slice que siempre te toma uno menos 
DFQvgmex=DFQvgmex[["Unnamed: 2","Unnamed: 4"]].sort_values("Unnamed: 2").set_index("Unnamed: 2")
CEFQVGMEX=QVGMEX[Columna][20]#Aqui estas tomando indices que siempre te toma el mismo dato que le das pq es un indice
DirTemp=Direccion+"\\CANASTAS\\QVGMEX1.csv"
NombreArchivo=DirTemp
QVGMEXDash=pd.read_csv(DirTemp)
QVGMEXDash=QVGMEXDash[["Emisora","Peso"]].sort_values("Emisora").set_index("Emisora")
DFQvgmex=DFQvgmex[DFQvgmex["Unnamed: 4"]!=0]
Indices=DFQvgmex.index.to_list()

NewIndx=list(map(lambda x:x.replace(" ","",),Indices))
QVGMEXDash.index=NewIndx

Indices=DFQvgmex.index.to_list()
NewIndx=list(map(lambda x:x.replace(" ","",),Indices))
DFQvgmex.index=NewIndx


Indices1=QVGMEXDash.index.to_list()
NewIndx=list(map(lambda x:x.replace(" ","",),Indices1))
QVGMEXDash.index=NewIndx



A=QVGMEXDash["Peso"]-DFQvgmex["Unnamed: 4"]
Data={
     "Tracker":"QVGME",
     "Tamaño":sum(FibraDash["Peso"]),
     "Componente Efectivo": CEFibra
     }
Tamaño.append(sum(QVGMEXDash["Peso"]))
EFECTIVO.append(CEFQVGMEX)

if (A==0).all():
    print("No hay diferencia en QVGMEX UwU")
else:
    print("Hay diferencias en QVGMEX >:v ")
#Ojo, el index podria cambiar
#Ten mucho cuidado 
# GENIUS #
DirTemp=Direccion+"\\CANASTAS\\GENIUS.xls"
NombreArchivo=DirTemp
Columna="Unnamed: 4"
Indexador="# de títulos"
GENIUS,GENIUSIndx=Localizadora(NombreArchivo,Columna,Indexador)
DFGenius=Extractora(GENIUS,GENIUSIndx[0]+1,len(GENIUS)-10)#Aquie estas usando slice que siempre te toma uno menos 
DFGenius=DFGenius[["Unnamed: 2","Unnamed: 4"]].sort_values("Unnamed: 2").set_index("Unnamed: 2")
CEFGENIUS=GENIUS[Columna][29]#Aqui estas tomando indices que siempre te toma el mismo dato que le das pq es un indice

DirTemp=Direccion+"\\CANASTAS\\GENIUS1.xlsx"
NombreArchivo=DirTemp

GeniusDash=pd.read_excel(DirTemp)
GeniusDash=GeniusDash[["Clave de Pizarra","Acciones"]].sort_values("Clave de Pizarra").set_index("Clave de Pizarra",drop=True)
A=GeniusDash["Acciones"]-DFGenius["Unnamed: 4"]
Tamaño.append(sum(GeniusDash["Acciones"]))
EFECTIVO.append(CEFGENIUS)
if (A==0).all():
    print("No hay diferencia en GENIUS UwU")
else:
    print("Hay diferencias en GENIUS >:v ")
# MEXTRAC #

DirTemp=Direccion+"\\CANASTAS\\MEXTRAC.xls"
NombreArchivo=DirTemp
Columna="Unnamed: 4"
Indexador="Acciones"
MEXTRAC,MEXTRACIndx=Localizadora(NombreArchivo,Columna,Indexador)
DFMextrac=Extractora(MEXTRAC,MEXTRACIndx[0]+1,len(MEXTRAC)-1)#Aquie estas usando slice que siempre te toma uno menos 
DFMextrac["Unnamed: 1"]=DFMextrac["Unnamed: 1"]+DFMextrac["Unnamed: 2"]#Tengo una warning aqui 
DFMextrac=DFMextrac[["Unnamed: 1","Unnamed: 4",]].sort_values("Unnamed: 1").set_index("Unnamed: 1")
CEFMEXTRAC=MEXTRAC[Columna][len(MEXTRAC)-1]#Aqui estas tomando indices que siempre te toma el mismo dato que le das pq es un indice
DirTemp=Direccion+"\\CANASTAS\\MEXTRAC1.csv"
NombreArchivo=DirTemp
MextracDash=pd.read_csv(DirTemp)
MextracDash=MextracDash[["Emisora","Peso"]].sort_values("Emisora").set_index("Emisora")
A=MextracDash["Peso"]-DFMextrac["Unnamed: 4"]
Tamaño.append(sum(MextracDash["Peso"]))
EFECTIVO.append(CEFMEXTRAC)
if (A==0).all():
    print("No hay diferencia en Mextrac UwU")
else:
    print("Hay diferencias en Mextrac >:v ")
# ESGMEX # 

DirTemp=Direccion+"\\CANASTAS\\ESGMEX.xls"
NombreArchivo=DirTemp
Columna="Unnamed: 3"
Indexador="# de títulos"
ESGMEX,ESGMEXIndx=Localizadora(NombreArchivo,Columna,Indexador)
DFEsgmex=Extractora(ESGMEX,ESGMEXIndx[0]+1,ESGMEXIndx[1]-3)#Aquie estas usando slice que siempre te toma uno menos 
DFEsgmex=DFEsgmex[["Unnamed: 1","Unnamed: 3"]].sort_values("Unnamed: 1").set_index("Unnamed: 1")
CEFESGMEX=ESGMEX["Unnamed: 1"][17]#Aqui estas tomando indices que siempre te toma el mismo dato que le das pq es un indice
DirTemp=Direccion+"\\CANASTAS\\ESGMEX1.csv"
NombreArchivo=DirTemp
ESGMEXDash=pd.read_csv(DirTemp)

#ESGMEXDash.loc[21,"Emisora"]="SITES1A.1"#Se rompe, hay que ver como hacer  para no dejar fijo el Indice
#ESGMEXDash.loc[8,"Emisora"]="FIBRAPL14"
ESGMEXDash=ESGMEXDash[["Emisora","Peso"]].sort_values("Emisora").set_index("Emisora")
A=ESGMEXDash["Peso"]-DFEsgmex["Unnamed: 3"]
Tamaño.append(sum(ESGMEXDash["Peso"]))
EFECTIVO.append(CEFESGMEX)
if (A==0).all():
    print("No hay diferencia en ESGMEX UwU")
else:
    print("Hay diferencias en ESGMEX >:v ")  
#Falta hacer la funcion de comparacion y asi para todas las canastas, obtener todos los componentes de efectivo 
#Deoyes dakta ver archivos de las diferentes cuentas y limpiarlos para poder calcular lo faltante
#VMEX#

DirTemp=Direccion+"\\CANASTAS\\VMEX.xls"
NombreArchivo=DirTemp
Columna="Unnamed: 7"
Indexador="NÚMERO DE TITULOS POR UNIDAD"
VMEX,VMEXIndx=Localizadora(NombreArchivo,Columna,Indexador)
DFEVmex=Extractora(VMEX,VMEXIndx[0]+1,len(VMEX)-6)#Aquie estas usando slice que siempre te toma uno menos 
DFEVmex=DFEVmex[["Unnamed: 2","Unnamed: 7"]].sort_values("Unnamed: 2").set_index("Unnamed: 2")
CEFVmexX=VMEX["FTSE BIVA Mexico Index ETF"][14]#Aqui estas tomando indices que siempre te toma el mismo dato que le das pq es un indice
DirTemp=Direccion+"\\CANASTAS\\VMEX1.csv"
NombreArchivo=DirTemp
VMEXDash=pd.read_csv(DirTemp)
VMEXDash=VMEXDash[["Emisora","Peso"]].sort_values("Emisora").set_index("Emisora")
A=VMEXDash["Peso"]-DFEVmex["Unnamed: 7"]

Tamaño.append(sum(VMEXDash["Peso"]))
EFECTIVO.append(CEFVmexX)
if (A==0).all():
    print("No hay diferencia en VMEX UwU")
else:
    print("Hay diferencias en VMEX >:v ")
    
    
#################################################################################################    
#Naftrac#########################################################################################
#################################################################################################


DirTemp=Direccion+"\\CANASTAS\\NAFTRAC.xls"
NombreArchivo=DirTemp
NombreArchivo=DirTemp
Columna="Unnamed: 3"
Indexador="# de títulos"
NAFTRAC,NAFTRACIndx=Localizadora(NombreArchivo,Columna,Indexador)
DFNaftrac=Extractora(NAFTRAC,NAFTRACIndx[0]+1,NAFTRACIndx[1]-3)#Aquie estas usando slice que siempre te toma uno menos 
DFNaftrac=DFNaftrac[["Unnamed: 1","Unnamed: 3"]].sort_values("Unnamed: 1").set_index("Unnamed: 1")
CEFNAFTRAC=NAFTRAC["Unnamed: 1"][17]#Aqui estas tomando indices que siempre te toma el mismo dato que le das pq es un indice

DirTemp=Direccion+"\\CANASTAS\\NAFTRAC1.csv"
NombreArchivo=DirTemp
NAFTRACDash=pd.read_csv(DirTemp)
#NAFTRACDash.loc[3,"Emisora"]="LIVEPOLC.1" #Checar esto  
NAFTRACDash=NAFTRACDash[["Emisora","Peso"]].sort_values("Emisora").set_index("Emisora")

DFNaftrac.rename({"LIVEPOLC.1":"LIVEPOLC-1"},inplace=True)

A=NAFTRACDash["Peso"]-DFNaftrac["Unnamed: 3"]
Tamaño.append(sum(NAFTRACDash["Peso"]))
EFECTIVO.append(CEFNAFTRAC)



DirTemp=Direccion+"\\CANASTAS\\IVVPESO.xls"
NombreArchivo=DirTemp
IVVPESO=pd.read_excel(DirTemp)
IvvPorUnidad=IVVPESO["Unnamed: 3"][25]
Tamaño.append(IvvPorUnidad)
EFECTIVO.append(0)    
    
    
if (A==0).all():
    print("No hay diferencia en NAFTRAC UwU")
else:
    print("Hay diferencias en NAFTRAC >:v ")  
print("El Componente de efectivo es el que viene de los archivos de la bolsa")     
print("El componente de efectivo de ESGMEX:",CEFESGMEX)
print("El componente de efectivo de GENIUS:",CEFGENIUS)
print("El componente de efectivo de MEXTRAC:",CEFMEXTRAC)
print("El componente de efectivo de NAFTRAC:",CEFNAFTRAC)
print("El componente de efectivo de QVGMEX:",CEFQVGMEX)
print("El componente de efectivo de VMEX:",CEFVmexX)
print("El componente de efectivo de Fibra:",CEFibra)
HEDGES=["FUNO11","NAFTRACISHRS","NAFTRACISHRS","NAFTRACISHRS","NAFTRACISHRS","NAFTRACISHRS","NAFTRACISHRS","IVV*"]
Data={"Name":Lista,"Size":Tamaño,"Efectivo":EFECTIVO,"HEDGE":HEDGES,"SIZES":Sizes}
PickleFile=open("Datos","wb+")
CanastaNAFTRAC=open("CanastaNaftrac","wb+")
CanastaQVGMEX=open("CanastaQvgmex","wb+")
pickle.dump(Data, PickleFile)
pickle.dump(QVGMEXDash, CanastaQVGMEX)
pickle.dump(NAFTRACDash, CanastaNAFTRAC)
PickleFile.close()
CanastaQVGMEX.close()
CanastaNAFTRAC.close()

DatosCanastas=pd.DataFrame.from_dict(Data)
Frame=DatosCanastas.set_index("Name")
DirTemp=Direccion+"\\Datos canastas\\Datos Canastas.xlsx"
NombreArchivo=DirTemp
Frame.to_excel(DirTemp)


#Para las cruzadas
EsgmexFile=open("EsgmexPesos","ab")
pickle.dump(ESGMEXDash,EsgmexFile)
EsgmexFile.close()
NaftracFile=open("NaftracPesos","ab")
pickle.dump(NAFTRACDash,NaftracFile)
NaftracFile.close()




###################################################USITS#################################################
#########################################################################################################
#########################################################################################################
#USITS=pd.read_excel("USITS.xlsx").dropna(axis=0,how="all")
