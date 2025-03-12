import pyautogui
import pandas as pd
pyautogui.position()  # current mouse x and y
pyautogui.size()  # current screen resolution width and height
def Boton(Name,Veces):
    for i in range(Veces):
        pyautogui.hotkey(Name)
def RegistroJAM(SIDE,NAME,SHARES,FX,PRICE,MONEDA,LIQUIDACION):
    SERIE=NAME[-1]
    pyautogui.click(x=1322, y=556, clicks=1, interval=2, button='left')
    pyautogui.typewrite(SIDE, interval=0)
    pyautogui.hotkey('tab')
    pyautogui.typewrite(NAME[:-1], interval=0)
    pyautogui.hotkey('tab')
    pyautogui.typewrite(SERIE, interval=0)
    pyautogui.hotkey('tab')
    for i in range(11):
        pyautogui.hotkey('Down')
    
    pyautogui.hotkey('tab')
    Boton("delete",10)
    pyautogui.typewrite(SHARES, interval=0)
    Boton("Tab",3)
    Boton("delete",12)
    pyautogui.typewrite(FX, interval=0)
    Boton("Tab",3)
    pyautogui.typewrite(PRICE, interval=0)
    Boton("Tab",8)
    pyautogui.typewrite(MONEDA, interval=0)
    Boton("Tab",1)
    pyautogui.typewrite(LIQUIDACION, interval=0)
    pyautogui.click(x=965, y=632, clicks=1, interval=3, button='left')
    

Ucits=pd.read_excel("UCITJAM.xlsx")

for i in Ucits.index:
    RegistroJAM(Ucits["SIDE"][i],Ucits["SECURITY"][i],str(Ucits["SHARES"][i]),str(Ucits["Dollis Ponderados"][i]),str(Ucits["Precio Ponderado"][i]),"Dolar","48 Horas")

        

















