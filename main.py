##################################################################################################
#IMPORTING FILES WHICH ARE TO BE USED:

import historicalCandelData #1
import candelstickGraph #2
import historicalToMACD #3
import HLOCavgGraph #4
import LivePriceEvent #5
import MACDandSignal #6
##################################################################################################


#NOTE :
#(1)-PLEASE ADD .CSV AT THE END OF FILENAMES WHICH ARE BEING PASSED AS A PARAMETER.


##################################################################################################

# NOW WE WILL BE CHECKING THE FUNCTIONS CREATED IN THE DIFFERNT FILES:

########################################

#(1)- COPY THE HISORICAL DATA IN A NEW CSV FILE IN THE RANGE OF TIME PERIOD GIVEN AS PER THE
#     INTERVAL OF TIME-PERIOD GIVEN, FOR A PARTICULAR COIN.
# valid intervals - 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M
#timestamp for 1 jan 2020 at time: 00:00:00 = 1577836800000 
#timestamp for 1 jan 2021 at time: 00:00:00 = 1609459200000 
historicalCandelData.historicalCandelstickData('BTCUSDT' , '1d' , 1577836800000 , 1609459200000 , 'bitcoinhistorical.csv')

########################################

#(2)- DRAW CANDELSTICK GRAPH FROM A PARTICULAR COIN'S HISTORICAL/MACD DATA CSV FILE:
candelstickGraph.candelStickChart('bitcoinhistorical.csv')

########################################

#(3)- APPEND A HISTORICAL DATA CSV FILE TO MACD DATA CSV FILE FOR A GIVEN COIN:
historicalToMACD.historical_To_MACD('bitcoinhistorical.csv' , 'bitcoinMACD.csv')

########################################

#(4)- DRAW THE HLOC-MOVING-AVG GRAPH FROM THE HISTORICAL/MACD CSV FILE, AND SAVE IT TO THE 
#     NEW FILE PASSED AS THE SECOND ARGUEMENT:
HLOCavgGraph.graphHLOCavg('bitcoinhistorical.csv' , 'bitcoinHLOCavgGraph.png')

########################################

#(5)- LIVE EVENTING APIS FOR THE, 1-CURRENT PRICE OF A COIN(KEY-VALUE PAIR) , 2-KLINES DATA
#     FOR A COIN(JSON-FILE):

#UNCOMMENT THE NEXT LINES ONE BY ONE,
#LivePriceEvent.currentPriceEvent('BTCUSDT')
#LivePriceEvent.currentKlinesEvent('BTCUSDT')

########################################

#(6)- DRAW THE MACD-SIGNAL GRAPH FROM THE MACD-CSV FILE, AND SAVE IT TO THE NEW FILE PASSED 
#     AS THE SECOND ARGUEMENT:

MACDandSignal.graphMACDSignal('bitcoinMACD.csv' , 'bitcoinMACD.png')

########################################
