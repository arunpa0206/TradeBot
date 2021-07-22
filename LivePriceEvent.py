from binance.websockets import BinanceSocketManager
import clientdata

#Eventing API - LIVE COIN PRICES and LIVE KLINE VALUES for a coin.
bm = BinanceSocketManager(clientdata.client)


#Starts an eventing current price API for a given coin name.
def currentPriceEvent(coinname):
    
    def process_message(msg):
        print("Current Price: {}".format(msg['p']))

    # start any sockets here, i.e a trade socket
    conn_key = bm.start_trade_socket(coinname, process_message)

    # then start the socket manager
    bm.start()


    #time.sleep(1000)
    #bm.stop_socket(conn_key) 
    '''
    This last 2 lines here is used if we only want the live data for a 
    mall period of time, and not continously.
    '''


#Starts an eventing current Klines API for a given coin name.
def currentKlinesEvent(coinname):
    
    def process_message(msg):
        print(msg)

    # start any sockets here:
    conn_key = bm.start_kline_socket(coinname, process_message, interval=clientdata.Client.KLINE_INTERVAL_1MINUTE)


    # then start the socket manager
    bm.start()


    #time.sleep(1000)
    #bm.stop_socket(conn_key) 
    '''
    This last 2 lines here is used if we only want the live data for a 
    mall period of time, and not continously.
    '''

