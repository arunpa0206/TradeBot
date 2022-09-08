# THIS IS A FILE HAVING FUNCTIONS HICH WILL HANDLE CONVERSION OF CURRENT DATAFRAME TO A CSV FILE AND VICE VERSA.


import pandas as pd
import logging
from datetime import datetime


logging.basicConfig(filename='app.log', level=logging.DEBUG) # Creating a log file.



def dfToFilewithindex(df , file_name):

    # LOGGING
    now_start = datetime.now()
    logging.info("# beginning to write to csv (func - dfToFilewithindex) : "+str(now_start))

    df.to_csv(file_name) #Saving the dataframe as a csv file, under filename passed.

    # LOGGING
    now_end = datetime.now()
    logging.info("# ended writing to csv (func - dfToFilewithindex) : "+str(now_end))


def dfToFilenoindex(df , file_name):

    # LOGGING
    now_start = datetime.now()
    logging.info("# beginning to write to csv (func - dfToFilenoindex) : "+str(now_start))

    df.to_csv(file_name , index=False)

    # LOGGING
    now_end = datetime.now()
    logging.info("# ended writing to csv (func - dfToFilenoindex) : "+str(now_end))

    return df    


def fileToDfwithindex(file_name):
    
    # LOGGING
    now_start = datetime.now()
    logging.info("# beginning to write to csv (func - fileToDfwithindex) : "+str(now_start))

    df = pd.read_csv(file_name)


    # LOGGING
    now_end = datetime.now()
    logging.info("# ended writing to csv (func - fileToDfwithindex) : "+str(now_end))

    return df

