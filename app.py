import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import calendar
import numpy as np


# configuración de la página
st.set_page_config(
    page_title= "Proyecto Streamlit",
    layout="wide",
    initial_sidebar_state="collapsed"
)


@st.cache_data
def cargar_df():

    df1 = pd.read_csv("parte_1.csv", low_memory = False)
    df2 = pd.read_csv("parte_2.csv", low_memory=False)
    df = pd.concat([df1, df2], ignore_index=True)

    return df

df = cargar_df()



PAGINAS = ["Visualización global", 
           "Información por tienda", 
           "Información por estado", 
           "Comparación ventas con y sin ahorro"]

tiendas = sorted(df['store_nbr'].unique())
estados = sorted(df['state'].unique())


# Menu lateral
with st.sidebar:
    st.title("⚙️ Menú de selección")
    st.divider()

    # Selector de páginas
    pagina = st.selectbox("Seleccione una sección: ",
                          PAGINAS)
    
    st.divider()

    # st.subheader()
    st.caption("@ Maite Viejo Baena 2026")


# Página de inicio
st.title("Recap de ventas del año")

# Utilizo dividers a lo largo de todo el script para que el resultado tenga una mejor estética
st.divider()

###############
# PÁGINAS
###############


#Página 1:
if pagina == "Visualización global":

    st.header("📈 Visualización global")


    seccion = st.selectbox("###### Seleccione la estadística que desea:", 
                           ["Datos generales", 
                            "Análisis en términos medios", 
                            "Análisis de la estacionalidad"])


    if seccion == "Datos generales":

        col1, col2 = st.columns(2)
        with col1:
            st.metric("🛍️ Número de tiendas: ", df['store_nbr'].nunique())
        with col2:
            st.metric(f"📦 Número de productos: ", df['family'].nunique())

        col3, col4 = st.columns(2)
        with col3:
            st.metric("🗺️ Estados: ", df['state'].nunique())
        with col4:
            st.metric("🗓️ Meses de los datos", df['month'].nunique())


    if seccion == "Análisis en términos medios":
        
        col1, col2 = st.columns(2)

        with col1:
            top10 = (df.groupby('family')['sales'].sum().sort_values(ascending=False).head(10).round(0).reset_index())
            top10.columns = ["Categoría", "Ventas"]
            st.write("#### TOP 10 productos")
            st.write("")
            st.write("")
            st.table(top10)
        
        with col2:
            top10_tiendas = (df[df['onpromotion']>0].groupby('store_nbr')['sales'].sum().sort_values(ascending=False).head(10).reset_index())
            top10_tiendas.columns = ["Tienda", "Ventas en promoción"]
            st.write("#### Top 10 tiendas con ventas en productos en promoción")
            st.table(top10_tiendas)
        
        st.divider()

        # Utilizo un boxplot para representar la distribución ya que permite mostrar de forma clara la distribución de los datos,
        # identificar su mediana, valores atípicos...
        st.subheader("Distribución de ventas por tiendas")
        ventas_tienda = df.groupby("store_nbr")['sales'].sum()

        fig, ax = plt.subplots(figsize=(10,4))
        ax.boxplot(ventas_tienda.values, vert = False, showfliers=True)
        ax.set_xlabel("Ventas por tienda")
        st.pyplot(fig)

        # Se observa una alta dispersión en las ventas de las tiendas, con presencia de valores
        # atípicos que indican que el valor de las tiendas a las que se le asocian tienen un volumen 
        # de ventas significativamente mayor en comparación al resto.


    if seccion == "Análisis de la estacionalidad":

        dia_semana = df.groupby('day_of_week')['sales'].mean().sort_values(ascending=False).head(1)
        st.write('### 🗓️ Día de la semana con más ventas medias:')
        st.markdown(f"#### {dia_semana.index[0]}")

        st.divider()
        
        col1, col2 = st.columns(2)

        with col1:
            volumen_semana = (df.groupby('week')['sales'].mean().sort_index())
            st.write("#### Volumen de ventas medio por semana del año")
            st.dataframe(volumen_semana, height=455)


        
        with col2:
            volumen_mes = (df.groupby('month')['sales'].mean().sort_index())
            st.write("#### Volumen de ventas medio por mes del año")
            st.dataframe(volumen_mes, height=455)

        st.divider() 


