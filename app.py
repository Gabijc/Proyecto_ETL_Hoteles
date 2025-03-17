import streamlit as st  # type: ignore
import pandas as pd 
import plotly.express as px   # type: ignore
from src.soporte_carga import conexion_BBDD
from src.soporte_informe import recaudacion_anual, n_hoteles, n_reservas, valoracion_media, ticket_medio, reservas_medias, ingresos_medios_hotel, n_clientes, n_clientes_recurrentes


conn = conexion_BBDD("BBDD_Hoteles")


# Ingresos totales
rec_mdo = recaudacion_anual(conn, "reservas")
rec_total_grupo = recaudacion_anual(conn, "Vista_hoteles_grupo")
rec_total_comp = recaudacion_anual(conn, "Vista_hoteles_competencia")


# Reservas totales 
reservas_mdo = n_reservas(conn, "reservas")
reservas_tot_grupo = n_reservas(conn, "Vista_hoteles_grupo")
reservas_tot_comp = n_reservas(conn, "Vista_hoteles_competencia")

# Valoraciones medias

v_media_mdo = valoracion_media(conn, "hoteles")
v_media_grupo = valoracion_media(conn, "Vista_hoteles_grupo")
v_media_comp = valoracion_media(conn, "Vista_hoteles_competencia")

# Numero de hoteles
n_hoteles_mdo = n_hoteles(conn, "hoteles")
n_hoteles_grupo = n_hoteles(conn, "Vista_hoteles_grupo")
n_hoteles_comp = n_hoteles(conn, "Vista_hoteles_competencia")

# Ticket medio
ticket_medio_mdo = ticket_medio(rec_mdo,reservas_mdo)
ticket_medio_grupo = ticket_medio(rec_total_grupo, reservas_tot_grupo)
ticket_medio_comp = ticket_medio(rec_total_comp, reservas_tot_comp)


# Valores medios
ing_medio_por_hotel = ingresos_medios_hotel(rec_mdo, n_hoteles_mdo)
reservas_medias_mdo = reservas_medias(reservas_mdo,n_hoteles_mdo)


# Kpis dahsboard clientes
numero_clientes = n_clientes(conn, "clientes")
gasto_medio_cliente = rec_mdo/numero_clientes
reserva_media_cliente = reservas_mdo/numero_clientes
clientes_recurrentes = n_clientes_recurrentes(conn, "reservas")
tasa_repeticion = clientes_recurrentes/numero_clientes


st.set_page_config(page_title = "Dashboard",
                   layout = "centered") # ponemos el titulo de la pestaña de la web

# creamos una nagevación lateral, a la cual tenemos que poner una serie de paginas. me generará un sidebar a la izquierda que me permetirña navegar oir diferentes páginas
st.sidebar.title("Navegación")
page = st.sidebar.radio(label = "Selecciona una página",
                        options = ["Análisis general", "Análisis de hoteles del grupo", "Análisis de hoteles de la competencia", "Análisis de clientes"])

if page == "Análisis general":
    st.title("Análisis general") # establecemos el titulo de la pagina
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Nº Hoteles", f"{n_hoteles_mdo:,.2f}", border = True)
    col2.metric("Valoracion media", f"{v_media_mdo:,.2f}", border = True)
    col3.metric("Ingreso medio por hotel", f"{ing_medio_por_hotel:,.2f}", border = True)
    col4.metric("Reservas medias por hotel", f"{reservas_medias_mdo:,.2f}", border = True)
    col5.metric("Ticket medio", f"{ticket_medio_mdo:,.2f}", border = True)

elif page == "Análisis de hoteles del grupo":

    st.title("Análisis de hoteles del grupo") # establecemos el titulo de la pagina
    with st.container():
        col1, col2, col3, col4, col5 = st.columns(5) # esto me dividirá la página en 4 columnas
        col1.metric("Nº Hoteles", f"{n_hoteles_grupo:,.2f}", border = True)
        col2.metric("Ingresos totales", f"{rec_total_grupo:,.2f}", border = True)
        col3.metric("Reservas totales", f"{reservas_tot_grupo:,.2f}", border = True)
        col4.metric("Valoracion media", f"{v_media_grupo:,.2f}", border = True)
        col5.metric("Ticket medio", f"{ticket_medio_grupo:,.2f}", border = True)

elif page == "Análisis de hoteles de la competencia":

    st.title("Análisis de hoteles del grupo") # establecemos el titulo de la pagina
    col1, col2, col3, col4, col5 = st.columns(5) # esto me dividirá la página en 4 columnas
    col1.metric("Nº Hoteles", f"{n_hoteles_comp:,.2f}", border = True)
    col2.metric("Ingresos totales", f"{rec_total_comp:,.2f}", border = True)
    col3.metric("Valoracion media", f"{v_media_comp:,.2f}", border = True)
    col4.metric("Reservas totales", f"{reservas_tot_comp:,.2f}", border = True)
    col5.metric("Ticket medio", f"{ticket_medio_comp:,.2f}", border = True)

elif page == "Análisis de clientes":
    
    st.title("Análisis de clientes") # establecemos el titulo de la pagina
    col1, col2, col3, col4 = st.columns(4) # esto me dividirá la página en 4 columnas
    col1.metric("Clientes totales", f"{numero_clientes:,.2f}", border = True)
    col2.metric("Gasto medio por cliente", f"{gasto_medio_cliente:,.2f}", border = True)
    col3.metric("Reservas medias por cliente", f"{reserva_media_cliente:,.2f}", border = True)
    col4.metric("Tasa de repetición", f"{tasa_repeticion:,.2f}", border = True)
