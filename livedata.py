from time import sleep
from binance.websockets import BinanceSocketManager
import credential
import datetime as time #
import pandas as pd #
import numpy as np
from datetime import datetime
import kafka
import time
import extract_data_talib
import logging


logging.basicConfig(filename='app.log', encoding='utf-8', level=logging.DEBUG) # Creating a log file.


#Eventing API - LIVE COIN PRICES and LIVE KLINE VALUES for a coin.
bm = BinanceSocketManager(credential.client)


#Starts an eventing current price API for a given coin name.
def currentPriceEvent(coinname = "DOGEUSDT" , timeinterval = "5m" , topicname = "testtopic"): #inputfile = historical+macd csv file. DEFALT TIME = 5 MIN-LIVE-DATA.
    
    stri = int(timeinterval[ : -1]) # Converting interval-time from string to int for numeric calc on it later.

    ####################################################################################################################
    live_price_list = []   # Initializing a global empty list, to store the live-price influx of the coin.

    def process_message(msg):  # Function to Append the live-prices to the price-list using Socket manager.
       
        live_price_list.append(msg['p'])
        
    # Initializing an object "conn-key" to start socket manager(thread for live price) later.
    conn_key = bm.start_trade_socket(coinname, process_message)
    bm.start()  # then starting the socket manager to obtain the live-price data.
    ######################################################################################################################



    #DOWNLOADING HISTORICAL-MACD DATA FOR THE COIN.
    ############################################################################
    now_start = datetime.now()
    logging.info("Starting time of Download Operation : "+str(now_start))


    now = time.time()
    now = int(now * 1000)
    his_file_name = coinname + "_his_" + timeinterval + ".csv"
    his_file_name1 = coinname + "_his_small_" + timeinterval + ".csv"
    macd_filename = coinname + "MACD" + timeinterval + ".csv"   
    extract_data_talib.historicalCandelstickData(coinname , timeinterval , 1439352284000 , now , his_file_name) 
    
    df10 = pd.read_csv(his_file_name)
    now = time.time()
    now = int(now * 1000)
    if ((now - df10['timestamp'][df10.index[-1]])/1000) > (((stri*60*1000) + (stri*60*1000))/1000):
        extract_data_talib.historicalCandelstickData(coinname , timeinterval , df10['timestamp'][df10.index[-1]] + 1 , now , his_file_name1)
        df2 = pd.read_csv(his_file_name1)
        df3 = pd.read_csv(his_file_name)
        df3.append(df2)
        df3.to_csv('his_file_name')
    extract_data_talib.historical_To_MACD(his_file_name , macd_filename) 
    outputfilename = "curr" + macd_filename        #live-data csv file.

    now_end = datetime.now()
    logging.info("Ending time of Download Operation : "+str(now_end))
    #############################################################################




# Dropping some coulumns from our MACD-HISTORICAL csv file, as they would not be present in our dataframe.
 #################################################################################################################################   
    now_start = datetime.now()
    logging.info("Starting time of Deleting unessesary coloumns Operation : "+str(now_start))
    df10 = pd.read_csv(macd_filename)

    ##################   #5
    start_time = df10['timestamp'][df10.index[-1]]
    next_execution_time = start_time + (stri*60*1000) #TO RUN AT EVERY 5TH SECOND EXACTLY, FROM THE START TIME.
    next_execution_time_2 = start_time + (stri*60*1000) + (stri*60*1000) # incase of weak data network speed.
    next_execution_time_3 = start_time + (stri*60*1000) + (stri*60*1000) + (stri*60*1000)
    now = time.time()
    now = int(now * 1000)
    if now >= next_execution_time_2:
        next_execution_time = next_execution_time_3
    else:    
        next_execution_time = next_execution_time_2 ## THIS GIVES THE EXACLY CORRECT LIVE-RESULT WITHOUT HAVING TO ADD THE CODE TO 
                                                 ## TO MANAGE FOR THE 5TH MIN MARK(AS THIS STARTS FROM 10TH MIN MARK),
                                                 ## THIS HAPPENS BECAUSE IN THE MACD FILE WE RECORD FOR ONE TIME-PERIOD 
                                                 ## LATER, SO IT SYNCHORONIZES.

    ################# 
    
    
    df10.drop(['timestamp'] , axis = 1 , inplace = True)
    df10.drop(['open'] , axis = 1 ,  inplace = True)
    df10.drop(['high'] , axis = 1 ,  inplace = True)
    df10.drop(['low'] , axis = 1 ,  inplace = True)
    df10.drop(['close'] , axis = 1 ,  inplace = True)
    df10.drop(['vol'] , axis = 1 ,  inplace = True)
    df10.drop(['close time'] , axis = 1 ,  inplace = True)
    df10.drop(['quote asset vol'] , axis = 1 ,  inplace = True)
    df10.drop(['no of trades'] , axis = 1 ,  inplace = True)
    df10.drop(['taker buy base asset vol'] , axis = 1 ,  inplace = True)
    df10.drop(['taker buy quote asset vol'] , axis = 1 ,  inplace = True)
    df10.drop(['ignore'] , axis = 1 ,  inplace = True)
    df10.drop(['HLavg'] , axis = 1 ,  inplace = True)
    df11 = df10.iloc[-1 : ]
    ls = [0]
    df11['currPrice'] = ls
    df11.to_csv(outputfilename , index= False)

    now_end = datetime.now()
    logging.info("Ending time of Deleting unessesary coloumns Operation : "+str(now_end))
 #################################################################################################################################           

    #FUNC TO CALC EMA, MACD, SIGNAL , CUTINGPOINT, ETC . ALL IN ONE FUNC.
    def EMAandSignalcalculator(inputdf , currPrice): #inputdf = dataframe containg last rows of i - 1th time , currPrice = current price of coin.
        
        now_start = datetime.now()
        logging.info("Starting time of EMAandSignalcalculator-function : "+str(now_start))

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


        retdf = pd.DataFrame([])
        retdf['DateTime'] = date_timea
        retdf['currPrice'] = currPricea
        retdf['EMA12'] = currEMA12a
        retdf['EMA26'] = currEMA26a
        retdf['MACD'] = currMACDa
        retdf['Signal'] = currSignala
        retdf['indicator'] = currindicatora
        retdf['CuttingPoint'] = currCuttingPointa

        now_end = datetime.now()
        logging.info("Ending time of EMAandSignalcalculator-function : "+str(now_end))

        return retdf

