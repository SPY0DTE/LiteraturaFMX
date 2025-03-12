# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 10:31:08 2023

@author: fvfentanes
"""
# from datetime import date,timedelta
# Start=date(2023,1,1)
# End=date(2023,6,1)
# delta=timedelta(days=1) #Es como un incremento/decremento para objetos tipo date time
# dates=[]
# while Start<=End:
#     dates.append(Start.isoformat())
#     Start += delta

# Calls=[]
# Puts=[]
# for i in range(dares):
#     Calls.append("Call")
#     Puts:
# Contratos={dates}

import pandas as pd
from IPython.display import display
from datetime import date
from thetadata import ThetaClient, OptionReqType, OptionRight, DateRange

client = ThetaClient()  # We don't need to provide a username / password because this is a free request.

with client.connect():  # Make any requests for data inside this block. Requests made outside this block wont run.
    data = client.get_hist_option(
          req=OptionReqType.EOD,
          root="AAPL",
          exp=date(2022, 11, 25),
          strike=150,
          right=OptionRight.CALL,
          date_range=DateRange(date(2022, 10, 15), date(2022, 11, 15))
    )
    
# We are out of the client.connect() block, so we can no longer make requests.   
display(data)  # displays the data. You can also do print(data


#SPY=ticker("SPY")
#"""
#Contraros=
    
    
 #   
  #  "Dia":"14-06-2023","",
   #       "CALLS":"SPYC061423",
    #       "PUTS":"SPYP061423",
     #       "STIKE":430""""""
          