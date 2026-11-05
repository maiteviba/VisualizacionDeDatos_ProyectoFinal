# Proyecto Final:

## Dashboard de ventas con Streamlit

Este repositorio contiene el código desarrollado para el proyecto final de la asignatura de Visualización de Datos de 2º iMAT.

El objetivo es crear una aplicación interactiva con Streamlit para analizar las ventas de una cadena de tiendas. La aplicación tiene cuatro secciones:

1. Visualización global: métricas generales, categorías y tiendas con más ventas y evolución semanal y mensual
2. Información por tienda: ventas por año y productos vendidos, con y sin promoción
3. Información por estado: transacciones por año, ranking de tiendas y producto más vendido
4. Comparación de ventas con y sin promoción a lo largo de los meses


## Estructura del proyecto

- `app.py`: código de la aplicación
- `parte_1.csv` y `parte_2.csv`: datos utilizados, divididos en dos archivos por su tamaño y subidos con Git LFS
- `requirements.txt`: librerías necesarias


## Ejecución

streamlit run app.py


## Requisitos

Para ejecutar el código es necesario tener instalado Python 3 y las siguientes librerías:

streamlit
pandas
matplotlib
numpy
