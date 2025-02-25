import pandas as pd
import numpy as np
from IPython.display import Markdown, display
import seaborn as sns
import matplotlib.pyplot as plt
import time


def creacion_vista(conn, nombre_vista, com_gr):

    cur = conn.cursor()

    query = f""" 
        CREATE VIEW "{nombre_vista}" AS
        SELECT 
            h.id_hotel ,
            h.nombre_hotel,
            h.valoracion,
            r.id_reserva,
            r.fecha_reserva,
            r.precio_noche,
            c.id_cliente,
            concat(c."nombre", ' ', c."apellido")
        FROM hoteles as h
            INNER JOIN  reservas AS r ON h.id_hotel = r.id_hotel
            INNER JOIN  clientes AS c ON r.id_cliente = c.id_cliente
        WHERE h.competencia = {com_gr}; 
        """

    cur.execute(query)
    conn.commit()

    return f"Vista_creada_correctamente"

# Recaudacion total anual
def recaudacion_anual(conn, vista):

    cur = conn.cursor()

    query_rec_grupo = f""" 
                SELECT 
                    SUM(precio_noche)
                FROM "{vista}"; 
        """

    cur.execute(query_rec_grupo)
    rec_total = cur.fetchall()
    return round(rec_total[0][0], 2)

# Precio medio noche
def precio_medio(conn, vista):

    cur = conn.cursor()

    query_p_medio = f""" 
            SELECT AVG(precio_noche)
            FROM "{vista}"; 
    """

    cur.execute(query_p_medio)
    p_medio = cur.fetchall()
    return round(p_medio[0][0], 2)

# Nº de reservas totales
def n_reservas(conn, vista):
    cur = conn.cursor()

    query_n_reservas = f""" 
            SELECT count(id_reserva)
            FROM "{vista}"; 
    """

    cur.execute(query_n_reservas)
    reservas_tot = cur.fetchall()
    return reservas_tot[0][0]

# Valoracion media
def valoracion_media(conn, vista):
    cur = conn.cursor()

    query_v_media = f""" 
            SELECT AVG(valoracion)
            FROM "{vista}"; 
    """

    cur.execute(query_v_media)
    v_media = cur.fetchall()
    return round(v_media[0][0], 2)


def grafico_hoteles(conn, vista, titulo_recaudacion, titulo_reservas):
    cur = conn.cursor()
    # Vamos a analizar los ingresos por hotel, y el numero de reservas por hotel
    query = f""" 
        SELECT 
                nombre_hotel,
                sum(precio_noche),
                count(id_reserva)
        FROM "{vista}"
        GROUP BY nombre_hotel
        ORDER BY 2 DESC; 
"""

    cur.execute(query)
    q = cur.fetchall()
    dataframe = pd.DataFrame(q)

    fig, axes = plt.subplots(nrows = 1, ncols = 2, figsize = (20, 5))

    sns.barplot(x = 0, 
                y = 1,
                data = dataframe,
                ax = axes[0])
    sns.barplot(x = 0, 
                y = 2,
                data = dataframe, 
                ax = axes[1])

    axes[0].set_title(titulo_recaudacion, fontsize = 10)
    axes[0].set_xlabel("Nombre_hotel", fontsize = 10)
    axes[0].set_ylabel("Recaudacion", fontsize = 10)
    axes[0].spines['right'].set_visible(False)
    axes[0].spines['top'].set_visible(False)
    axes[0].set_xticklabels(labels = dataframe[0], rotation=45, ha='right')


    axes[1].set_title(titulo_reservas, fontsize = 10)
    axes[1].set_ylabel("Nº_reservas", fontsize = 10)
    axes[1].set_xlabel("Nombre_hotel", fontsize = 10)
    axes[1].spines['right'].set_visible(False)
    axes[1].spines['top'].set_visible(False)
    axes[1].set_xticklabels(labels = dataframe[0], rotation=45, ha='right')

    plt.show()
    plt.close(fig)


def big_numbers(conn):
    try:

        creacion_vista(conn, "Vista_hoteles_grupo", False)
        creacion_vista(conn, "Vista_hoteles_competencia", True)

        rec_total = recaudacion_anual(conn, "Vista_hoteles_grupo")
        rec_total_c = recaudacion_anual(conn, "Vista_hoteles_competencia")
        p_medio = precio_medio(conn, "Vista_hoteles_grupo")
        p_medio_c = precio_medio(conn, "Vista_hoteles_competencia")
        reservas_tot = n_reservas(conn, "Vista_hoteles_grupo")
        reservas_tot_c = n_reservas(conn, "Vista_hoteles_competencia")
        v_media = valoracion_media(conn, "Vista_hoteles_grupo")
        v_media_c = valoracion_media(conn, "Vista_hoteles_competencia")

        tabla_bn = f"""
        | Métrica            | Hoteles_Grupo | Hoteles_Competencia |
        |--------------------|--------------|---------------------|
        | Recaudación Total |{rec_total}|  {rec_total_c} |
        | Precio Medio      |{p_medio}  |{p_medio_c} |
        | Reservas Totales  |{reservas_tot}       |{reservas_tot_c} |
        | Valoración Media  |{v_media}  | {v_media_c} |
        """
        print(tabla_bn)

    except Exception as e:
        print(f"Error: {e}")

def analisis_hoteles(conn):
    grafico_hoteles(conn, "Vista_hoteles_grupo", "Recaudacion por hotel del grupo", "Numero de reservas por hotel del grupo")
    time.sleep(5)
    grafico_hoteles(conn, "Vista_hoteles_competencia", "Recaudacion por hotel de la competencia", "Numero de reservas por hotel de la competencia")