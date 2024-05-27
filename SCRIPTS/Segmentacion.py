# -*- coding: utf-8 -*-


import os
import pickle
import pandas as pd
import numpy as np
import os
import sys


from dotenv import dotenv_values

scripts_dir = os.path.join(os.getcwd(), 'SCRIPTS')
sys.path.append(scripts_dir)
from utils import conn_sql_server

# Cargar las variables de entorno desde el archivo .env
env_vars = dotenv_values(".env")

# Acceder a las variables de entorno
bd = env_vars["bd"]
server = env_vars["server"]
engine = conn_sql_server(bd, server)


# =============================================================================
# FUNCIONES
# =============================================================================


# Función para leer el archivo pickle y convertirlo en DataFrame
def lectura(data):
    with open(data, 'rb') as f:
        df = pickle.load(f)
    return df


# Definir la ruta raíz del proyecto
#root_dir = '/Users/linaherrera/Documents/GitHub/Frubana24/INPUTS/Ventas'


current_dir = os.getcwd()
# project_name = 'Frubana24'



# Encontrar el índice de la carpeta del proyecto
# project_index = current_dir.split(os.sep).index(project_name)

# Reconstruir la ruta del directorio base hasta 'Frubana24'
# base_dir = os.sep.join(current_dir.split(os.sep)[:project_index + 1])


# root_dir = os.path.join(base_dir, 'INPUTS/Ventas')



# # Lista de archivos pickle dentro del directorio Ventas
# meses = [
#     'df_sales_BAQ_1.pkl', 'df_sales_BAQ_2.pkl', 'df_sales_BAQ_3.pkl',
#     'df_sales_BAQ_4.pkl', 'df_sales_BAQ_5.pkl', 'df_sales_BAQ_6.pkl',
#     'df_sales_BAQ_7.pkl', 'df_sales_BAQ_8.pkl', 'df_sales_BAQ_9.pkl',
#     'df_sales_BAQ_10.pkl', 'df_sales_BAQ_11.pkl', 'df_sales_BAQ_12.pkl'
# ]



# Lista para almacenar los DataFrames
# dataframes = []

# # Leer cada archivo pickle y almacenarlo en la lista de DataFrames
# for mes in meses:
#     # Construir la ruta completa al archivo pickle
#     data_path = os.path.join(root_dir, mes)
#     df = lectura(data_path)
#     dataframes.append(df)

# Concatenar todos los DataFrames en uno solo
# ventas = pd.concat(dataframes, ignore_index=True)

ventas = pd.read_sql("SELECT *  FROM [FRUBANA].[dbo].[FACT_VENTAS]", con=engine)


# Groupby para hacer la segmentacion:
    
# Agrupar por id_cliente y sumar las ventas

# Agrupar por id_cliente y realizar varias operaciones de agregación
grouped_df = ventas.groupby('customer_id').agg(
    nro_orden_unicos=('nro_orden', 'nunique'),
    promedio_compra=('precio', 'mean')
).reset_index()


# Agrupar segmento: 
    
# Definir los valores de F1 y F2
F1 = 50000
F2 = 6

# Crear las condiciones y valores correspondientes
condiciones = [
    (grouped_df['nro_orden_unicos'] < F2) & (grouped_df['promedio_compra'] < F1),
    (grouped_df['nro_orden_unicos'] >= F2) & (grouped_df['promedio_compra'] < F1),
    (grouped_df['nro_orden_unicos'] < F2) & (grouped_df['promedio_compra'] >= F1),
    (grouped_df['nro_orden_unicos'] >= F2) & (grouped_df['promedio_compra'] >= F1)
]

valores = [1, 2, 3, 4]

# Crear la nueva columna 'nuevo_segmento' usando np.select()
grouped_df['Segmento'] = np.select(condiciones, valores)

nombre_campos = {'customer_id':"customer_id", 
                 'nro_orden_unicos':"num_compras", 
                 'promedio_compra':"PROMEDIO COMPRA", 
                 'Segmento':"SEGMENTACION"}
grouped_df = grouped_df.rename(columns = nombre_campos)

grouped_df.to_sql("DIM_SEGMENTACION",con=engine, index=False, if_exists='replace')


# Ahora se adicionará el segmento a la base de ventas.

# Mapear los segmentos al DataFrame original usando el id_cliente
ventas['SEGMENTO'] = ventas['customer_id'].map(grouped_df.set_index('customer_id')['SEGMENTACION'])

ventas.to_sql("FACT_VENTAS_SEGMENTACION",con=engine, index=False, if_exists='replace')

