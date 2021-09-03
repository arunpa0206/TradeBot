import extract_data_talib
import time
import logging
from datetime import datetime
import func_calcMACDSignalHistogram
import pandas as pd

logging.basicConfig(filename='app.log', level=logging.DEBUG) # Creating a log file.


def calcMACDSignalhistogramForHisData(his_file_name):

    # LOGGING
    now_start = datetime.now()
    logging.info("# ENTERED calcMACDSignalhistogramForHisData-function : "+str(now_start))

    macd_his_df =  extract_data_talib.historical_To_MACD(his_file_name) 

    # LOGGING
    now_end = datetime.now()
    logging.info("# EXITTED from calcMACDSignalhistogramForHisData-function : "+str(now_end))

    return macd_his_df







def validateStartTime(macd_his_df_before_filter , stringtimeinterval): #this function runs before dropping columns.
   
    # LOGGING
    now_start = datetime.now()
    logging.info("# ENTERED validateStartTime-function : "+str(now_start))


    start_time = macd_his_df_before_filter['timestamp'][macd_his_df_before_filter.index[-1]]
    diffbwtwotimestamps = diffBwTimePeriodsOfLiveData(stringtimeinterval)
    
    next_execution_time = start_time + diffbwtwotimestamps #TO RUN AT EVERY 5TH SECOND EXACTLY, FROM THE START TIME.
    next_execution_time_2 = start_time + (2 * diffbwtwotimestamps) # incase of weak data network speed.
    next_execution_time_3 = start_time + (3 * diffbwtwotimestamps)
    
    now = time.time()
    now = int(now * 1000)
    
    if now >= next_execution_time_2:
        next_execution_time = next_execution_time_3
    else:    
        next_execution_time = next_execution_time_2 ## THIS GIVES THE EXACLY CORRECT LIVE-RESULT WITHOUT HAVING TO ADD THE CODE TO 
                                                 ## TO MANAGE FOR THE 5TH MIN MARK(AS THIS STARTS FROM 10TH MIN MARK),
                                                 ## THIS HAPPENS BECAUSE IN THE MACD FILE WE RECORD FOR ONE TIME-PERIOD 
                                                 ## LATER, SO IT SYNCHORONIZES.

    # LOGGING
    now_end = datetime.now()
    logging.info("# EXITTED from validateStartTime-function : "+str(now_end))


    return next_execution_time                                             





def diffBwTimePeriodsOfLiveData(stringtimeinterval):

    # LOGGING
    now_start = datetime.now()
    logging.info("# ENTERED diffBwTimePeriodsOfLiveData-function : "+str(now_start))


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
        time_period_int = numerictimeinterval*60*60*24*30*1000    


    # LOGGING
    now_end = datetime.now()
    logging.info("# EXITTED from diffBwTimePeriodsOfLiveData-function : "+str(now_end))    

    return time_period_int    






def dropColumnsFromMACDhisFile(macd_his_df_before_filter):

    # LOGGING
    now_start = datetime.now()
    logging.info("# ENTERED dropColumnsFromMACDhisFile-function : "+str(now_start))


    macd_his_df_before_filter.drop(['timestamp'] , axis = 1 , inplace = True)
    macd_his_df_before_filter.drop(['open'] , axis = 1 ,  inplace = True)
    macd_his_df_before_filter.drop(['high'] , axis = 1 ,  inplace = True)
    macd_his_df_before_filter.drop(['low'] , axis = 1 ,  inplace = True)
    macd_his_df_before_filter.drop(['close'] , axis = 1 ,  inplace = True)
    macd_his_df_before_filter.drop(['vol'] , axis = 1 ,  inplace = True)
    macd_his_df_before_filter.drop(['close time'] , axis = 1 ,  inplace = True)
    macd_his_df_before_filter.drop(['quote asset vol'] , axis = 1 ,  inplace = True)
    macd_his_df_before_filter.drop(['no of trades'] , axis = 1 ,  inplace = True)
    macd_his_df_before_filter.drop(['taker buy base asset vol'] , axis = 1 ,  inplace = True)
    macd_his_df_before_filter.drop(['taker buy quote asset vol'] , axis = 1 ,  inplace = True)
    macd_his_df_before_filter.drop(['ignore'] , axis = 1 ,  inplace = True)
    macd_his_df_before_filter.drop(['HLavg'] , axis = 1 ,  inplace = True)
    
    macd_his_df_filtered = macd_his_df_before_filter

    # LOGGING
    now_end = datetime.now()
    logging.info("# EXITTED from dropColumnsFromMACDhisFile-function : "+str(now_end))


    return macd_his_df_filtered





def initializeLiveDataDf(filtered_macd_df):

    # LOGGING
    now_start = datetime.now()
    logging.info("# ENTERED initializeLiveDataDf-function : "+str(now_start))


    df_for_macd_live_file_initialization = filtered_macd_df.iloc[-1 : ]
    currprice = [0]
    df_for_macd_live_file_initialization['currPrice'] = currprice

    # LOGGING
    now_end = datetime.now()
    logging.info("# EXITTED from initializeLiveDataDf-function : "+str(now_end))

    return df_for_macd_live_file_initialization





    #################################################################




def handleMACDMissingRecords(coinname , stringtimeinterval , macd_file_df):

    # LOGGING
    now_start = datetime.now()
    logging.info("# ENTERED handleMACDMissingRecords-function : "+str(now_start))


    diffbwtwotimestamps = diffBwTimePeriodsOfLiveData(stringtimeinterval)
    now = time.time()
    now = int(now * 1000)

    while ((now - macd_file_df['timestamp'][macd_file_df.index[-1]])/1000) > (2 * diffbwtwotimestamps):
        now = time.time()
        now = int(now * 1000)
        last_row_macd_before_handling = macd_file_df.iloc[-1 : ]
        new_his_df = extract_data_talib.historicalCandelstickData(coinname , stringtimeinterval , macd_file_df['timestamp'][macd_file_df.index[-1]] + diffbwtwotimestamps + 1 , now)
        
        df2 = pd.DataFrame([])
        closepricesnew = new_his_df['close'].tolist()
        for i in range(len(closepricesnew)):
            df1 = func_calcMACDSignalHistogram.EMAandSignalHistogramLive(last_row_macd_before_handling , i)
            df2 = df2.append(df1)
        
        macd_file_df.append(df2)


    now_end = datetime.now()
    logging.info("# EXITTED from handleMACDMissingRecords-function : "+str(now_end))

    return macd_file_df    
