import pandas as pd
import time
import logging
from datetime import datetime


logging.basicConfig(filename='app.log', level=logging.DEBUG) # Creating a log file.



 #FUNC TO CALC EMA, MACD, SIGNAL , CUTINGPOINT, ETC . ALL IN ONE FUNC.
def EMAandSignalHistogramLive(inputdf , currPrice): #inputdf = dataframe containg last rows of i - 1th time , currPrice = current price of coin.
    
    # LOGGING
    now_start = datetime.now()
    logging.info("# ENTERED EMAandSignalHistogramLive-function : "+str(now_start))


    df = inputdf.iloc[-1 : ]
    prevEMA12 = df['EMA12'][0]
    prevEMA26 = df['EMA26'][0]
    prevSignal = df['Signal'][0]
    previndicator = df['indicator'][0]

    alpha12 = (2 / (12 + 1))
    alpha26 = (2 / (26 + 1))
    alpha9 =  (2 / (9 + 1))

    currEMA12a , currEMA26a , currPricea , currCuttingPointa , currMACDa , currSignala , currindicatora , date_timea = [] , [] , [] , [] , [] , [] , [] , []
    currEMA12 = ((currPrice * alpha12) + ((1 - alpha12) * prevEMA12))
    currEMA26 = ((currPrice * alpha26) + ((1 - alpha26) * prevEMA26))
    currMACD = currEMA12 - currEMA26
    currSignal = ((currMACD * alpha9) + ((1 - alpha9) * prevSignal))
    currindicator = currMACD - currSignal
    currCuttingPoint = cuttingPoint(currindicator , previndicator)
    now = datetime.now()
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")

    currEMA26a.append(currEMA26)
    currEMA12a.append(currEMA12)
    currMACDa.append(currMACD)
    currSignala.append(currSignal)
    currindicatora.append(currindicator)
    currCuttingPointa.append(currCuttingPoint)
    currPricea.append(currPrice)
    date_timea.append(date_time)

   ###################################### DONT CHANGE THE ORDER BELOW!! OR IT WILL CAUSE PROBLEM WHILE APPENDEING LATER
    retdf = pd.DataFrame([])
    retdf['EMA12'] = currEMA12a
    retdf['EMA26'] = currEMA26a
    retdf['MACD'] = currMACDa
    retdf['Signal'] = currSignala
    retdf['indicator'] = currindicatora
    retdf['DateTime'] = date_timea
    retdf['CuttingPoint'] = currCuttingPointa
    retdf['currPrice'] = currPricea
   ########################################
   
    # LOGGING
    now_end = datetime.now()
    logging.info("# EXITTED EMAandSignalHistogramLive-function : "+str(now_end))


    return retdf





def cuttingPoint(n , previndicator): # Calculates the cutting-Point value at 
   
    # LOGGING
    now_start = datetime.now()
    logging.info("# ENTERED cuttingPoint-function : "+str(now_start))

    a = 0
    if n >= 0 and previndicator >= 0:
        previndicator = n
        a = 0
    elif n < 0 and previndicator >=0:
        previndicator = n
        a = 2                   #SELL(orignally - 1)  # ONLY HERE THE SIGNALS ARE REVERSED.
    elif n >= 0 and previndicator < 0:
        previndicator = n
        a = 1                   #BUY(originally - 2)
    else:
        previndicator = n
        a = 0
    
    # LOGGING
    now_end = datetime.now()
    logging.info("# EXITTED cuttingPoint-function : "+str(now_end))


    return a     





    
def returnLivePrice(live_price_list): #get
    
    # LOGGING
    now_start = datetime.now()
    logging.info("# ENTERED returnLivePrice-function : "+str(now_start))

    currprice = float(live_price_list[-1]) # Getting the current price of the coin at this moment, from the last entry of Dynamic-list.
    
    # LOGGING
    now_end = datetime.now()
    logging.info("# EXITTED returnLivePrice-function : "+str(now_end))

    return currprice






def timeWrapper(stri , next_execution_time): #calc the - offset , waitfornextexectime().

    # LOGGING
    now_start = datetime.now()
    logging.info("# ENTERED timeWrapper-function : "+str(now_start))

    while True:    
        curr_time  = int(time.time()*1000)       # This ensures that the code always runs only when it is the exact time
        while curr_time < next_execution_time:   # time for it to run.
            curr_time = int(time.time()*1000)                     
        next_execution_time = next_execution_time + (stri*60*1000)
        
        # LOGGING
        now_end = datetime.now()
        logging.info("# EXITTED timeWrapper-function : "+str(now_end))

        return next_execution_time

