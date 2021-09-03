import func_handleMissingHistoricRecords
import func_calculateMACDForhisData
import DFandFileConverter
import logging
from datetime import datetime


logging.basicConfig(filename='app.log', level=logging.DEBUG) # Creating a log file.



#TAKE HISTORIC FILE AND CREATE HIS_MACD AND LIVE_MACD FILES & RETURN LIVE_MACD DF FOR FURTHER CALCULATIONS.

def preprocessHistoricData(coinname , stringtimeinterval):

    # LOGGING
    now_start = datetime.now()
    logging.info("### ENTERED preprocessHistoricData-function : "+str(now_start))

    filenames =  func_handleMissingHistoricRecords.generateProperFilenames(coinname , stringtimeinterval)
    # 0=his_file_name , 1=his_file_name_to_append , 2=macd_file_name , 3-macd_live_file_name.
    

    macd_his_df_before_filter = func_calculateMACDForhisData.calcMACDSignalhistogramForHisData(filenames[0])
    

    macd_his_df_before_filter = func_calculateMACDForhisData.handleMACDMissingRecords(coinname , stringtimeinterval , macd_his_df_before_filter)


    next_execution_time = func_calculateMACDForhisData.validateStartTime(macd_his_df_before_filter , stringtimeinterval)
    

    macd_his_df_filtered = func_calculateMACDForhisData.dropColumnsFromMACDhisFile(macd_his_df_before_filter)
    

    DFandFileConverter.dfToFilenoindex(macd_his_df_filtered , filenames[2])
  

    live_data_initialisation_df = func_calculateMACDForhisData.initializeLiveDataDf(macd_his_df_filtered)
    
    
    DFandFileConverter.dfToFilenoindex(live_data_initialisation_df , filenames[3])
    
    # LOGGING
    now_end = datetime.now()
    logging.info("### EXITTED preprocessHistoricData-function : "+str(now_end))

    return next_execution_time