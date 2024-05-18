import os
import sys
from sqlalchemy import create_engine
import statsmodels.api as sm
import pandas as pd

def conn_sql_server(db:str,server:str):
    # configurar conexión a base de datos SQLServer
    database_name = db #'FRUBANA'
    server_name = server # 'TORRE_DG\SQLEXPRESS'
    connection_string = f'mssql+pyodbc://{server_name}/{database_name}?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes'
    engine = create_engine(connection_string, echo=True)
    return engine

def calcular_elasticidad(df):
    # Agregar logaritmos a los datos
    df['log_precio'] = np.log(df['PRECIO_FINAL'])
    df['log_cantidad'] = np.log(df['product_quantity_x_step_unit'])

    # Ajustar el modelo de regresión lineal log-log
    X = sm.add_constant(df['log_precio'])  # Variable independiente (logaritmo del precio)
    y = df['log_cantidad']  # Variable dependiente (logaritmo de la cantidad)

    modelo = sm.OLS(y, X).fit()

    # Obtener los coeficientes del modelo
    coef_precio = modelo.params['log_precio']
    
    # Obtener el valor del R² ajustado
    r_cuadrado_ajustado = modelo.rsquared_adj

    # Calcular la elasticidad
    elasticidad = coef_precio
    
    # Determinar el tipo de elasticidad
    tipo_elasticidad = 'Inelástico' if abs(elasticidad) < 1 else 'Elástico'

    # Retornar la elasticidad, el tipo de elasticidad y el R² ajustado
    return pd.Series({'elasticidad': elasticidad, 'tipo_elasticidad': tipo_elasticidad, 'R_cuadrado_ajustado': r_cuadrado_ajustado})
