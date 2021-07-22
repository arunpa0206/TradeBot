import clientdata
import pandas as pd


#This module has a function which returns to us a csv file containing the historical
# klines(candelstick) data for a particular coin during a particular timestamp range for the 
# specified interval. The csv file is saved with the name passed as 'filename'(last parameter).


def historicalCandelstickData(coin , interval , opentimestamp , closetimestamp , filename):
# valid intervals - 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M
#timestamp for 1 jan 2020 at time: 00:00:00 = 1577836800000 
#timestamp for 1 jan 2021 at time: 00:00:00 = 1609459200000 
#timestamp for yesterday at time: 00:00:00 = 1626134400000

    bars = clientdata.client.get_historical_klines(coin , interval , opentimestamp , closetimestamp)
    file_df = pd.DataFrame(bars, columns=['date', 'open', 'high', 'low', 'close', 'vol', 'close time', 'quote asset vol', 'no of trades', 'taker buy base asset vol', 'taker buy quote asset vol', 'ignore'])
    file_df.set_index('date', inplace=True)
#print(btc_df.head())       
# export DataFrame to csv
    file_df.to_csv(filename)        

