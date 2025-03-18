import streamlit as st  # type: ignore
import pandas as pd 
import plotly.express as px   # type: ignore
from src.soporte_carga import conexion_BBDD
from src.soporte_informe import recaudacion_anual, n_hoteles, n_reservas, valoracion_media, ticket_medio, reservas_medias, ingresos_medios_hotel, n_clientes, recurrencia_clientes, cuota_clientes, cuota_mercado, info_hoteles, info_temporales, info_clientes


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

st.set_page_config(page_title = "Dashboard_Hoteles",
                    page_icon="🏨",
                    layout="wide",
                    initial_sidebar_state="collapsed",
                    menu_items={ 'Get Help': "https://github.com/Gabijc/Proyecto_ETL_Hoteles"}) 

def set_bg_color(color):
    st.markdown(
        f"""
         <style>
         .stApp {{
             background-color: {color};
         }}
         </style>
         """,
        unsafe_allow_html=True
    )

# Ejemplo de uso:
#set_bg_color('#E5F6E3')  # Un verde claro

# PENDIENTE TERMINAR ESTILO APP, COLORES GRAFICOS, FONDO....

# creamos una nagevación lateral, a la cual tenemos que poner una serie de paginas. me generará un sidebar a la izquierda que me permetirña navegar oir diferentes páginas
st.sidebar.title("Navegación")
page = st.sidebar.radio(label = "Selecciona una página",
                        options = ["Análisis general", "Análisis de hoteles del grupo", "Análisis de hoteles de la competencia", "Análisis de clientes"])


if page == "Análisis general":

    elemento = st.selectbox("Elige un elemento", ["Evolución temporal de reservas", "Evolución temporal de ingresos"])
    elemento2 = st.selectbox("Elige un elemento", ["Reservas por hotel", "Ingresos por hotel", "Valoracion por hotel"])
    
    st.title("Análisis general") # establecemos el titulo de la pagina
    #st.header("Análisis general", divider="gray")
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Nº Hoteles", f"{n_hoteles_mdo:,.2f}",  border = True)
    col2.metric("Valoracion media", f"{v_media_mdo:,.2f}",  border = True)
    col3.metric("Ingreso medio por hotel", f"{ing_medio_por_hotel:,.2f}",  border = True)
    col4.metric("Reservas medias por hotel", f"{reservas_medias_mdo:,.2f}",  border = True)
    col5.metric("Ticket medio", f"{ticket_medio_mdo:,.2f}",  border = True)
    
    with st.container():
        
        col1, col2 = st.columns([1.5, 1.5])

        with col1:
            cuota_mercado_gr = cuota_mercado(conn, "hoteles")
            fig1 = px.pie(cuota_mercado_gr, # dataframe que contiene los datos
                        values='Cuota de mercado', # columna con los valores para determinar la posicion en el grafico
                        names="Competencia", # categorías de los datos
                        title="Cuota mercado") 
            fig1.update_layout(title_font_size = 24,
                               font_color = "white",
                               plot_bgcolor = "white",
                               paper_bgcolor = "white",
                               legend = dict(font = dict(color = "white", size = 20)))
            st.plotly_chart(fig1, use_container_width = True) # mostramos el gráfico
            
            analisis_temporal_mdo = info_temporales(conn)
            if elemento == "Evolución temporal de reservas":
                fig2 = px.line(analisis_temporal_mdo, 
                                x = "fecha_reserva",
                                y = "Ingresos",
                                title = "Evolución temporal de ingresos en el mercado")
                st.plotly_chart(fig2, use_container_width = True) # método para que me muestre el gráfico

            elif elemento == "Evolución temporal de ingresos":
                fig3 = px.line(analisis_temporal_mdo, 
                                x = "fecha_reserva",
                                y = "Nº reservas",
                                title = "Evolución temporal de reservas en el mercado")
                st.plotly_chart(fig3, use_container_width = True) # método para que me muestre el gráfico

        with col2:
            ingresos_hotel_mdo = info_hoteles(conn)
            if elemento2 == "Reservas por hotel":
                fig1 = px.bar(ingresos_hotel_mdo, 
                                    x = "Ingresos",
                                    y = "Hotel",
                                    title = "Ingresos por hotel",
                                    orientation = "h")
                fig1.update_layout( width=100, 
                        height=1000,
                        title_x=0.3)
                fig1.update_xaxes(title=None)
                fig1.update_yaxes(title=None)
                st.plotly_chart(fig1, use_container_width = True) # método para que me muestre el gráfico

            elif elemento2 == "Ingresos por hotel":
                fig2 = px.bar(ingresos_hotel_mdo, 
                                    x = "Nº reservas",
                                    y = "Hotel",
                                    title = "Reservas por hotel",
                                    orientation = "h")
                fig2.update_layout( width=100, 
                        height=1000,
                        title_x=0.3)
                fig2.update_xaxes(title=None)
                fig2.update_yaxes(title=None)
                st.plotly_chart(fig2, use_container_width = True) # método para que me muestre el gráfico
            elif elemento2 == "Valoracion por hotel":
                fig3 = px.bar(ingresos_hotel_mdo, 
                                    x = "Valoracion media",
                                    y = "Hotel",
                                    title = "Valoración media por hotel",
                                    orientation = "h")
                fig3.update_layout( width=800, 
                        height=800,
                        title_x=0.3)
                fig3.update_xaxes(title=None)
                fig3.update_yaxes(title=None)
                st.plotly_chart(fig3, use_container_width = True) # método para que me muestre el gráfico

