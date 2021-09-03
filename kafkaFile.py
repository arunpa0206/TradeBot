from json import dumps
from kafka import KafkaProducer
from datetime import datetime
import logging
import sys
import dummy_execute_buy_sell



# FOR GURU SIR :  LINE 23 : bootstrap_servers= ['localhost:9092']
# FOR GURU SIR :  LINE 23 : KAFKA_api_version= (2, 0, 2), now is 2.3.0

logging.basicConfig(filename='app.log', level=logging.DEBUG) # Creating a log file.


# Initializing a kafka-producer object, which can be listened on a kafka-consumer terminal.

try : 
    # LOGGING
    now_start = datetime.now()
    logging.info("trying to initialize kafka-producer object at  : "+str(now_start))

    producer = KafkaProducer(bootstrap_servers= ['kafka1:19091'], value_serializer=lambda x: dumps(x).encode('utf-8'),api_version= (2, 0, 2))  #kafka starter

    # LOGGING
    now_end = datetime.now()
    logging.info("initialized kafka-producer object at : "+str(now_end))

except : 
    # LOGGING
    now_start = datetime.now()
    logging.info("(Entered except block),ERROR WHILE INITIALIZING KAFKA PRODUCER OBJECT AT : "+str(now_start))

    sys.exit("ERROR WHILE INITIALIZING KAFKA-PRODUCER OBJECT")




def kafkaproducer(coinname , topicname , df3):  # start func name with a verb

    currdatetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S') #GENERATING CURRENT DATE-TIME 

    #PUBLISHING CUTTING POINT DATA TO KAFKA CONSUMER (CURRENT TOPIC NAME - 'TESTOPIC'), IF IT IS A BUY OR SELL.
    if df3['CuttingPoint'][0] == 1: # SELL INDICATOR
        data = {"SELL AT PRICE" : df3['currPrice'][0] , "AT Date-Time" : currdatetime , "Exchange" : coinname}
        dummy_execute_buy_sell.execute_buy_sell('SELL' , df3['currPrice'][0] , coinname , currdatetime)

        try : 
            producer.send(topicname, value=data) 
    
        except : 
            print("producer.send function isnt working properly in kafkaproducer func in kafkafile.py")
            print("SELL AT PRICE :" , df3['currPrice'][0] , "AT Date-Time" , currdatetime , "EXCHANGE" , coinname)

    if df3['CuttingPoint'][0] == 2: # BUY INDICATOR
        data = {"BUY AT PRICE" : df3['currPrice'][0] , "AT Date-Time" : currdatetime , "Exchange" : coinname}
        dummy_execute_buy_sell.execute_buy_sell('BUY' , df3['currPrice'][0] , coinname , currdatetime)

        try : 
            producer.send(topicname, value=data) 

        except : 
            print("producer.send function isnt working properly in kafkaproducer func in kafkafile.py")
            print("BUY AT PRICE :" , df3['currPrice'][0] , "AT Date-Time" , currdatetime , "EXCHANGE" , coinname)

