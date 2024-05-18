import os
import sys
import pandas as pd
import numpy as np
import statsmodels.api as sm
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules

scripts_dir = os.path.join(os.getcwd(), 'SCRIPTS')
sys.path.append(scripts_dir)
from utils import conn_sql_server

from dotenv import dotenv_values

# Cargar las variables de entorno desde el archivo .env
env_vars = dotenv_values(".env")

# Acceder a las variables de entorno
bd = env_vars["bd"]
server = env_vars["server"]
engine = conn_sql_server(bd, server)

canastas = pd.read_sql("""SELECT * FROM [FRUBANA].[dbo].[FACT_VENTAS_SEGMENTACION]""",con=engine)

tabla_ventas_mod1 = canastas[['nombre_estandarizado','nro_orden']][canastas['SEGMENTO']==3]
records = []
for i in tabla_ventas_mod1['nro_orden'].unique():
    records.append(list(tabla_ventas_mod1[tabla_ventas_mod1['nro_orden'] == i]['nombre_estandarizado'].values))

canastas_mas_de_un_producto = [ele for ele in records if len(ele)>1]
canastas_mas_de_un_producto

# Tus datos en formato de lista de listas
datos = canastas_mas_de_un_producto

# Instanciar y ajustar TransactionEncoder
encoder = TransactionEncoder()
encoder.fit(datos)

# Transformar los datos a formato binario (one-hot encoding)
datos_encoded = encoder.transform(datos)

# Convertir los datos a DataFrame de pandas
df = pd.DataFrame(datos_encoded, columns=encoder.columns_)

# Aplicar el algoritmo de Apriori para encontrar itemsets frecuentes
frequent_itemsets = apriori(df, min_support=0.1, use_colnames=True)

# Generar reglas de asociación
rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.5)
rules.to_sql(name="RULES_ASSOCIATION", con=engine, index=False, if_exists='replace')


