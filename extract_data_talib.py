import credential
import pandas as pd
from datetime import datetime
import talib
import logging
from datetime import datetime

logging.basicConfig(filename='app.log', level=logging.DEBUG) # Creating a log file.





#(1)-historicalCandelstickData()->To extract historical data from Binance APIs:
def historicalCandelstickData(coin , interval , opentimestamp , closetimestamp):
    
    # LOGGING
    now_start = datetime.now()
    logging.info("# ENTERED generateProperFilenames-function : "+str(now_start))
  

    bars = credential.client.get_historical_klines(coin , interval , opentimestamp , closetimestamp)
    file_df = pd.DataFrame(bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'vol', 'close time', 'quote asset vol', 'no of trades', 'taker buy base asset vol', 'taker buy quote asset vol', 'ignore'])
    #file_df.set_index('timestamp', inplace=True) #Setting 'timestamp' as the index of the dataframe.

    # LOGGING
    now_end = datetime.now()
    logging.info("# ENTERED generateProperFilenames-function : "+str(now_end))

    return file_df






#(2)-historical_To_MACD()->To convert and create MACD data file from Historical data file:
def historical_To_MACD(inputfile):

    # LOGGING
    now_start = datetime.now()
    logging.info("# ENTERED generateProperFilenames-function : "+str(now_start))
    
    df = pd.read_csv(inputfile)

    # This function when called creates columns = [DateTime,HLavg,EMA12,EMA26,MACD,Signal,indicator]
    def dFEdittingForMACD(df):

        def dateTimeCalculator(input): # Function to Add 'DateTime' coloumn in DataFrame, will be called after MACD calc.
            dfToList = input['timestamp'].tolist()
            resList = []

            for i in range(len(dfToList)): 
                dt_object = datetime.fromtimestamp((dfToList[i]/1000))   
                resList.append(dt_object.strftime("%d/%m/%Y, %H:%M:%S"))
             
            input['DateTime'] = pd.DataFrame(resList) 

        df['HLavg'] = ((df['high'] + df['low'])/2)              # Add H-L avg of the interval column
        df['EMA12'] = talib.EMA(df['close'] , timeperiod = 12)  # Add EMA OF LAST 12 DAYS on close price column
        df['EMA26'] = talib.EMA(df['close'] , timeperiod = 26)  # Add EMA OF LAST 26 DAYS on close price column
        df['MACD'] , df['Signal'] , df['indicator'] = talib.MACD(df['close'], fastperiod=12, slowperiod=26, signalperiod=9)     
        
        #If (indicator>0, then MACD > signal) at that moment and vice-versa
        dateTimeCalculator(df)                                   # Add DateTime column to dataframe
    


    #Calling function for MACD and signal coloumn creation.
    dFEdittingForMACD(df)



    # Now creating the CuttingPoint-column in dataframe using 'indicator' column:
    # 'CuttingPoint' value indicates bear/bull crossings at any given time.
    
    indicatorList = df['indicator']  #For ith cell gives info about current cell's MACD and signal position. 
    cuttingPointList = []            #Will finally be the List containing all cutting points.
    flag = True                      #For ith cell, gives info about MACD and signal position at (i-1)th cell.
    
    # Editting flag value for 1st cell.
    if indicatorList[0] >= 0:
        flag = True      # MACD above signal, at first cell.
        cuttingPointList.append(0)
    else:
        flag = False     # signal above MACD, at first cell.
        cuttingPointList.append(0)

    # Editting flag value and cutting-point value for i'th cell.
    # 0 --> NOT A CUTTING POINT.
    # 1 --> BUY trade.
    # 2 --> SELL trade.
    for i in range(len(indicatorList)):
        if i == 0:
            continue
        if (indicatorList[i] >= 0) and flag == True:    # not a cutting point
            cuttingPointList.append(0) 
        elif (indicatorList[i] >= 0) and flag == False: # buy trade, MACD just became more than signal at this point.
            cuttingPointList.append(1) 
            flag = True
        elif (indicatorList[i] < 0) and flag == True:   # sell trade, MACD just became less than signal at this point.
            flag = False
            cuttingPointList.append(2)
        else:                                           # not a cutting point
            cuttingPointList.append(0) 


    df['CuttingPoint'] = cuttingPointList

    # LOGGING
    now_end = datetime.now()
    logging.info("# ENTERED generateProperFilenames-function : "+str(now_end))

    return df
