import pandas as pd
from backtesting import Backtest
from backtesting import Strategy
from backtesting.lib import crossover
def BB(values, n):
    Prom=pd.Series(values).rolling(n).mean()
    Desv=pd.Series(values).rolling(n).std()
    BandInf=Prom-2*Desv
    BandSup=Desv+2*Desv
    """
    Return simple moving average of `values`, at
    each step taking into account `n` previous values.
    """
    return Prom,Desv,BandInf,BandSup
def RSI(values,n):
    delta=pd.Series(values).diff()
    gain= delta.where(delta>0,0)#Duda
    loss= delta.where(delta<0,0)#Duda
    avgGain=gain.rolling(n).mean()
    avgLoss=loss.rolling(n).mean()
    Rs=avgGain/avgLoss
    RSI=100-(100/(1+Rs))
    return RSI

class SmaCross(Strategy):
    # Define the two MA lags as *class variables*
    # for later optimization
    n = 10
    
    
    def init(self):
        # Precompute the two moving averages
        self.bb1 = self.I(BB, self.data.Close, self.n)
        self.rsi1 = self.I(RSI, self.data.Close, self.n)
    
    def next(self):
        # If sma1 crosses above sma2, close any existing
        # short trades, and buy the asset
        if self.data.Close<self.bb1.BandaInf() and self.rsi1<70:
            
            self.position.close()
            self.buy()

        # Else, if sma1 crosses below sma2, close any existing
        # long trades, and sell the asset
        elif self.data.Close>BandaSup and  self.rsi1>30:
            self.position.close()
            self.sell()
            
            
            
            
            
data=pd.read_excel("SPY_Minute_Data.xlsx").dropna()
bt = Backtest(data, SmaCross, cash=10_000, commission=.002)
stats = bt.run()
print(stats)
bt.plot()