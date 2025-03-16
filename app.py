import streamlit as st  # type: ignore
import pandas as pd 
import plotly.express as px   # type: ignore
from src.soporte_carga import conexion_BBDD
from src.soporte_informe import recaudacion_anual, precio_medio, n_reservas, valoracion_media


conn = conexion_BBDD("BBDD_Hoteles")

rec_total = recaudacion_anual(conn, "Vista_hoteles_grupo")
rec_total_c = recaudacion_anual(conn, "Vista_hoteles_competencia")
p_medio = precio_medio(conn, "Vista_hoteles_grupo")
p_medio_c = precio_medio(conn, "Vista_hoteles_competencia")
reservas_tot = n_reservas(conn, "Vista_hoteles_grupo")
reservas_tot_c = n_reservas(conn, "Vista_hoteles_competencia")
v_media = valoracion_media(conn, "Vista_hoteles_grupo")
v_media_c = valoracion_media(conn, "Vista_hoteles_competencia")


st.set_page_config(page_title = "Dashboard",
                   layout = "centered") # ponemos el titulo de la pestaña de la web

# creamos una nagevación lateral, a la cual tenemos que poner una serie de paginas. me generará un sidebar a la izquierda que me permetirña navegar oir diferentes páginas
st.sidebar.title("Navegación")
page = st.sidebar.radio(label = "Selecciona una página",
                        options = ["Análisis general", "Análisis de hoteles del grupo", "Análisis de hoteles de la competencia", "Análisis de clientes"])

if page == "Análisis de hoteles del grupo":

    st.title("Análisis de hoteles del grupo") # establecemos el titulo de la pagina
    #col1, col2 = st.columns(2) # esto me dividirá la página en dos columnas
    

    #col1.metric("Recaudacion total", f"{rec_total:.2f} €") #v ponemos el kpi
    #col2.metric("Precio medio", f"{p_medio:.2f}€")
    tab1, tab2 = st.tabs(["Tab 1", "Tab2"])
    tab1.write("this is tab 1")
    tab2.write("this is tab 2")