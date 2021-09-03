import pandas as pd
import extract_data_talib
import time
import logging
from datetime import datetime

logging.basicConfig(filename='app.log', level=logging.DEBUG) # Creating a log file.


def generateProperFilenames(coinname , stringtimeinterval): #returns a tuple containing 3 file-names

    # LOGGING
    now_start = datetime.now()
    logging.info("# ENTERED generateProperFilenames-function : "+str(now_start))


    now = time.time()
    now = int(now * 1000)
    his_file_name = coinname + "_his_file_" + stringtimeinterval + ".csv"
    his_file_name_to_append = coinname + "_his_file_to_append_" + stringtimeinterval + ".csv"
    macd_his_file_name = coinname + "_MACD_file_for_his_data_" + stringtimeinterval + ".csv" 
    macd_live_file_name = "curr" + macd_his_file_name        #live-data csv file.  

    # LOGGING
    now_end = datetime.now()
    logging.info("# EXITTED from generateProperFilenames-function : "+str(now_end))


    return his_file_name , his_file_name_to_append , macd_his_file_name , macd_live_file_name





def extratHistoricalData(coinname , timeinterval): #c
    
    # LOGGING
    now_start = datetime.now()
    logging.info("# ENTERED extractHistoricalData-function : "+str(now_start))


    now = time.time()
    now = int(now * 1000)
    binance_start_date_timestamp = 1439352284000

    df =  extract_data_talib.historicalCandelstickData(coinname , timeinterval , binance_start_date_timestamp , now)
    
    now_end = datetime.now()
    logging.info("# EXITTED from extractHistoricalData-function : "+str(now_end))
    
    
    return df





def handleHistoricMissingRecords(coinname , stringtimeinterval , his_file_df):

    # LOGGING
    now_start = datetime.now()
    logging.info("# ENTERED handleHistoricMissingRecords-function : "+str(now_start))

    
    diffbwtwotimestamps = diffBwTimePeriodsOfLiveData(stringtimeinterval)
    now = time.time()
    now = int(now * 1000)

    while ((now - his_file_df['timestamp'][his_file_df.index[-1]])/1000) > (2 * diffbwtwotimestamps):
        now = time.time()
        now = int(now * 1000)
        df2 = extract_data_talib.historicalCandelstickData(coinname , stringtimeinterval , his_file_df['timestamp'][his_file_df.index[-1]] + diffbwtwotimestamps + 1 , now)
        his_file_df.append(df2)


    now_end = datetime.now()
    logging.info("# EXITTED from handleHistoricMissingRecords-function : "+str(now_end))

    return his_file_df    





def diffBwTimePeriodsOfLiveData(stringtimeinterval):

    # LOGGING
    now_start = datetime.now()
    logging.info("# ENTERED diffBwtimePeriodsOfLivedata-function : "+str(now_start))

    numerictimeinterval = int(stringtimeinterval[ : -1]) # Converting interval-time from string to int for numeric calc on it later
    time_period_string = stringtimeinterval[-1]
    time_period_int = 0
    if time_period_string == 'm':
        time_period_int = numerictimeinterval*60*1000
    elif time_period_string == 'h':
        time_period_int = numerictimeinterval*60*60*1000 # 1hr => 60 * 60 sec    
    elif time_period_string == 'd':
        time_period_int = numerictimeinterval*60*60*24*1000    
    elif time_period_string == 'w':
        time_period_int = numerictimeinterval*60*60*24*7*1000
    else: # 'M' = month!
        time_period_int = numerictimeinterval*60*60*24*7*30*1000    

    now_end = datetime.now()
    logging.info("# EXITTED from diffBwTimePeriodsOfLiveData-function : "+str(now_end))


    return time_period_int    





