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


#Eventing API - LIVE COIN PRICES and LIVE KLINE VALUES for a coin.
bm = BinanceSocketManager(credential.client)


#Starts an eventing current price API for a given coin name.
def currentPriceEvent(coinname = "DOGEUSDT" , timeinterval = "5m" , topicname = "testtopic"): #inputfile = historical+macd csv file. DEFALT TIME = 5 MIN-LIVE-DATA.
    
    stri = int(timeinterval[ : -1])

    lar = []

    def process_message(msg):
       
        lar.append(msg['p'])
        
    # start any sockets here, i.e a trade socket
    conn_key = bm.start_trade_socket(coinname, process_message)

    # then start the socket manager
    bm.start()



 #DOWNLOADING HISTORICAL-MACD DATA FOR THE COIN. #  1439352284000 - start time of doge
    ############################################################################
    now = time.time()
    now = int(now * 1000)
    his_file_name = coinname + "_his_" + timeinterval + ".csv"
    his_file_name1 = coinname + "_his_small_" + timeinterval + ".csv"
    macd_filename = coinname + "MACD" + timeinterval + ".csv"   
    extract_data_talib.historicalCandelstickData(coinname , timeinterval , 1439352284000 , now , his_file_name) #1
    
    df10 = pd.read_csv(his_file_name)
    now = time.time()
    now = int(now * 1000)

    if ((now - df10['timestamp'][df10.index[-1]])/1000) > 600:
        extract_data_talib.historicalCandelstickData(coinname , timeinterval , (df10['timestamp'][df10.index[-1]] + 1) , now , his_file_name1)
        df2 = pd.read_csv('his_file_name1')
        df3 = pd.read_csv('his_file_name')
        df3.append(df2)
        df3.to_csv('his_file_name')
    extract_data_talib.historical_To_MACD(his_file_name , macd_filename) #2    
    outputfilename = "curr" + macd_filename
    #############################################################################



# Dropping some coulumns from our MACD-HISTORICAL csv file, as they would not be present in our dataframe.
 #################################################################################################################################   
    
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
    df10.drop(['idx'] , axis = 1 ,  inplace = True)
    df10.drop(['HLavg'] , axis = 1 ,  inplace = True)
    df11 = df10.iloc[-1 : ]
    ls = [0]
    df11['currPrice'] = ls
    df11.to_csv(outputfilename , index= False)
 #################################################################################################################################           

    #FUNC TO CALC EMA, MACD, SIGNAL , CUTINGPOINT, ETC . ALL IN ONE FUNC.
    def EMAandSignalcalculator(inputdf , currPrice): #inputdf = dataframe containg last rows of i - 1th time , currPrice = current price of coin.
        df = inputdf.iloc[-1 : ]
        prevEMA12 = df['EMA12'][0]
        prevEMA26 = df['EMA26'][0]
        prevSignal = df['Signal'][0]
        prevTF = df['indicator'][0]

        alpha12 = (2 / (12 + 1))
        alpha26 = (2 / (26 + 1))
        alpha9 =  (2 / (9 + 1))

        currEMA12a , currEMA26a , currPricea , currCuttingPointa , currMACDa , currSignala , currTFa , date_timea = [] , [] , [] , [] , [] , [] , [] , []
        currEMA12 = ((currPrice * alpha12) + ((1 - alpha12) * prevEMA12))
        currEMA26 = ((currPrice * alpha26) + ((1 - alpha26) * prevEMA26))
        currMACD = currEMA12 - currEMA26
        currSignal = ((currMACD * alpha9) + ((1 - alpha9) * prevSignal))
        currTF = currMACD - currSignal
        currCuttingPoint = cuttingPoint(currTF , prevTF)
        now = datetime.now()
        date_time = now.strftime("%m/%d/%Y, %H:%M:%S")

        currEMA26a.append(currEMA26)
        currEMA12a.append(currEMA12)
        currMACDa.append(currMACD)
        currSignala.append(currSignal)
        currTFa.append(currTF)
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
        retdf['indicator'] = currTFa
        retdf['CuttingPoint'] = currCuttingPointa

        return retdf

##################################################################################################################################################

    def cuttingPoint(n , prevtf):
        a = 0
        if n >= 0 and prevtf >= 0:
            prevtf = n
            a = 0
        elif n < 0 and prevtf >=0:
            prevtf = n
            a = 1                   #SELL
        elif n >= 0 and prevtf < 0:
            prevtf = n
            a = 2                   #BUY
        else:
            prevtf = n
            a = 0

        return a    

#####################################################################################################################################################
    df1 = pd.read_csv(outputfilename)
   

    ###########
    # curr_time  = int(time.time()*1000)
    # if curr_time >= next_execution_time:
    #     next_execution_time = next_execution_time_2
    # print(next_execution_time)                                                #1
    ###########



    while True:    
        ####   #4
        curr_time  = int(time.time()*1000)       

        while curr_time < next_execution_time:
            curr_time = int(time.time()*1000)
                                              
        next_execution_time = next_execution_time + (stri*60*1000)
        ####
        df2 = pd.DataFrame([])
        df3 = pd.DataFrame([])
        currPrice = float(lar[-1])
        
        ###############
        
        df2 = df1.iloc[-1 : ]
        df3 = EMAandSignalcalculator(df2 , currPrice)

        ######################
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        ######################


        #PUBLISHING CUTTING POINT DATA TO KAFKA CONSUMER (CURRENT TOPIC NAME - 'TESTOPIC'), IF IT IS A BUY OR SELL.
        # if df3['CuttingPoint'][0] == 0:
        #     data = {"NEUTRAL AT PRICE" : df3['currPrice'][0] , "AT Time" : current_time}
        #     mykafkafile.producer.send('testtopic', value=data) 
        if df3['CuttingPoint'][0] == 1:
            #print("SELL AT PRICE : {} - AT Time : {}".format(df3['currPrice'][0] , current_time))
            data = {"SELL AT PRICE" : df3['currPrice'][0] , "AT Time" : current_time , "Exchange" : coinname}
            kafka.producer.send(topicname, value=data) 
        if df3['CuttingPoint'][0] == 2:
            #print("BUY AT PRICE : {} - AT Time : {}".format(df3['currPrice'][0] , current_time))
            data = {"BUY AT PRICE" : df3['currPrice'][0] , "AT Time" : current_time , "Exchange" : coinname}
            kafka.producer.send(topicname, value=data) 
        
        
        
        df1 = df1.append(df3)
        df1.to_csv(outputfilename , index= False) #APPENDING DF AND WRITING IT TO OUR LIVE-CSV FILE.
        
    

        lar.clear()
        sleep(((stri)*60) - 50) # THE TIME-INTERVAL OF LIVE DATA - 2 seconds (2 second buffer is at start of while loop)