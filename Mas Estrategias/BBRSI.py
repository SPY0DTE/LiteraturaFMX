"Este codigo hace un backtest para la estrategia de bandas de Bollinger y el RSI"
"Para el spy en el ultimo año "
"Liberrias a importar"
######################################
#Librerias a importar#################
######################################
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#plt.style.use()
Ventana=30 #Parametro a optimizar
BBpar=2
Ventana2=13

#####################################
#Definicion de funciones#############
#####################################
def BB(data,Ventana,BBpar):
    WindowMean=data["TRDPRC_1"].rolling(window=Ventana).mean()
    WindowSTD= data["TRDPRC_1"].rolling(window=Ventana).std()
    data["Banda Superior"]=WindowMean + (BBpar*WindowSTD)
    data["Banda Inferior"]=WindowMean - (BBpar*WindowSTD)
    return data
def RSI(data,Ventana2):
    delta=data["TRDPRC_1"].diff()
    gain= delta.where(delta>0,0)#Duda
    loss= delta.where(delta<0,0)#Duda
    avgGain=gain.rolling(Ventana2).mean()
    avgLoss=loss.rolling(Ventana2).mean()
    Rs=avgGain/avgLoss
    RSI=100-(100/(1+Rs))
    data["RSI"]=RSI
    data["SobreVenta"]=70
    data["SobreCompra"]=30
    return data
def Algo(data):
    Stock=0
    BuyPrice=[]
    SellPrice=[]
    INDXCPA=[]
    INDXVTA=[]
    for i in range(len(data)):
        if data["TRDPRC_1"][i]<data["Banda Inferior"][i] and data["RSI"][i]<data["SobreVenta"][i] and Stock==0:
            Stock=1
            BuyPrice.append(data["TRDPRC_1"][i])
            SellPrice.append(np.nan)
            INDXCPA.append(data["TRDPRC_1"][i])
            
        elif data["TRDPRC_1"][i]>data["Banda Superior"][i] and data["RSI"][i]>data["SobreCompra"][i] and Stock==1:
            Stock=0
            SellPrice.append(data["TRDPRC_1"][i])
            BuyPrice.append(np.nan)
            INDXVTA.append(data["TRDPRC_1"][i])
        else:
            BuyPrice.append(np.nan)
            SellPrice.append(np.nan)
    return BuyPrice,SellPrice,INDXCPA,INDXVTA          
#####################################
#Cargar la data######################
#####################################
data=pd.read_excel("SPY_Minute_Data.xlsx")
data.sort_values(by="Timestamp")
data=BB(data,Ventana,BBpar)
data=RSI(data,Ventana2)
#####################################
#Implementacion de la estrategia#####
#####################################

Buy_price,Sell_price,IndCpa,IndVta=Algo(data)
data["Buy"]=Buy_price
data["Sell"]=Sell_price

#####################################
#Graficacion#########################
#####################################


Portafolio=10000
for i in range(len(IndCpa)):
    try:
        Portafolio=Portafolio+(IndVta[i]-IndCpa[i])
        
    except:
        break
        
    
fig, ax =plt.subplots(figsize=(16,8))
plt.title("Estrategia De Trading")
plt.ylabel("Price in USD")
plt.xlabel("Dates")
ax.plot(data["TRDPRC_1"],label="Close Price",alpha=.25,color="blue")
ax.plot(data["Banda Superior"],label="Banda Superior",alpha=.25,color="yellow")
ax.plot(data["Banda Inferior"],label="Banda Inferior",alpha=.25,color="purple")
ax.fill_between(data.index,data["Banda Superior"],data["Banda Inferior"], color="grey")
ax.scatter(data.index,data["Buy"],label="Buy", alpha=1,marker="^",color="green")
ax.scatter(data.index,data["Sell"],label="Sell",alpha=1, marker="v",color="red")
plt.legend()
plt.show()   
    

        
        
    
