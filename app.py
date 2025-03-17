import streamlit as st  # type: ignore
import pandas as pd 
import plotly.express as px   # type: ignore
from src.soporte_carga import conexion_BBDD
from src.soporte_informe import recaudacion_anual, n_hoteles, n_reservas, valoracion_media, ticket_medio, reservas_medias, ingresos_medios_hotel, n_clientes, recurrencia_clientes, cuota_clientes, cuota_mercado, info_hoteles, info_temporales


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
clientes_recurrentes = recurrencia_clientes(conn, "reservas")
clientes_no_recurrentes = recurrencia_clientes(conn, "reservas", "clientes no recurrentes")
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

    cuota_mercado_gr = cuota_mercado(conn, "hoteles")

    fig = px.pie(cuota_mercado_gr, # dataframe que contiene los datos
                values='Cuota de mercado', # columna con los valores para determinar la posicion en el grafico
                names="Competencia", # categorías de los datos
                title="Cuota mercado") # titulo del grafico 
    st.plotly_chart(fig, use_container_width = True) # mostramos el gráfico
 
    #if st.button == "Ingresos por hotel":
    ingresos_hotel_mdo = info_hoteles(conn)

    fig1 = px.bar(ingresos_hotel_mdo, 
                        x = "Ingresos",
                        y = "Hotel",
                        title = "Ingresos por hotel",
                        orientation = "h")
    st.plotly_chart(fig1, use_container_width = True) # método para que me muestre el gráfico

    #if st.button == "Reservas por hotel":
    fig2 = px.bar(ingresos_hotel_mdo, 
                        x = "Nº reservas",
                        y = "Hotel",
                        title = "Reservas por hotel",
                        orientation = "h")
    st.plotly_chart(fig2, use_container_width = True) # método para que me muestre el gráfico

    #if st.button == "Valoración por hotel":
    fig3 = px.bar(ingresos_hotel_mdo, 
                        x = "Valoracion media",
                        y = "Hotel",
                        title = "Valoración media por hotel",
                        orientation = "h")
    st.plotly_chart(fig3, use_container_width = True) # método para que me muestre el gráfico

    analisis_temporal_mdo = info_temporales(conn)
    fig4 = px.line(analisis_temporal_mdo, 
                      x = "fecha_reserva",
                      y = "Ingresos",
                      title = "Evolución temporal de ingresos en el mercado")
    st.plotly_chart(fig4, use_container_width = True) # método para que me muestre el gráfico

    fig5 = px.line(analisis_temporal_mdo, 
                      x = "fecha_reserva",
                      y = "Nº reservas",
                      title = "Evolución temporal de reservas en el mercado")
    st.plotly_chart(fig5, use_container_width = True) # método para que me muestre el gráfico

elif page == "Análisis de hoteles del grupo":

    st.title("Análisis de hoteles del grupo") # establecemos el titulo de la pagina
    with st.container():
        col1, col2, col3, col4, col5 = st.columns(5) # esto me dividirá la página en 4 columnas
        col1.metric("Nº Hoteles", f"{n_hoteles_grupo:,.2f}", border = True)
        col2.metric("Ingresos totales", f"{rec_total_grupo:,.2f}", border = True)
        col3.metric("Reservas totales", f"{reservas_tot_grupo:,.2f}", border = True)
        col4.metric("Valoracion media", f"{v_media_grupo:,.2f}", border = True)
        col5.metric("Ticket medio", f"{ticket_medio_grupo:,.2f}", border = True)

    ingresos_hoteles_grupo = info_hoteles(conn, "grupo")

    fig1 = px.bar(ingresos_hoteles_grupo, 
                        x = "Hotel",
                        y = "Ingresos",
                        title = "Ingresos por hotel")
    st.plotly_chart(fig1, use_container_width = True) # método para que me muestre el gráfico

    fig2 = px.bar(ingresos_hoteles_grupo, 
                        x = "Hotel",
                        y = "Nº reservas",
                        title = "Reservas por hotel")
    st.plotly_chart(fig2, use_container_width = True) # método para que me muestre el gráfico

    fig3 = px.bar(ingresos_hoteles_grupo, 
                        x = "Hotel",
                        y = "Valoracion media",
                        title = "Valoración media por hotel")
    st.plotly_chart(fig3, use_container_width = True) # método para que me muestre el gráfico

    analisis_temporal_grupo = info_temporales(conn, "grupo")
    fig4 = px.line(analisis_temporal_grupo, 
                      x = "fecha_reserva",
                      y = "Ingresos",
                      title = "Evolución temporal de ingresos del grupo")
    st.plotly_chart(fig4, use_container_width = True) # método para que me muestre el gráfico

    fig5 = px.line(analisis_temporal_grupo, 
                      x = "fecha_reserva",
                      y = "Nº reservas",
                      title = "Evolución temporal de reservas del grupo")
    st.plotly_chart(fig5, use_container_width = True) # método para que me muestre el gráfico

