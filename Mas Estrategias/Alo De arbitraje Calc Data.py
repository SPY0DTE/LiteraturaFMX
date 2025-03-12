import base64
import json
from bytewax.dataflow import Dataflow
from bytewax.inputs import ManualInputConfig, distribute
from websocket import create_connection
ticker_list = ['AZTD', 'SPY']
def yf_input(worker_tickers, state):
        ws = create_connection("wss://streamer.finance.yahoo.com/")
        ws.send(json.dumps({"subscribe": worker_tickers}))
        while True:
            yield state, ws.recv()

def input_builder(worker_index, worker_count, resume_state):
    state = resume_state or None
    worker_tickers = list(distribute(ticker_list, worker_index, worker_count))
    print({"subscribing to": worker_tickers})
    return yf_input(worker_tickers, state)

flow = Dataflow()
flow.input("input", ManualInputConfig(input_builder))




#data=yf.download(tickers="SPY",period=!"")
#Tickers=["MXN=X","AZTD"]
#current_price = web.yahoo.quotes.YahooQuotesReader(symbols="AZTD", start=None, end=None, retry_count=3, pause=0.1, session=None)["regularMarketPrice"]
#Como obtienes iformacion en tiempo real de YAHOO FINANCE CON Web Sockets?
#Que api usar?




spread=float(input("Introduce el spread: "))
Size=float(input("Introduce el size: "))

A=True
while A:

    
#web.pandas_datareader.yahoo.quotes.YahooQuotesReader(symbols="SPY", start=None, end=None, retry_count=3, pause=0.1, session=None)