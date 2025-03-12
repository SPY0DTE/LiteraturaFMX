import schedule

import time
from datetime import datetime,timedelta
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
import requests
import os
import time
import sys
import threading
###############################################################################
###############################################################################
Direccion=os.getcwd()
#Preparamos Todos Los Links####################################################
LastUpdate=datetime.strptime("2024-08-19 07:30 AM", '%Y-%m-%d %I:%M %p')
def EscanerEntrefechas():
    
        
    BaseLink="https://www.bmv.com.mx/" 
    LinkEventosXPagina="https://www.bmv.com.mx/es/Grupo_BMV/Sala_de_Prensa/_rid/240/_act/FILTER_APPLY?viewPage=EVENTOS_RELEVANTES&cboType=&index="
    Titulo=[]
    Detalles=[]
    Hora=[]
    Link=[]
    FechaTemp=datetime.today()
    Fecha=FechaTemp-timedelta(days=2)
    Dia=Fecha.day
    TerminamosFlag=0
    for i in range(200):#El 20 es porque al webscrapear, nosotros obtenemos acceso a las paginas de la BMV, es como un libro en el que elegimos una pagina la leemos y empezamos a procesar la info
        w=i+1
        PaginaIterada=LinkEventosXPagina+str(w)
        EventosPaginaIterada=requests.get(PaginaIterada).text
        Sopita=BeautifulSoup(EventosPaginaIterada,"lxml")
        ListaEventos=Sopita.find("table",role="presentation")
            
        for j in range(len(ListaEventos)):
            
            if ListaEventos.contents[j]!="\n":
                w3=ListaEventos.contents[j].find("p")#La hora del evento
                Texto=w3.text   #Vamos a filtrar por fecha y por hora :) 
                Texto=Texto.replace(" ","")
                Texto=Texto.replace("\n","")
                Fecha=Texto[0:10]+" "+Texto[10:15]+" "+Texto[15:]
                TextoFecha=datetime.strptime(Fecha, '%Y-%m-%d %I:%M %p')
                DayData=TextoFecha.day
                if DayData>=Dia:
                    w1=list(ListaEventos.contents[j].find_all("h2"))
                    w2=list(ListaEventos.contents[j].find_all("a"))
                    w3=list(ListaEventos.contents[j].find_all("p"))
                    Titulo.append(w1[0].text)
                    Linksito=[]
                    for k in range(len(w2)):
                        LinkTemporal=w2[k].get("href")
                        if LinkTemporal[-3:]=="pdf":
                            Linksito.append(LinkTemporal)
                    Link.append(Linksito)
                    Textito=[]
                    for s in range(len(w3)):
                        TextoTemporal=w3[s].text
                        TextoTemporal=TextoTemporal.replace(" ","")
                        TextoTemporal=TextoTemporal.replace("\n","")
                        Textito.append(TextoTemporal)
                    print("--------")
                    print(TextoFecha)
                    print(w1[0].text)
                    print(Textito[1])
                    for j in range(len(Linksito)):
                        print("https://www.bmv.com.mx"+Linksito[j])
                else:
                    TerminamosFlag=1
        if TerminamosFlag==1:
            break
                    
schedule.every().minute.at(":56").do(EscanerEntrefechas)
while True:
    schedule.run_pending()
    time.sleep(1)