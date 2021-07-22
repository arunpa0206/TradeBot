import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


#This modelue has a function which builds the bar graph for HLOC-avg of a particular coin from 
# its historical data csv file. We pass the filename into it , and the name of the image of 
# graph into it.

def graphHLOCavg(filename , imgname):
    cols_list = ['high' , 'low' , 'open' , 'close']
    df = pd.read_csv(filename, usecols=cols_list)                                     #

    highdata = df['high']
    lowdata = df['low']
    closedata = df['close']
    opendata = df['open']

    HLOCavg = []

    for i in range(len(opendata)):
        t =  ((highdata[i] + lowdata[i] + closedata[i] + opendata[i])/4) 
        HLOCavg.append(t)
        #print(HLOCavg)

    days = []
    for i in range(368):
        days.append(i+1)




    #simple bar graph
    x = np.array(days)
    y = np.array(HLOCavg)

    plt.plot(y , marker = 'o')
    #manager = plt.get_current_fig_manager()
    #manager.full_screen_toggle()  # Makes the graph appear in full screen mode
    plt.show()  # Shows the graph while running
    plt.savefig(imgname)                                                               #

