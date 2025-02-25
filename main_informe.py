# Importamos las librerías necesarias
import pandas as pd
import numpy as np
import psycopg2 as ps
from src.soporte_carga import conexion_BBDD
import os
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    conn = conexion_BBDD("BBDD_Hoteles")

