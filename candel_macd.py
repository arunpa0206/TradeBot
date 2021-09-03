import pandas as pd 
import plotly.graph_objects as go 
import plotly 
import matplotlib.pyplot as plt


#NOTE:
#This file contains 2 functions => (1)candelStickChart , (2) - MACD and Signal chart. 
#The time and date interval which the csv file contains will be plotted.




#FUNC(1) - PLOT THE CANDELSTICK GRAPH. inputfile = Historical file of the coin , outputfile = name with which it should be stored.
def candelStickChart(inputfile , outputfile):  
    df = pd.read_csv(inputfile)

    fig = go.Figure(data=[go.Candlestick(x=df['timestamp'],
                open=df['open'],
                high=df['high'],
                low=df['low'],
                close=df['close'])])
    
    plotly.offline.plot(fig, filename = outputfile, auto_open=False)





#FUNC(2) - PLOT MACD AND SIGNAL GRAPH. inputfile = MACD file of the coin , outputfile = name with which it should be stored.
def graphMACDSignal(inputfile , outputfile):

    df = pd.read_csv(inputfile)
    plt.plot(df.Signal , label='Signal' , color='red')
    plt.plot(df.MACD , label='MACD' , color='green')
    plt.legend()
    plt.savefig(outputfile)

