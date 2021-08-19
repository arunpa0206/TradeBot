from json import dumps
from kafka import KafkaProducer
from datetime import datetime

# Initializing a kafka-producer object, which can be listened on a kafka-consumer terminal.
producer = KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=lambda x: dumps(x).encode('utf-8'),api_version=(2, 0, 2)) #kafka starter



def kafkaproducer(coinname , topicname , df3):  # start func name with a verb

    currdatetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S') #GENERATING CURRENT DATE-TIME 

    #PUBLISHING CUTTING POINT DATA TO KAFKA CONSUMER (CURRENT TOPIC NAME - 'TESTOPIC'), IF IT IS A BUY OR SELL.
    if df3['CuttingPoint'][0] == 1: # SELL INDICATOR
        data = {"SELL AT PRICE" : df3['currPrice'][0] , "AT Date-Time" : currdatetime , "Exchange" : coinname}
        producer.send(topicname, value=data) 
    if df3['CuttingPoint'][0] == 2: # BUY INDICATOR
        data = {"BUY AT PRICE" : df3['currPrice'][0] , "AT Date-Time" : currdatetime , "Exchange" : coinname}
        producer.send(topicname, value=data) 