elif page == "Análisis de hoteles de la competencia":

    st.title("Análisis de hoteles de la competencia") # establecemos el titulo de la pagina
    col1, col2, col3, col4, col5 = st.columns(5) # esto me dividirá la página en 4 columnas
    col1.metric("Nº Hoteles", f"{n_hoteles_comp:,.2f}", border = True)
    col2.metric("Ingresos totales", f"{rec_total_comp:,.2f}", border = True)
    col3.metric("Valoracion media", f"{v_media_comp:,.2f}", border = True)
    col4.metric("Reservas totales", f"{reservas_tot_comp:,.2f}", border = True)
    col5.metric("Ticket medio", f"{ticket_medio_comp:,.2f}", border = True)
    
    ingresos_hoteles_competencia = info_hoteles(conn, "competencia")

    fig1 = px.bar(ingresos_hoteles_competencia, 
                        x = "Hotel",
                        y = "Ingresos",
                        title = "Ingresos por hotel")
    st.plotly_chart(fig1, use_container_width = True) # método para que me muestre el gráfico

    fig2 = px.bar(ingresos_hoteles_competencia, 
                        x = "Hotel",
                        y = "Nº reservas",
                        title = "Reservas por hotel")
    st.plotly_chart(fig2, use_container_width = True) # método para que me muestre el gráfico

    fig3 = px.bar(ingresos_hoteles_competencia, 
                        x = "Hotel",
                        y = "Valoracion media",
                        title = "Valoración media por hotel")
    st.plotly_chart(fig3, use_container_width = True) # método para que me muestre el gráfico

elif page == "Análisis de clientes":
    
    st.title("Análisis de clientes") # establecemos el titulo de la pagina
    col1, col2, col3, col4 = st.columns(4) # esto me dividirá la página en 4 columnas
    col1.metric("Clientes totales", f"{numero_clientes:,.2f}", border = True)
    col2.metric("Gasto medio por cliente", f"{gasto_medio_cliente:,.2f}", border = True)
    col3.metric("Reservas medias por cliente", f"{reserva_media_cliente:,.2f}", border = True)
    col4.metric("Tasa de repetición", f"{tasa_repeticion:,.2f}", border = True)

    cuota_clientes_mdo = cuota_clientes(conn, "reservas", "hoteles")
    fig = px.pie(cuota_clientes_mdo, # dataframe que contiene los datos
                values='Cuota clientes', # columna con los valores para determinar la posicion en el grafico
                names="Competencia", # categorías de los datos
                title="Cuota de clientes") # titulo del grafico 
    st.plotly_chart(fig, use_container_width = True) # mostramos el gráfico

    
    clientes = [] 
    clientes.append({"Clientes recurrentes": clientes_recurrentes,
                        "Clientes no recurrentes":clientes_no_recurrentes})
    df_clientes_recurrencia = pd.DataFrame(clientes).T.reset_index()
    df_clientes_recurrencia = df_clientes_recurrencia.rename(columns = {"index": "Values",0: "Nº_clientes"})
    df_clientes_recurrencia["Recurrencia"] = round((df_clientes_recurrencia['Nº_clientes']/df_clientes_recurrencia['Nº_clientes'].sum())*100, 2)
    
    fig = px.pie(df_clientes_recurrencia, # dataframe que contiene los datos
                values='Recurrencia', # columna con los valores para determinar la posicion en el grafico
                names="Values", # categorías de los datos
                title="Recurrencia de clientes") # titulo del grafico 
    st.plotly_chart(fig, use_container_width = True) # mostramos el gráfico