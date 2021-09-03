import dummy_execute_buy_sell 
import getLivePricePoint
import func_calcMACDSignalHistogram
from time import sleep
import time
import func_handleMissingHistoricRecords
import pandas as pd
import kafkaFile
import logging
from datetime import datetime
#import rabbitSender


logging.basicConfig(filename='app.log', level=logging.DEBUG) # Creating a log file.



def mainpipeline(coinname , stringtimeinterval , next_execution_time , topicname):
    
    # LOGGING
    now_start = datetime.now()
    logging.info("### ENTERED mainpipeline-function : "+str(now_start))


    filenames = func_handleMissingHistoricRecords.generateProperFilenames(coinname , stringtimeinterval)
    # 0=his_file_name , 1=his_file_name_to_append , 2=macd_file_name , 3-macd_live_file_name.
    

    live_MACD_file_df = pd.read_csv(filenames[3])
    live_price_list = []   # Initializing a global empty list, to store the live-price influx of the coin.
    numerictimeinterval = int(stringtimeinterval[ : -1]) # Converting interval-time from string to int for numeric calc on it later
    

    getLivePricePoint.getLivePricePoint(coinname , live_price_list) # thread to update-prices-every-second
    dummy_execute_buy_sell.make_profit_loss_file(coinname , func_calcMACDSignalHistogram.returnLivePrice(live_price_list) , live_MACD_file_df.iloc[-1 : ]['DateTime'][0] )


    while True:
        
        


        next_execution_time = func_calcMACDSignalHistogram.timeWrapper(numerictimeinterval , next_execution_time)

       ##############################
        currprice = func_calcMACDSignalHistogram.returnLivePrice(live_price_list)
       

        live_MACD_file_last_row_df = live_MACD_file_df.iloc[-1 : ]    # GETTING LAST ROW FROM live_MACD_file_df TO PASS IT FOR MACD, SIGNAL, CUTTINGPOINT CALCULATION.
        
        current_MACD_row = func_calcMACDSignalHistogram.EMAandSignalHistogramLive(live_MACD_file_last_row_df , currprice) # current_MACD_row WILL NOW CONTAIN THE LIVE ROW'S CALCULATED DATA, CALCULATED
                                                    # FROM CURRENT-PRICE AND PREV ROW'S DATA.
        
        live_MACD_file_df = live_MACD_file_df.append(current_MACD_row)                                            
       ##############################

        kafkaFile.kafkaproducer(coinname , topicname , current_MACD_row) # publish to kafka.
        #rabbitSender.rabbitProducer(coinname , topicname , current_MACD_row)

        current_MACD_row.to_csv(filenames[3], mode='a', header=False , index=False)

        live_price_list.clear()


        
