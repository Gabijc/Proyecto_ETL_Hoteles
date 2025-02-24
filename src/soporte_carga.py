# Importamos las librerías necesarias
import pandas as pd
import numpy as np
import psycopg2 as ps

def conexion_BBDD(nombre_BBDD , usuario = "postgres", contraseña = "admin", anfitrion = "localhost", puerto = "5432"):

    conn = ps.connect(
    dbname = nombre_BBDD, 
    user = usuario,
    password = contraseña,
    host = anfitrion,
    port = puerto)

    cur = conn.cursor()
    
    cur.execute("SELECT version();")
    conexion = cur.fetchone()
    print(conexion)