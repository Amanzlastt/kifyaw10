import pandas as pd 
import numpy as np

from sklearn.preprocessing import StandardScaler
from sklearn.impute import KNNImputer

class PreProcessing(StandardScaler, KNNImputer):
    def __init__(self):
        pass
    def impute(self,df):
        df=df.dropna(axis = 1, how='all')
        df['Date'] = pd.to_datetime(df['Date'])
        df.set_index('Date', inplace = True)
        imputer = KNNImputer(n_neighbors=5)
        imputed_values = imputer.fit_transform(df)
        df_imputed = pd.DataFrame(imputed_values, index=df.index, columns=df.columns)
        return df_imputed
    def scalle(self,df):
        scaler = StandardScaler()
        scaled_values = scaler.fit_transform(df)
        df_scalled = pd.DataFrame(scaled_values, index=df.index, columns=df.columns )
        return df_scalled
    