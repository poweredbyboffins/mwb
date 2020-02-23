import psycopg2
import pandas as pd
import numpy as np

class pander:

    def __init__(self, df):
            self.df = df
             
    
    def sumhome(self,df,type):
    #frames=[dfh,dfa]
    #df3=pd.concat(frames)
        dfsum=self.df.groupby('hometeam').sum()
        dftop=dfsum.sort_values(by=type,ascending=False).head(10)
        return dftop
    
    def mean(self,df,type):
        dfmean=self.df.groupby('hometeam').mean()
        dftop2=dfmean.sort_values(by=type,ascending=False).head(10)
        return dftop2

    def json(self,df):
        return df.to_json(orient='index')

    def movingAverage(self,df):
        dfrm=pd.rolling_mean(self.df['fthr'],window=3)
        return dfrm
