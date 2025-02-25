# Importamos las librerías necesarias
import pandas as pd
import numpy as np
import psycopg2 as ps
from src.soporte_carga import conexion_BBDD, carga_tabla_ciudad, carga_tabla_clientes, carga_tabla_eventos, carga_tabla_hoteles, carga_tabla_reservas


if __name__ == "__main__":
    conexion_BBDD("BBDD_Hoteles")
    carga_tabla_ciudad()
    carga_tabla_eventos()
    carga_tabla_hoteles()
    carga_tabla_clientes()
    carga_tabla_reservas()
