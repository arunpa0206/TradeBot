import credential
import pandas as pd
from datetime import datetime
import talib

#(1)-historicalCandelstickData()->To extract historical data from Binance APIs.
##############################################################################################

#Function that returns historical k-lines data.

def historicalCandelstickData(coin , interval , opentimestamp , closetimestamp , filename):
# valid intervals - 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M

    bars = credential.client.get_historical_klines(coin , interval , opentimestamp , closetimestamp)
    file_df = pd.DataFrame(bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'vol', 'close time', 'quote asset vol', 'no of trades', 'taker buy base asset vol', 'taker buy quote asset vol', 'ignore'])
    ##
    # df1 = pd.DataFrame(columns=['timestamp', 'open', 'high', 'low', 'close', 'vol', 'close time', 'quote asset vol', 'no of trades', 'taker buy base asset vol', 'taker buy quote asset vol', 'ignore'])
    # df1['timestamp'] = [0]
    # df1['open'] = [0]
    # df1['high']  = [0]
    # df1['low'] = [0]
    # df1['close'] = [0]
    # df1['vol'] = [0]
    # df1['close time'] = [0]
    # df1['quote asset vol'] = [0]
    # df1['no of trades'] = [0]
    # df1['taker buy base asset vol'] = [0]
    # df1['taker buy quote asset vol'] = [0]
    # df1['ignore'] = [0]
    # ##
    # df1.append(file_df)

    file_df.set_index('timestamp', inplace=True)
    
    #Creating an index value column(integer starting from 0) for the dataframe(Useful for graph plotting):
    a = file_df['open'].tolist()
    b = []

    for i in range(len(a)):
        b.append(i)

    file_df['idx'] = b    
    
    file_df.to_csv(filename) #Saving the dataframe as a csv file, under filename passed.





#(2)-historical_To_MACD()->To convert historical data file to MACD data file.
################################################################################################


# TAKES IN A HISTORICAL DATA-CSV FILE AND RETURNS A MACD-CSV FILE.

def historical_To_MACD(inputfile , outputfilename):
    
    df = pd.read_csv(inputfile)

    #Defining function for MACD and signal coloumn creation.
    def dFEdittingForMACD(df):

        def dateTimeCalculator(input):
            dfToList = input['timestamp'].tolist()
            resList = []

            for i in range(len(dfToList)): #'-1' was needed for the reason given just above.
                dt_object = datetime.fromtimestamp((dfToList[i]/1000))   
                resList.append(dt_object.strftime("%d/%m/%Y, %H:%M:%S"))
             
            #del resList[0]
            #last_timestamp = dfToList[len(dfToList) - 1]
            #diff_bw_two_timestamps = dfToList[len(dfToList) - 1] - dfToList[len(dfToList) - 2]
            #latest_timestamp = last_timestamp + diff_bw_two_timestamps
            #resList.append(datetime.fromtimestamp(latest_timestamp/1000).strftime("%d/%m/%Y, %H:%M:%S"))
            input['DateTime'] = pd.DataFrame(resList)

   

        df['HLavg'] = ((df['high'] + df['low'])/2)  # H-L avg of the day
        df['EMA12'] = talib.EMA(df['close'] , timeperiod = 12)  # EMA OF LAST 12 DAYS on close price
        df['EMA26'] = talib.EMA(df['close'] , timeperiod = 26)  # EMA OF LAST 26 DAYS on close price
        # df['MACD'] = df.EMA12 - df.EMA26        # MACD = EMA12 - EMA26
        
        # df['Signal'] = df.MACD.ewm(span=9 , min_periods = 9).mean()   # SIGNAL = EMA of last 9 days of MACD
        # df['indicator'] = df['MACD'] - df['Signal'] # NEEDED TO CALC CUTTING POINTS IN MACD AND SIGNAL
        df['MACD'] , df['Signal'] , df['indicator'] = talib.MACD(df['close'], fastperiod=12, slowperiod=26, signalperiod=9)     
        #If (indicator>0, then MACD > signal) at that moment and vice-versa
        dateTimeCalculator(df)
    
    #Calling function for MACD and signal coloumn creation.
    dFEdittingForMACD(df)

    # Now creating the final column in dataframe using 'indicator' column:
    
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
    df.to_csv(outputfilename , index=False)
