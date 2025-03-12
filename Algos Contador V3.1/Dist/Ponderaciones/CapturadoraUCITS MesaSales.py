import pyautogui
import pandas as pd
pyautogui.position()  # current mouse x and y
pyautogui.size()  # current screen resolution width and height
def Boton(Name,Veces):
    for i in range(Veces):
        pyautogui.hotkey(Name)
def RegistroJAM(SIDE,NAME,SERIE,BROKER,SHARES,COMISON,FX,PRICE,MONEDA,LIQUIDACION):
    pyautogui.click(x=1322, y=556, clicks=1, interval=2, button='left') #Click en Capturar Operacion
    pyautogui.typewrite(SIDE, interval=0)# Escribimos Compra
    pyautogui.hotkey('tab')
    pyautogui.typewrite(NAME, interval=0) #Escribimos el name sin la serie
    pyautogui.hotkey('tab')
    pyautogui.typewrite(SERIE, interval=0) #Pónemos la serie
    pyautogui.hotkey('tab')
    pyautogui.typewrite(BROKER, interval=0) #Pónemos la serie
    pyautogui.hotkey('tab')
    Boton("delete",8)
    pyautogui.typewrite(SHARES, interval=0)
    Boton("Tab",2)#Nos vamos a la celda comison
    Boton("delete",8)
    pyautogui.typewrite(COMISON, interval=0)
    Boton("Tab",1)
    Boton("delete",8)
    pyautogui.typewrite(FX, interval=0)
    Boton("Tab",3)
    pyautogui.typewrite(PRICE, interval=0)
    Boton("Tab",8)
    pyautogui.typewrite(MONEDA, interval=0)
    Boton("Tab",1)
    pyautogui.typewrite(LIQUIDACION, interval=0)
    pyautogui.click(x=965, y=632, clicks=1, interval=3, button='left')
    

Operaciones=pd.read_excel("JAMBORI.xlsx")
Operaciones=Operaciones[Operaciones["SHARES"]>0]
for i in Operaciones.index:
    RegistroJAM(Operaciones["SIDE"][i],Operaciones["SECURITY"][i][:-1:],Operaciones["SECURITY"][i][-1],Operaciones["CLAVE NOMBRE"][i],str(Operaciones["SHARES"][i]),str(Operaciones["Comisión"][i]),str(Operaciones["FX"][i]),str(Operaciones["Price (USD)"][i]),"Dolar",str(Operaciones["LIQ"][i])+" Horas")

        



















