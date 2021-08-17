import extract_data_talib
import candel_macd
import livedata
import extract_data_talib


#NOTE :
#(1)-PLEASE ADD .CSV AT THE END OF FILENAMES WHICH ARE BEING PASSED AS A PARAMETER.



#extract_data_talib.historicalCandelstickData('DOGEUSDT' , '5m' , 1501525800000, 1629079930000 , 'doge_5_his_uhgt.csv')
#currently coded for dogecoin- from its starting date to 3rd aug 2021 , at 10:16:39 AM.
#timestamp for 5 July 2019 12:00:00 = 1501525800000(opening of doge-coin)
#timestamp for 3 August 2021 10:16:39 = 1627965999000
#valid intervals - 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M



#extract_data_talib.historical_To_MACD('doge_5_his_uhgt.csv' , 'dogeMACD5_uhgt.csv')
#(3)- CONVERT A HISTORICAL DATA CSV FILE TO MACD DATA CSV FILE FOR A GIVEN COIN.




#####candel_macd.candelStickChart('dogeusdtbymin15_MACD.csv' , 'dogeusdtbymin15_Candel_Graph.html')
#####candel_macd.graphMACDSignal('dogeusdtbymin15_MACD.csv' , 'dogeusdtbymin15_MACD_Graph.png')
#(4)- PLOTTING CANDELSTICK AND MACD GRAPH(NOT LIVE GRAPH, HISTORICAL DATA GRAPH ONLY)


livedata.currentPriceEvent(coinname = "DOGEUSDT" , timeinterval = "5m" , topicname = "dogetopic") # (String 'coin-conversioncurrency_name' , String 'interval_minutes')
#(5)- LIVE EVENT FOR BUY SELL TRIGGER USING KAFKA.