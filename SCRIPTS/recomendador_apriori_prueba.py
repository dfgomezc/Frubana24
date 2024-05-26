#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 26 00:47:46 2024

@author: linaherrera
"""

#!pip install apyori  # en caso de no poner instalar apryori

from apyori import apriori
import os
import pandas as pd
import sys
import numpy as np
import pandas as pd
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
import warnings
warnings.filterwarnings("ignore")
import re


current_dir = os.getcwd()
project_name = 'Frubana24'



# Encontrar el índice de la carpeta del proyecto
project_index = current_dir.split(os.sep).index(project_name)

# Reconstruir la ruta del directorio base hasta 'Frubana24'
base_dir = os.sep.join(current_dir.split(os.sep)[:project_index + 1])

# Definir las rutas relativas a partir del directorio base
input_dir = os.path.join(base_dir, 'INPUTS')
input_file = os.path.join(input_dir, 'VENTAS_CON_SEGMENTACION.xlsx')  # Archivo de entrada

#Leer data 

df = pd.read_excel(input_file)


# MODELO A PRIORI


# Función para aplicar la codificación binaria
def encode_unit(x):
    if x <= 0:
        return 0
    if x >= 1:
        return 1

# Función para limpiar los elementos de las reglas
def remove_parentheses(x):
    x = str(x)
    return re.sub(r'\(|\)', '', x)

# DataFrame para almacenar todas las reglas
all_rules = pd.DataFrame()

for segment in range(0, 4):  # Genera reglas para segmentos 1 a 5
    df_segment = df[df['SEGMENTO'] == segment]

    if df_segment.empty:
        continue  # Salta el segmento si está vacío

    basket = pd.crosstab(df_segment['nro_orden'], df_segment['nombre_estandarizado'])
    basket_set = basket.applymap(encode_unit)
    
    frecuencia_items = apriori(basket_set, min_support=0.01, use_colnames=True)
    rules = association_rules(frecuencia_items, metric='lift', min_threshold=1)
    
    rules['consequents'] = rules['consequents'].apply(lambda x: list(x)[0])
    rules['antecedents'] = rules['antecedents'].apply(lambda x: list(x)[0])
    
    # Agregar columna para identificar el segmento
    rules['segment'] = segment
    
    # Agregar las reglas al DataFrame total
    all_rules = pd.concat([all_rules, rules], ignore_index=True)

# Limpiar las columnas de 'consequents' y 'antecedents'
all_rules['consequents'] = all_rules['consequents'].apply(remove_parentheses)
all_rules['antecedents'] = all_rules['antecedents'].apply(remove_parentheses)

# Guardar el DataFrame resultante
output_file = os.path.join(input_dir, 'canastas.xlsx')
all_rules.to_excel(output_file, index=False)