elif page == "Análisis de hoteles del grupo":

    elemento_analisis = st.selectbox("Elige un elemento", ["Evolución temporal de reservas", "Evolución temporal de ingresos"])
    
    st.title("Análisis de hoteles del grupo") # establecemos el titulo de la pagina
    with st.container():
        col1, col2, col3, col4, col5 = st.columns(5) # esto me dividirá la página en 4 columnas
        col1.metric("Nº Hoteles", f"{n_hoteles_grupo:,.2f}", border = True)
        col2.metric("Ingresos totales", f"{rec_total_grupo:,.2f}", border = True)
        col3.metric("Reservas totales", f"{reservas_tot_grupo:,.2f}", border = True)
        col4.metric("Valoracion media", f"{v_media_grupo:,.2f}", border = True)
        col5.metric("Ticket medio", f"{ticket_medio_grupo:,.2f}", border = True)

    with st.container():
        col1, col2 = st.columns([1.5, 1.5])
        ingresos_hoteles_grupo = info_hoteles(conn, "grupo")

        with col1:
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

        with col2: 
            fig1 = px.bar(ingresos_hoteles_grupo, 
                                x = "Ingresos",
                                y = "Hotel",
                                title = "Ingresos por hotel", 
                                orientation= "h")
            fig1.update_layout( width=800, 
                        height=800,
                        title_x=0.3)
            fig1.update_xaxes(title=None)
            fig1.update_yaxes(title=None)
            st.plotly_chart(fig1, use_container_width = True) # método para que me muestre el gráfico

    analisis_temporal_grupo = info_temporales(conn, "grupo")
    if elemento_analisis == "Evolución temporal de reservas":
        
        fig4 = px.line(analisis_temporal_grupo, 
                        x = "fecha_reserva",
                        y = "Ingresos",
                        title = "Evolución temporal de ingresos del grupo")
        st.plotly_chart(fig4, use_container_width = True) # método para que me muestre el gráfico

    elif elemento_analisis == "Evolución temporal de ingresos":
        fig5 = px.line(analisis_temporal_grupo, 
                        x = "fecha_reserva",
                        y = "Nº reservas",
                        title = "Evolución temporal de reservas del grupo")
        st.plotly_chart(fig5, use_container_width = True) # método para que me muestre el gráfico

elif page == "Análisis de hoteles de la competencia":

    st.title("Análisis de hoteles de la competencia") # establecemos el titulo de la pagina
    with st.container():
        col1, col2, col3, col4, col5 = st.columns(5) # esto me dividirá la página en 4 columnas
        col1.metric("Nº Hoteles", f"{n_hoteles_comp:,.2f}", border = True)
        col2.metric("Ingresos totales", f"{rec_total_comp:,.2f}", border = True)
        col3.metric("Valoracion media", f"{v_media_comp:,.2f}", border = True)
        col4.metric("Reservas totales", f"{reservas_tot_comp:,.2f}", border = True)
        col5.metric("Ticket medio", f"{ticket_medio_comp:,.2f}", border = True)
    
    with st.container():

        col1, col2 = st.columns([1.5, 1.5])
        with col1:

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

        with col2:
            fig3 = px.bar(ingresos_hoteles_competencia, 
                                x = "Hotel",
                                y = "Valoracion media",
                                title = "Valoración media por hotel")
            st.plotly_chart(fig3, use_container_width = True) # método para que me muestre el gráfico

            st.write("Todas las reservas de la competencia han sido realizadas el 21 de febrero")

