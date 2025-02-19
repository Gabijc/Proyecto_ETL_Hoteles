import pandas as pd
import numpy as np
from pandas.api.types import is_datetime64_any_dtype as is_datetime

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


# Creamos una función que nos modifica el tipo de dato de las columnas que le pasemos a tipo fecha
def data_fechas(dataframe, columnas):
    """
    Convierte las columnas especificadas de un DataFrame a tipo datetime.

    Args:
        dataframe (pd.DataFrame): DataFrame que contiene las columnas a modificar.
        columnas (list): Lista de nombres de las columnas a convertir a datetime.

    Returns:
        pd.DataFrame: DataFrame con las columnas especificadas convertidas a datetime.
    """
    for col in columnas:
        dataframe[col] = pd.to_datetime(dataframe[col])
    return dataframe

# Creamos una funcion que nos modifica los indices de las columnas que le pasemos, en este caso el de id de hotel e id de cliente
def cambio_id(dataframe, lista_columnas):
    
    lista = dataframe[lista_columnas[0]].unique()
    diccionario = {}
    conteo = 1
    for elemento in lista:
        if elemento == '':
            diccionario[elemento] = np.nan
        else:
            diccionario[elemento] = conteo
            conteo += 1

    dataframe[lista_columnas[1]] = dataframe[lista_columnas[0]].map(diccionario).astype("Int64")
    return dataframe

# Creamos una función que realiza las mismas funciones que el describe, pero con más estadísticos, solo para elementos numéricos
def estadisticos_numericas_df(dataframe, lista_columnas):
    valores_curtosis = []
    valores_asimetria = []
    valores_moda = []
    #creamos un bucle for para calcular los valores de la curtosis y la asimetría
    for columna in lista_columnas:
        if dataframe[columna].dtype == int or dataframe[columna].dtype == float:

            curtosis = round(dataframe[columna].kurtosis(), 2)
            asimetria = round(dataframe[columna].skew(),2)
            moda = dataframe[columna].mode()

            valores_curtosis.append(curtosis)
            valores_asimetria.append(asimetria)
            valores_moda.append(float(moda.iloc[0]))
            
        elif is_datetime(dataframe[columna]):
            valores_curtosis.append(np.nan)
            valores_asimetria.append(np.nan)
            valores_moda.append(float(moda.iloc[0]))
            
    estadísticos_generales = round(dataframe.describe().T, 2)
    estadísticos_generales["Curtosis"] = valores_curtosis
    estadísticos_generales["Coef_asimetria"] = valores_asimetria
    estadísticos_generales["Moda"] = valores_moda

    return estadísticos_generales