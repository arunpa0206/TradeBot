import pandas as pd


def dfToFilewithindex(df , file_name):
    df.to_csv(file_name) #Saving the dataframe as a csv file, under filename passed.


def dfToFilenoindex(df , file_name):
    df.to_csv(file_name , index=False)
    return df    


def fileToDfwithindex(file_name):
    df = pd.read_csv(file_name)
    return df

