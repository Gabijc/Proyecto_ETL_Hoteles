import pandas as pd
import numpy as np

# Función info de dataframes 
def info_df(dataframe):
    """
    Función que devuelve información general sobre el DatFrame que le pasemos.


    Args:
        df (DataFrame): DataFrame con información que queramos revisar

    Returns:
        DataFrame: DataFrame con información general sobre las columnas del DataFrame que se le ha pasado a la función: tipo de datos, número de
        registros, número de valores nulos, porcentaje de los valores nulos sobre el total
    """
    info_df = pd.DataFrame()
    info_df["Tipo_dato"] = dataframe.dtypes
    info_df["numero_registros"] = [dataframe[elemento].value_counts().sum() for elemento in dataframe]
    info_df["Numero_nulos"] = round(dataframe.isnull().sum())
    info_df["%_nulos"] = round((dataframe.isnull().sum()/dataframe.shape[0])*100, 2)

    return info_df