import pandas as pd


# APPENDING THE HISTORICAL CSV FILE TO A CSV FILE WHICH CONATINS MACD DATA ENTRIES.
# TAKES IN A HISTORICAL DATA-CSV FILE AND RETURNS A MACD-CSV FILE.


# APPENDING HISTORICAL CSV FILE TO MACD CSV FILE:
def historical_To_MACD(inputfile , outputfilename):
    df = pd.read_csv(inputfile)
    def dFEdittingForMACD(df):
        df['EMA12'] = df.close.ewm(span=12).mean() # EMA OF LAST 12 DAYS
        df['EMA26'] = df.close.ewm(span=26).mean() # EMA OF LAST 26 DAYS
        df['MACD'] = df.EMA12 - df.EMA26           # MACD 
        df['signal'] = df.MACD.ewm(span=9).mean()  # SIGNAL
        df['T/F'] = df['MACD'] - df['signal']      # NEEDED TO CALC CUTTING POINTS IN MACD AND SIGNAL
        #print(df)

    dFEdittingForMACD(df)

    # NOW WE ARE CALCULATING THE CUTTING POINTS OF GRAPH USING THE 'T/F' ENTRY IN THE CSV FILE.
    l = df['T/F']
    a = []
    b = True

    if l[0] >= 0:
        b = True
        a.append(0)
    else:
        b = False  
        a.append(0)


    for i in range(len(l)):
        if i == 0:
            continue
        if (l[i] >= 0) and b == True:
            a.append(0)
        elif (l[i] >= 0) and b == False:
            a.append(1) # buy trade, MACD just became more than signal
            b = True
        elif (l[i] < 0) and b == True:
            b = False
            a.append(2) #sell trade, MACD just became less than signal
        else:
            a.append(0)

    #print(a)
    #print(len(a))


    df['CuttingPoint'] = a
    #print(df)
    df.to_csv(outputfilename)