##################################################################################################################################################

    def cuttingPoint(n , previndicator): # Calculates the cutting-Point value at 
        now_start = datetime.now()
        logging.info("Starting time of cuttingPoint-function : "+str(now_start))
        a = 0
        if n >= 0 and previndicator >= 0:
            previndicator = n
            a = 0
        elif n < 0 and previndicator >=0:
            previndicator = n
            a = 1                   #SELL
        elif n >= 0 and previndicator < 0:
            previndicator = n
            a = 2                   #BUY
        else:
            previndicator = n
            a = 0

        now_end = datetime.now()
        logging.info("Ending time of cuttingPoint-function : "+str(now_end))

        return a     


#####################################################################################################################################################
    df1 = pd.read_csv(outputfilename)
   
    while True:    
        curr_time  = int(time.time()*1000)       # This ensures that the code always runs only when it is the exact time
        while curr_time < next_execution_time:   # time for it to run.
            curr_time = int(time.time()*1000)                     
        next_execution_time = next_execution_time + (stri*60*1000)

        df2 = pd.DataFrame([]) # initializing empty dataframes to use later for live-row's data calulation.
        df3 = pd.DataFrame([])
        currPrice = float(live_price_list[-1]) # Getting the current price of the coin at this moment, from the last entry of Dynamic-list.
        
        
        df2 = df1.iloc[-1 : ]    # GETTING LAST ROW FROM DF1 TO PASS IT FOR MACD, SIGNAL, CUTTINGPOINT CALCULATION.
        df3 = EMAandSignalcalculator(df2 , currPrice) # DF3 WILL NOW CONTAIN THE LIVE ROW'S CALCULATED DATA, CALCULATED
                                                      # FROM CURRENT-PRICE AND PREV ROW'S DATA.


      
        currdatetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S') #GENERATING CURRENT DATE-TIME 


        #PUBLISHING CUTTING POINT DATA TO KAFKA CONSUMER (CURRENT TOPIC NAME - 'TESTOPIC'), IF IT IS A BUY OR SELL.
        if df3['CuttingPoint'][0] == 1: # SELL INDICATOR
            data = {"SELL AT PRICE" : df3['currPrice'][0] , "AT Date-Time" : currdatetime , "Exchange" : coinname}
            kafka.producer.send(topicname, value=data) 
        if df3['CuttingPoint'][0] == 2: # BUY INDICATOR
            data = {"BUY AT PRICE" : df3['currPrice'][0] , "AT Date-Time" : currdatetime , "Exchange" : coinname}
            kafka.producer.send(topicname, value=data) 
        
        
        df1 = df1.append(df3)
        df1.to_csv(outputfilename , index= False) # UPDATING LATEST COLOUMN TO OUR LIVE-CSV FILE.


        live_price_list.clear() # We clear the list containing all the live current price of coin at end of each loop ,as we need 
                    # only the last entry in that price-list always.

        sleep(((stri)*60) - 30) # THE TIME-INTERVAL OF LIVE DATA - 30 seconds (30 second buffer is managed at start of while 
                                # loop, putting the 30 second was unessesary here actually, but is put so that pressure on 
                                # computer is less).
                                