import prepareHistoricData
import preprocesshistoricData
import pipeline



##########################################################
coin_name = 'DOGEUSDT'
time_interval = '5m'
topic_name = 'DOGEUSDTTOPIC'
##########################################################

print("main.py is running")

prepareHistoricData.prepareHistoricData(coin_name , time_interval)

next_execution_time = preprocesshistoricData.preprocessHistoricData(coin_name , time_interval)

pipeline.mainpipeline(coin_name , time_interval , next_execution_time , topic_name)

