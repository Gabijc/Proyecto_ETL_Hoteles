# Importamos las librerías necesarias
import pandas as pd
import numpy as np
import psycopg2 as ps
import os
from dotenv import load_dotenv

load_dotenv()
usuario_BBDD = os.getenv("usuario_BBDD")
contraseña_BBDD = os.getenv("contraseña_BBDD")
host_BBDD = os.getenv("host_BBDD")
port_BBDD = os.getenv("port_BBDD")


def conexion_BBDD(nombre_BBDD , usuario = usuario_BBDD, contraseña = contraseña_BBDD, anfitrion = host_BBDD, puerto = port_BBDD):

    conn = ps.connect(
                    dbname = nombre_BBDD, 
                    user = usuario,
                    password = contraseña,
                    host = anfitrion,
                    port = puerto)

    return conn

# Carga tabla ciudad
def carga_tabla_ciudad(conn, ciudad = "Madrid"):
    
    cur = conn.cursor()

    data_to_insert = [ciudad]
    insert_query = """ 
                        INSERT INTO ciudad (nombre_ciudad)
                        VALUES (%s) 
                    """
    cur.execute(insert_query, data_to_insert)
    conn.commit()


# Carga tabla eventos
# la query será tal que así: "SELECT nombre_ciudad, id_ciudad FROM ciudad"
def carga_tabla_eventos(dataframe, query_ciudad, conn):

    cur = conn.cursor()
    
    cur.execute(query_ciudad)
    dictio = dict(cur.fetchall())

    data_to_insert = []


    for i, row in dataframe.iterrows():
        nombre_evento = row["nombre_evento"]
        url_evento = row["url_evento"]
        codigo_postal = row["codigo_postal"] if row["codigo_postal"] != 0 else None # en este caso los valores que son igual a 0 se corresponden con valores nulos, por lo que le indicamos que si el valor es igual a 0 nos ponga un nulo
        direccion = row["direccion"] if pd.notna(row["direccion"]) else None # tenemos valores nulos en esta columna, de manera que le indicamos, que si el elemento no es nulo nos lo coja, y si es nulo, nos incluya un None, ya que sql no acepta valores nulos que no sean None
        horario = row["horario"] if pd.notna(row["horario"]) else None
        fecha_inicio = row["fecha_inicio"]
        fecha_fin = row["fecha_fin"]
        organizacion = row["organizacion"] if pd.notna(row["organizacion"]) else None
        id_ciudad = dictio.get("Madrid")

        data_to_insert.append((nombre_evento, url_evento, codigo_postal, direccion, horario, fecha_inicio, fecha_fin, organizacion, id_ciudad))
        
    insert_query = """ 
                    INSERT INTO eventos (nombre_evento, url_evento, codigo_postal, direccion, horario,
                    fecha_inicio, fecha_fin,organizacion, id_ciudad)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
    cur.executemany(insert_query, data_to_insert)
    conn.commit()


# Carga tabla hoteles
# la query será tal que así: "SELECT nombre_ciudad, id_ciudad FROM ciudad"
def carga_tabla_hoteles(dataframe, query_ciudad, conn):

    cur = conn.cursor()

    data_to_insert = []

    cur.execute(query_ciudad)
    dictio = dict(cur.fetchall())

    for _, row in dataframe.iterrows():
        id_hotel = row["id_hotel"]
        nombre_hotel = row["nombre_hotel"] 
        competencia = row["competencia"] 
        valoracion = row["estrellas"] 
        id_ciudad = dictio.get("Madrid") 

        tupla = (id_hotel, nombre_hotel, competencia, valoracion, id_ciudad)

        if tupla not in data_to_insert:
            data_to_insert.append(tupla)
    
    insert_query = """ 
                        INSERT INTO hoteles (id_hotel, nombre_hotel, competencia, valoracion, id_ciudad)
                        VALUES (%s, %s, %s, %s, %s)
            """
    cur.executemany(insert_query, data_to_insert)
    conn.commit()

# Carga tabla clientes
def carga_tabla_clientes(dataframe, conn):

    cur = conn.cursor()

    data_to_insert = []

    for _, row in dataframe.iterrows():

        id_cliente = row["id_cliente"]
        nombre = row["nombre"],
        apellido = row["apellido"],
        mail = row["mail"]

        tupla = (id_cliente, nombre, apellido, mail)

        if tupla not in data_to_insert:
            data_to_insert.append(tupla)
    
    insert_query = """ 
                        INSERT INTO clientes (id_cliente, nombre, apellido, mail)
                        VALUES (%s, %s, %s, %s)
                        """
    cur.executemany(insert_query, data_to_insert)
    conn.commit()

# Carga tabla reservas
# La query de clientes será así: "SELECT nombre, id_cliente FROM clientes"
# la query de hoteles será así: "SELECT nombre_hotel, id_hotel FROM hoteles"
def carga_tabla_reservas(dataframe, query_clientes, query_hoteles, conn):

    cur = conn.cursor()
    
    cur.execute(query_clientes)
    dictio_clientes = dict(cur.fetchall())

    cur.execute(query_hoteles)
    dictio_hoteles = dict(cur.fetchall())

    data_to_insert = []

    for _, row in dataframe.iterrows():
        id_reserva = row["id_reserva"]
        fecha_reserva = row["fecha_reserva"]
        inicio_estancia = row["inicio_estancia"]
        final_estancia = row["final_estancia"]
        precio_noche = row["precio_noche"]
        id_cliente = dictio_clientes.get(row["nombre"])
        id_hotel = dictio_hoteles.get(row["nombre_hotel"])

        data_to_insert.append((id_reserva, fecha_reserva, inicio_estancia, final_estancia, precio_noche, id_cliente, id_hotel))
    
    insert_query = """ 
                        INSERT INTO reservas (id_reserva, fecha_reserva, inicio_estancia, final_estancia, precio_noche, id_cliente, id_hotel)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """
    
    cur.executemany(insert_query, data_to_insert)
    conn.commit()