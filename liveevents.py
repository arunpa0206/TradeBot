from time import sleep
from binance.websockets import BinanceSocketManager
import credential
import datetime as time #
import pandas as pd #
import numpy as np
from datetime import datetime
import time
import mykafkafile
import extract_data
import time


#Eventing API - LIVE COIN PRICES and LIVE KLINE VALUES for a coin.
bm = BinanceSocketManager(credential.client)


#Starts an eventing current price API for a given coin name.
def currentPriceEvent(coinname , timeinterval = "5m"): #inputfile = historical+macd csv file. DEFALT TIME = 5 MIN-LIVE-DATA.
    
    #DOWNLOADING HISTORICAL-MACD DATA FOR THE COIN.
    ############################################################################
    now = time.time()
    now = int(now * 1000)
    his_file_name = coinname + "_his_" + timeinterval + ".csv"
    macd_filename = coinname + "MACD" + timeinterval + ".csv"
    extract_data.historicalCandelstickData(coinname , timeinterval , 1501525800000 , now , his_file_name)
    extract_data.historical_To_MACD(his_file_name , macd_filename)
    #############################################################################
    
    lar = []

    def process_message(msg):
       
        lar.append(msg['p'])
        
    # start any sockets here, i.e a trade socket
    conn_key = bm.start_trade_socket(coinname, process_message)

    # then start the socket manager
    bm.start()


# Dropping some coulumns from our MACD-HISTORICAL csv file, as they would not be present in our dataframe.
 #################################################################################################################################   
    
    df10 = pd.read_csv(macd_filename)
    
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
    df11.to_csv('curr.csv' , index= False)
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
    df1 = pd.read_csv('curr.csv')
    sleep(6) # INITIAL SLEEP IS REQUIRED FOR DATA CONNECTION TO BE ESTABLISHED WITH THE SERVER OF BINANCE FOR LIVE DATA.

    while True:    
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
            data = {"SELL AT PRICE" : df3['currPrice'][0] , "AT Time" : current_time}
            mykafkafile.producer.send('testtopic', value=data) 
        if df3['CuttingPoint'][0] == 2:
            data = {"BUY AT PRICE" : df3['currPrice'][0] , "AT Time" : current_time}
            mykafkafile.producer.send('testtopic', value=data) 
        

        df1 = df1.append(df3)
        df1.to_csv('curr.csv' , index= False) #APPENDING DF AND WRITING IT TO OUR LIVE-CSV FILE.
        
        stri = int(timeinterval[ : -1])
        sleep(((stri)*60)) # THE TIME-INTERVAL OF LIVE DATA.
        

































