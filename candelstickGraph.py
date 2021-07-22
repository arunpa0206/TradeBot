import pandas as pd
import plotly.graph_objects as go


#PLOTTING THE CANDELSTICK GRAPH FOR A COIN USING ITS HISTORICAL KLINE DATA:

#The time and date interval which the csv file contains will be plotted.
#Enter name of csv-file of the currency you want the chart for.


def candelStickChart(name):  
    df = pd.read_csv(name)

    fig = go.Figure(data=[go.Candlestick(x=df['date'],
                open=df['open'],
                high=df['high'],
                low=df['low'],
                close=df['close'])])
    
    fig.show()





#1 function = accepts name of csv file of historical kline data = returns graph of candelstick.
