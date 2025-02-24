# Importamos las librerías necesarias
import pandas as pd
import numpy as np
import psycopg2 as ps
from src.soporte_carga import conexion_BBDD

if __name__ == "__main__":
    conexion_BBDD("BBDD_Hoteles")