#Página 2:
if pagina == "Información por tienda":

    st.header ("ℹ️ Información por tienda")

    tienda = st.selectbox("###### Seleccione la tienda que desee:", tiendas)
    df_tienda = df[df['store_nbr']==tienda]
    
    st.header ("Métricas")

    col1, col2, col3 = st.columns(3)
    with col1:
        ventas_año = df_tienda.groupby('year')['sales'].sum()
        st.write("##### Número total de ventas por año: ")
        st.table(ventas_año)
    with col2:
        n_productos = df_tienda['family'].nunique()
        st.metric("##### Número total de productos vendidos", n_productos)
    with col3:
        promocion = len(df_tienda[df_tienda['onpromotion']> 0])
        st.metric("##### Número total de productos vendidos en promoción", promocion)


#Página 3:
if pagina == "Información por estado":

    st.header("🗺️ Ventas por nivel de estado")

    estado = st.selectbox("###### Seleccione un estado:", estados)
    df_estado = df[df['state'] == estado]
    
    st.divider()
    
    ventas = (df_estado.groupby("year")['transactions'].sum().reset_index())
    ventas.columns = ['Año', 'Transacciones']
    st.subheader("Número total de transacciones por año")
    st.table(ventas)
    
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:

        store = (df_estado.groupby('store_nbr')['sales'].sum().sort_values(ascending = False).reset_index())
        store.columns = ['Tienda', 'Ventas']
        st.write("##### Ranking de tiendas con más ventas")
        st.table(store)

    with col2:
        producto = df_estado.groupby('family')['sales'].sum().sort_values(ascending = False).head(1)
        st.metric("##### Producto más vendido en el estado", producto.index[0])


#Página 4:
if pagina == "Comparación ventas con y sin ahorro":
    
    st.subheader("🛍️ Comparación de ventas con y sin ahorro")

    promo = (df[df['onpromotion']>0].groupby('month')['sales'].sum().sort_index())
    no_promo = (df[df['onpromotion']==0].groupby('month')['sales'].sum().sort_index())

    meses = [calendar.month_name[m] for m in promo.index]

    x = np.arange(len(meses))
    width = 0.4

    fig, ax = plt.subplots(figsize =(10,5))

    ax.bar(x-width/2, no_promo.values, width, label = "Ventas sin promoción")
    ax.bar(x+width/2, promo.values, width, label = "Ventas con promoción")
    
    ax.set_ylabel("Ventas totales")
    ax.set_xticks(x)
    ax.set_xticklabels(meses, rotation = 45)
    ax.legend()

    st.pyplot(fig)

    st.divider()

    st.subheader("Categorías con mayores ventas por mes")

    df_no_promo_cat = (df[df['onpromotion'] == 0].groupby(['month', 'family'])['sales'].sum().reset_index())
    df_promo_cat = (df[df['onpromotion']>0].groupby(['month', 'family'])['sales'].sum().reset_index())

    top_promo = df_promo_cat.loc[df_promo_cat.groupby('month')['sales'].idxmax()][['month', 'family']]
    top_promo.columns = ['Mes', 'Categoría con promoción']

    top_no_promo = df_no_promo_cat.loc[df_no_promo_cat.groupby('month')['sales'].idxmax()][['month', 'family']]
    top_no_promo.columns = ['Mes', 'Categoría sin promoción']

    tabla_categorias = top_no_promo.merge(top_promo, on="Mes", how="inner").sort_values("Mes")
    tabla_categorias['Mes'] = tabla_categorias['Mes'].apply(lambda x: calendar.month_name[x])
    st.table(tabla_categorias)
