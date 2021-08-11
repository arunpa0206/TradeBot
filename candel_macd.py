import pandas as pd
import plotly.graph_objects as go
import plotly
import matplotlib.pyplot as plt


#NOTE:
#The time and date interval which the csv file contains will be plotted.
#Enter name of csv-file of the currency you want the chart from the 'main' file.


#PLOTTING THE CANDELSTICK GRAPH FOR A COIN USING ITS HISTORICAL KLINE DATA:
def candelStickChart(inputfile , outputfile):  
    df = pd.read_csv(inputfile)

    fig = go.Figure(data=[go.Candlestick(x=df['timestamp'],
                open=df['open'],
                high=df['high'],
                low=df['low'],
                close=df['close'])])
    
    #fig.show()
    plotly.offline.plot(fig, filename = outputfile, auto_open=False)




#input: a MACD input file.
#PLOTTING THE MACD AND SIGNAL LINES IN A GRAPH AND SHOWING IT:

def graphMACDSignal(inputfile , outputfile):

    df = pd.read_csv(inputfile)
    plt.plot(df.Signal , label='Signal' , color='red')
    plt.plot(df.MACD , label='MACD' , color='green')
    plt.legend()
    plt.savefig(outputfile)

