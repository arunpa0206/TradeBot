from binance.websockets import BinanceSocketManager
import credential
from time import sleep
import logging
from datetime import datetime

logging.basicConfig(filename='app.log', level=logging.DEBUG) # Creating a log file.




def getLivePricePoint(coinname , live_price_list):
    
    # LOGGING
    now_start = datetime.now()
    logging.info("# ENTERED generateProperFilenames-function : "+str(now_start))


    #Eventing API - LIVE COIN PRICES and LIVE KLINE VALUES for a coin.
    bm = BinanceSocketManager(credential.client)

    def process_message(msg):  # Function to Append the live-prices to the price-list using Socket manager.
        live_price_list.append(msg['p'])
        
        
   
    conn_key = bm.start_trade_socket(coinname, process_message)  # Initializing an object "conn-key" to start socket manager(thread for live price) later.
    bm.start()  # then starting the socket manager to obtain the live-price data.

    sleep(10) 

    # LOGGING
    now_end = datetime.now()
    logging.info("# ENTERED generateProperFilenames-function : "+str(now_end))