elif page == "Análisis de clientes":

    elemento = st.selectbox("Elige un elemento", ["Gasto por cliente", "Nº de reservas por cliente"])
    
    with st.container():
        st.title("Análisis de clientes") # establecemos el titulo de la pagina
        col1, col2, col3, col4 = st.columns(4) # esto me dividirá la página en 4 columnas
        col1.metric("Clientes totales", f"{numero_clientes:,.2f}", border = True)
        col2.metric("Gasto medio por cliente", f"{gasto_medio_cliente:,.2f}", border = True)
        col3.metric("Reservas medias por cliente", f"{reserva_media_cliente:,.2f}", border = True)
        col4.metric("Tasa de repetición", f"{tasa_repeticion:,.2f}", border = True)

    with st.container():
        col1, col2 = st.columns([1.5, 1.5])
        with col1:
            cuota_clientes_mdo = cuota_clientes(conn, "reservas", "hoteles")

            fig1 = px.pie(cuota_clientes_mdo, # dataframe que contiene los datos
                          values='Cuota clientes', # columna con los valores para determinar la posicion en el grafico
                          names="Competencia", # categorías de los datos
                          title="Cuota de clientes") # titulo del grafico 

            st.plotly_chart(fig1, use_container_width = True) # mostramos el gráfico

            clientes = [] 
            clientes.append({"Clientes recurrentes": clientes_recurrentes,
                                "Clientes no recurrentes":clientes_no_recurrentes})
            df_clientes_recurrencia = pd.DataFrame(clientes).T.reset_index()
            df_clientes_recurrencia = df_clientes_recurrencia.rename(columns = {"index": "Values",0: "Nº_clientes"})
            df_clientes_recurrencia["Recurrencia"] = round((df_clientes_recurrencia['Nº_clientes']/df_clientes_recurrencia['Nº_clientes'].sum())*100, 2)
            
            fig2 = px.pie(df_clientes_recurrencia, # dataframe que contiene los datos
                        values='Recurrencia', # columna con los valores para determinar la posicion en el grafico
                        names="Values", # categorías de los datos
                        title="Recurrencia de clientes") # titulo del grafico 
            st.plotly_chart(fig2, use_container_width = True) # mostramos el gráfico

        with col2:

            tabla_clientes = info_clientes(conn)

            if elemento == "Gasto por cliente":

                tabla_clientes_gasto = tabla_clientes.sort_values("Gasto", ascending = False).head(30)
                fig3 = px.bar(tabla_clientes_gasto, 
                            x = "Gasto",
                            y = "Cliente",
                            title = "Gasto por cliente",
                            orientation = "h")
                fig3.update_layout( width=1000, 
                                    height=800,
                                    title_x=0.3,
                                    font_family="Courier New",
                                    font_color="blue",
                                    title_font_family="Times New Roman",
                                    legend_title_font_color="green")
                
                fig3.update_xaxes(title=None)
                fig3.update_yaxes(title=None)
                st.plotly_chart(fig3, use_container_width = True) # método para que me muestre el gráfico

            elif elemento == "Nº de reservas por cliente":

                tabla_clientes_reservas = tabla_clientes.sort_values("Nº reservas", ascending = False).head(30)
                fig4 = px.bar(tabla_clientes_reservas, 
                            x = "Nº reservas",
                            y = "Cliente",
                            title = "Nº de reservas por cliente",
                            orientation = "h")  
                fig4.update_layout( width=1000,  
                                    height=800,
                                    title_x=0.3,
                                    font_family="Courier New",
                                    font_color="blue",
                                    title_font_family="Times New Roman",
                                    legend_title_font_color="green")
                fig4.update_xaxes(title=None)
                fig4.update_yaxes(title=None)
                st.plotly_chart(fig4, use_container_width = True) # método para que me muestre el gráfico