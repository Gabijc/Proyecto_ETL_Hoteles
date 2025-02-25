import pandas as pd
from src.soporte_limpieza import limpieza_inicial
from src.soporte_extraccion import scrapeo_competencia, eventos_api
from src.soporte_carga import conexion_BBDD, carga_BBDD
from src.soporte_informe import big_numbers, analisis_hoteles
import os 
from dotenv import load_dotenv

load_dotenv()
url_api = os.getenv("url_api")
url_scrapeo = os.getenv("url_scrapeo")
archivo_raw = os.getenv("archivo_raw")

url_scrapeo_competencia = url_scrapeo
enp = url_api
df_raw = pd.read_parquet(archivo_raw, engine='auto')
query_ciudad_madrid = "SELECT nombre_ciudad, id_ciudad FROM ciudad"
query_hoteles_carga = "SELECT nombre_hotel, id_hotel FROM hoteles"
query_clientes_carga = "SELECT nombre, id_cliente FROM clientes"
 

def ETL_hoteles(endpoint, url_scrapeo, dataframe):

    dataframe_eventos = eventos_api(endpoint)
    dataframe_scrapeo = scrapeo_competencia(url_scrapeo)
    dataframe_final = limpieza_inicial(dataframe, dataframe_scrapeo)
    conn = conexion_BBDD("BBDD_Hoteles")
    carga_BBDD(conn, dataframe_eventos, dataframe_final, query_ciudad_madrid, query_clientes_carga, query_hoteles_carga)
    big_numbers(conn)
    analisis_hoteles(conn)



if __name__ == "__main__":
    ETL_hoteles(enp, url_scrapeo_competencia, df_raw)