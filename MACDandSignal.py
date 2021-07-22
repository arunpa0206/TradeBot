import pandas as pd
import matplotlib.pyplot as plt

#input: a MACD input file.
#PLOTTING THE MACD AND SIGNAL LINES IN A GRAPH AND SHOWING IT(NOT SAVING CURRENTLYS):


def graphMACDSignal(inputfile , outputfile):

    df = pd.read_csv(inputfile)
    plt.plot(df.signal , label='signal' , color='red')
    plt.plot(df.MACD , label='MACD' , color='green')
    plt.legend()
    plt.show()
    plt.savefig(outputfile)

