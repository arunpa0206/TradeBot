import func_handleMissingHistoricRecords
import DFandFileConverter
import logging
from datetime import datetime


logging.basicConfig(filename='app.log', level=logging.DEBUG) # Creating a log file.



def prepareHistoricData(coinname , stringtimeinterval): #finally we will have a fully updated to the current time, historical data.

    # LOGGING
    now_start = datetime.now()
    logging.info("### ENTERED prepareHistoricData-function : "+str(now_start))


    filenames = func_handleMissingHistoricRecords.generateProperFilenames(coinname , stringtimeinterval) 
    # 0-his_file_name , 1-his_file_name_to_append , 3-macd_file_name

    
    his_file_df =  func_handleMissingHistoricRecords.extratHistoricalData(coinname , stringtimeinterval)

    
    his_updated_file_df = func_handleMissingHistoricRecords.handleHistoricMissingRecords(coinname , stringtimeinterval , his_file_df)
    

    DFandFileConverter.dfToFilenoindex(his_updated_file_df , filenames[0])

    # LOGGING
    now_end = datetime.now()
    logging.info("### EXITTED prepareHistoricData-function : "+str(now_end))
    
