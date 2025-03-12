## IMPORTAMOS LAS LIBRERIAS
######################
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
import requests
import os
Direccion=os.getcwd()
######################
#Preparamos Todos Los Links
TodayDate=datetime.now()
DiaHoy=TodayDate.day
MesHoy=TodayDate.month
requests.get("https://www.bmv.com.mx/es/emisoras/informcioncorporativa/FIBRATC-31496-CGEN_CAPIT").text
Html_Esgmex=requests.get("https://www.bmv.com.mx/es/emisoras/informcioncorporativa/ESGMEX-34471-CGEN_CAPIT").text
Html_Mextrac=requests.get("https://www.bmv.com.mx/es/emisoras/informcioncorporativa/MEXTRAC-7220-CGEN_CAPIT").text
Html_Naftrac=requests.get("https://www.bmv.com.mx/es/emisoras/informcioncorporativa/NAFTRAC-6101-CGEN_CAPIT").text
Html_QVGMEX=requests.get("https://www.bmv.com.mx/es/emisoras/informcioncorporativa/QVGMEX-32995-CGEN_CAPIT").text
Html_IVVPESO=requests.get("https://www.bmv.com.mx/es/emisoras/informcioncorporativa/IVVPESO-31537-CGEN_CAPIT").text
Html_Fibra=requests.get("https://www.bmv.com.mx/es/emisoras/informcioncorporativa/FIBRATC-31496-CGEN_CAPIT").text
Html_Genius=requests.get("https://www.bmv.com.mx/es/emisoras/informcioncorporativa/GENIUS-34417-CGEN_CAPIT").text
Html_VMEX=requests.get("https://biva.mx/empresas/emisoras_inscritas/banco_de_informacion?tipoInstrumto=&tipoInformacion=&type=null&tipoDocumento=&fechaInicio=&fechaFin=&emisora_id=2746&periodo=&ejercicio=&page=1").text

#Apuntadores de cada archivo de la bolsa
# FIBRA---> 7
# ESGMEX--> 3
# MEXTRAC--> 7
# NAFTRAC --> 3
# QVGMEX --> 1
# IVVPESO --> 1
# Genius --> 3

def ScrapperBMV(HTML,Apuntador):
    BaseLink="https://www.bmv.com.mx/" 
    Soup=BeautifulSoup(HTML,"lxml")
    a=Soup.find("ul",class_="accordion-area accordion-area-2")
    EventosCorporativos=a.contents[Apuntador]# Para el archivo de Fibra aplica esto solamente por como esta  construida la pagina en la BMV
    PrimeraFila=EventosCorporativos.find_all("tr",limit=2)
    CuadranteFibra=PrimeraFila[1]
    FechaLink=CuadranteFibra.find("td").text
    DiaArchivo=int(FechaLink[0:2])
    MesArchivo=int(FechaLink[3:5])
    LinkExcellClass=CuadranteFibra.find("a")
    LinkExcelPreliminar=LinkExcellClass.get("href")
    LinkFinal=BaseLink+LinkExcelPreliminar
    return DiaArchivo,MesArchivo,LinkFinal

DireccionCanastas=Direccion+"\\CANASTAS\\"
Files=os.listdir(DireccionCanastas)
Blindados=["IVVPESOCALCULADORA NEW.xlsm","ESGMEX.xls",
           "FIBRA.xls","GENIUS.xls","IVVPESO.xls","MEXTRAC.xls","NAFTRAC.xls",
           "QVGMEX.xls","VMEX.xls","GENIUS1.xlsx"] #Estos son los que no vamos a borrar Todo lo demas si se va a borrar

DiaArchivo,MesArchivo,LinkFinalFibra=ScrapperBMV(Html_Fibra,7)
Filename=("FIBRA")
r=requests.get(LinkFinalFibra,allow_redirects=True)
open(Direccion+"\\CANASTAS\\"+Filename+".xls","wb").write(r.content)

DiaArchivo,MesArchivo,LinkFinalEsgmex=ScrapperBMV(Html_Esgmex,3)

Filename=("ESGMEX")
r=requests.get(LinkFinalEsgmex,allow_redirects=True)
open(Direccion+"\\CANASTAS\\"+Filename+".xls","wb").write(r.content)

DiaArchivo,MesArchivo,LinkFinalMextrac=ScrapperBMV(Html_Mextrac,7)

Filename=("MEXTRAC")
r=requests.get(LinkFinalMextrac,allow_redirects=True)
open(Direccion+"\\CANASTAS\\"+Filename+".xls","wb").write(r.content)

DiaArchivo,MesArchivo,LinkFinalNaftrac=ScrapperBMV(Html_Naftrac,3)

Filename=("NAFTRAC")
r=requests.get(LinkFinalNaftrac,allow_redirects=True)
open(Direccion+"\\CANASTAS\\"+Filename+".xls","wb").write(r.content)

DiaArchivo,MesArchivo,LinkFinalQvgmex=ScrapperBMV(Html_QVGMEX,1)

Filename=("QVGMEX")
r=requests.get(LinkFinalQvgmex,allow_redirects=True)
open(Direccion+"\\CANASTAS\\"+Filename+".xls","wb").write(r.content)

DiaArchivo,MesArchivo,LinkFinalIVVPESO=ScrapperBMV(Html_IVVPESO,1)

Filename=("IVVPESO")
r=requests.get(LinkFinalIVVPESO,allow_redirects=True)
open(Direccion+"\\CANASTAS\\"+Filename+".xls","wb").write(r.content)

DiaArchivo,MesArchivo,LinkFinalGenius=ScrapperBMV(Html_Genius,3)

Filename=("GENIUS")
r=requests.get(LinkFinalGenius,allow_redirects=True)
open(Direccion+"\\CANASTAS\\"+Filename+".xls","wb").write(r.content)

for i in Files:
    if i not in Blindados:
        w=DireccionCanastas+i
        os.remove(w)



# for file in Files:
#     if 

    
    # if DiaArchivo==(DiaHoy-1) and MesArchivo==MesHoy:
    #     LinkExcellClass=CuadranteFibra.find("a")
    #     LinkExcelPreliminar=LinkExcellClass.get("href")
    #     LinkFinal=BaseLink+LinkExcelPreliminar
    #     print("Su Link Señor",LinkFinal)
    # elif DiaArchivo==(DiaHoy-3) and MesArchivo==MesHoy:
    #     LinkExcellClass=CuadranteFibra.find("a")
    #     LinkExcelPreliminar=LinkExcellClass.get("href")
    #     LinkFinal=BaseLink+LinkExcelPreliminar
    #     print("Su Link Señor",LinkFinal)
    # else:
    #     print("Hay Algo raro")
#Filename=("FIBRA")
#r=requests.get(LinkFinal,allow_redirects=True)
#open(Filename+".xls","wb").write(r.content)