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

# Función para modificar el tipo de dato de las columnas que le pasemos a tipo fecha
def data_fechas(dataframe, columnas):
    """
    Convierte las columnas especificadas de un DataFrame al tipo de dato datetime.

    Args:
        dataframe (pd.DataFrame): El DataFrame que contiene las columnas a modificar.
        columnas (list): Lista de nombres de las columnas a convertir a tipo datetime.

    Returns:
        pd.DataFrame: El DataFrame con las columnas modificadas al tipo datetime.
    """
    for col in columnas:
        dataframe[col] = pd.to_datetime(dataframe[col])
    return dataframe

# Creamos una función que nos permite realizar el cambio del id creando uno nuevo que será seriado
def cambio_id(dataframe, lista_columnas, nombre_columna_nueva):
    """
    Crea una nueva columna con un identificador seriado basado en valores únicos de otra columna.

    Args:
        dataframe (pd.DataFrame): El DataFrame que contiene la columna original.
        lista_columnas (list): Lista con el nombre de la columna sobre la cual se generará el nuevo ID.
        nombre_columna_nueva (str): Nombre de la nueva columna que contendrá los IDs serializados.

    Returns:
        pd.DataFrame: El DataFrame con la nueva columna de identificadores serializados.
    """
    
    lista = dataframe[lista_columnas[0]].unique()
    diccionario = {}
    conteo = 1
    for elemento in lista:
        
        diccionario[elemento] = conteo
        conteo += 1

    dataframe[nombre_columna_nueva] = dataframe[lista_columnas[0]].map(diccionario).astype(str)
    return dataframe
