import pandas as pd
import numpy as np
from src.soporte_limpieza import info_df, data_fechas, cambio_id


df_raw = pd.read_parquet("../data/reservas_hoteles.parquet", engine='auto')
hoteles_competencia_scrapeado = pd.read_csv("../data/hoteles_competencia.csv")

def limpieza_inicial(dataframe_limpieza, dataframe_scrapeo):
    
    data = dataframe_limpieza.copy() # creamos una copia del dataframe recibido sobre el cual vamos a trabajar

    data = data.drop_duplicates() # eliminamos los duplicados iguales en el dataframe
    if data.duplicated().sum() == 0: # comprobamos que se han eliminado correctamente
        print("Duplicados iguales eliminados")

    print(f"La estructura inicial del dataframe es: \n {info_df(data)}") # Revisamos la información general del dataframe
    
    data = data_fechas(data, ["fecha_reserva", "inicio_estancia", "final_estancia"]) # modificamos las columnas que queremos a tipo fecha llamando a la funcon de modificacion de fechas
    
    data["inicio_estancia"] = data["inicio_estancia"].fillna("2025-03-01") # Realizamos la modificación de los valores nulos de las columnas reemplazándolas por los valores de las fechas del fin de semana correspondientes
    data["final_estancia"] = data["final_estancia"].fillna("2025-03-02")


    grupo = data[data["competencia"] == False] # Creamos un dataframe para los hoteles del grupo 
    competencia =  data[data["competencia"] == True] # Creamos un dataframe para los hoteles de la competencia

    # Calculamos los precios medios de los hoteles del grupo

    precios_grupo = grupo[["nombre_hotel", "precio_noche"]] # creamos un dataframe solo con los hoteles y el precio correspondiente de cada uno 
    estadisticos_precio = precios_grupo.groupby("nombre_hotel")["precio_noche"].describe() # calculamos los estadíticos de los precios por hotel para revisar con que calcular el precio medio. Es como pasarle una lista de funciones de agregacion con el agg al groupby
    estadisticos_precio = estadisticos_precio.reset_index() # creamos un dataframe a partir de los estadistcios
    precios_medios_grupo = estadisticos_precio[["nombre_hotel", "mean"]] # nos quedamos solo con los precios medios

    # Calulamos las estrellas medias por hotel

    estrellas_grupo = grupo[["nombre_hotel", "estrellas"]]
    estadisticos_estrellas = estrellas_grupo.groupby("nombre_hotel")["estrellas"].describe() # calculamos los estadíticos de las estrellas por hotel para revisar con que calcular la valoracion media. Es como pasarle una lista de funciones de agregacion con el agg al groupby
    estadisticos_estrellas = estadisticos_estrellas.reset_index()
    estrellas_medias_grupo = estadisticos_estrellas[["nombre_hotel", "mean"]]
    estrellas_medias_grupo["mean"] = pd.Series([round(val, 2) for val in estrellas_medias_grupo["mean"]]) # redoneamos los valores a 2 decimales

    grupo_con_precio = grupo.merge(precios_medios_grupo, on = "nombre_hotel") #unimos el df de grupo con el de precios
    grupo_final = grupo_con_precio.merge(estrellas_medias_grupo, on = "nombre_hotel") #unimos el df de grupo con el de estrellas
    grupo_final = grupo_final.drop(columns = ["precio_noche", "estrellas"]) # eliminamos las columnas con los precios y las estrellas incorrectos
    grupo_final = grupo_final.rename(columns = {'mean_x': 'precio_noche', 'mean_y': 'estrellas'}) # renombramos las columnas de medias a los precios y las estrellas medias
    
    competencia_scrapeado = dataframe_scrapeo # nos traemos la información scrapeada
    competencia_scrapeado["id_hotel"] = competencia["id_hotel"].unique() # Asignamos un id de competencia a los hoteles scrapeados

    competencia_final = competencia.merge(competencia_scrapeado, on = "id_hotel") # Unimos los datos scrapeados con los de la competencia original
    competencia_final = competencia_final.drop(columns = ["fecha_reserva_x", "precio_noche", "nombre_hotel_x", "estrellas_x"]) # eliminamos las columns con la información antigua y erronea 
    competencia_final["ciudad"] = "Madrid" # rellenamos la columna de ciudad con Madrid, ya que todos los hoteles son de Madrid
    competencia_final = competencia_final.rename(columns = {'fecha_reserva_y': 'fecha_reserva', 'nombre_hotel_y': 'nombre_hotel', 'estrellas_y': 'estrellas','precio': 'precio_noche'}) # renombramos las columnas con los nombres correctos
    competencia_final = competencia_final.reindex(['id_reserva', 'id_cliente', 'nombre', 'apellido', 'mail', 'competencia',
       'fecha_reserva', 'inicio_estancia', 'final_estancia', 'id_hotel',
       'nombre_hotel', 'estrellas', 'ciudad', 'precio_noche'], axis = 1) # reindexamos las columnas del dataframe para que estén en el mismo orden que el dataframe de grupo, ya que sino el concat se realizará de forma incorrecta
    
    df_final = pd.concat([grupo_final, competencia_final], axis = 0) # Concatenamos ambos dataframes uno encima de otro
    df_final["fecha_reserva"] = pd.to_datetime(df_final["fecha_reserva"]) # modificamos el tipo de dato de la columna de fecha de reserva ahora que la tenemos completa

    columnas_cliente = ["mail", "id_cliente"]
    cambio_id(df_final, columnas_cliente, "id_cliente_nuevo") # Modificamos los id de cliente para que sean únicos

    columnas_hoteles = ["nombre_hotel", "id_hotel"]
    cambio_id(df_final, columnas_hoteles, "id_hotel_nuevo") # Modificamos los id de hotel para que sean únicos

    df_final["id_hotel"] = df_final["id_hotel_nuevo"] 
    df_final["id_cliente"] = df_final["id_cliente_nuevo"]
    df_final = df_final.drop(columns = ["id_hotel_nuevo", "id_cliente_nuevo"])

    df_final["id_hotel"] = df_final["id_hotel"].astype(str) # modificamos el tipo de dato al correspondiente con el de la abse de datos
    df_final["id_cliente"] = df_final["id_cliente"].astype(str) # modificamos el tipo de dato al correspondiente con el de la abse de datos

    df_final.to_csv("../data/reservas_hoteles_limpio2.csv", index = False) # guardamos el dataframe limpio
    return print(f"La estructura final del dataframe es: \n {info_df(df_final)}") # Revisamos la información general del dataframe 


if __name__ == "__main__":
    limpieza_inicial(df_raw, hoteles_competencia_scrapeado)