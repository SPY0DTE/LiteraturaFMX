import MetaTrader5 as mt5
from alpaca.data.live import StockDataStream
from alpaca.data.requests import StockLatestQuoteRequest
import nest_asyncio
nest_asyncio.apply()
wss_client = StockDataStream("PKQQZKCZX9NM3G02TBRU","8ALMk4v92t4vh3ss4zOYS5VObZrbwOaGSU5O6UDh")
# display data on the MetaTrader 5 package
print("MetaTrader5 package author: ",mt5.__author__)
print("MetaTrader5 package version: ",mt5.__version__)
 
# establish connection to the MetaTrader 5 terminal
if not mt5.initialize():
    print("initialize() failed, error code =",mt5.last_error())
    quit()
 
# attempt to enable the display of the GBPUSD in MarketWatch
selected=mt5.symbol_select("USDMXN",True)
if not selected:
    print("Failed to select GBPUSD")
    mt5.shutdown()
    quit()
 
# display the last GBPUSD tick
lasttick=mt5.symbol_info_tick("USDMXN")
print(lasttick)
# display tick field values in the form of a list
print("Show symbol_info_tick(\"GBPUSD\")._asdict():")

PXY=input("Danos el proxy")
S0=input("Precio de Proxy")
Spread=input("¿Spread?")
Size=input("Cuantas acciones")
Pcierre=input("Precio de cierre")
multisymbol_request_params = StockLatestQuoteRequest(symbol_or_symbols=[PXY])
async def quote_data_handler(data):
    symbol_info_tick_dict = mt5.symbol_info_tick("USDMXN")._asdict()
    BidTC=symbol_info_tick_dict["bid"]
    AskTC=symbol_info_tick_dict["ask"]
    
    BidPXY=data.bid_price
    AskPXY=data.ask_price   
    CambioBid0=1+(BidPXY-S0)/BidPXY
    CambioAsk0=1+((AskPXY-S0)/AskPXY)
    ArbitrajeC=(Pcierre*CambioBid0-Spread-.002)*BidTC
    ArbitrajeV=(Pcierre*CambioAsk0+Spread+.002)*AskTC
    
    print("Vendiendo",Size,"@",ArbitrajeV,"Comprado",Size,"@",ArbitrajeC)
wss_client.subscribe_quotes(quote_data_handler, "QQQ")
wss_client.run() 
# shut down connection to the MetaTrader 5 terminal
mt5.shutdown()