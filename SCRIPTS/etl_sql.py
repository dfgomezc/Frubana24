import os
import sys

import pandas as pd
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
# COMPRAS
# =============================================================================
format_compras = {
                    'warehouse_code' : str,
                    'region_code': str,
                    'id': str,
                    #'delivery_date': str,
                    'product_id': str,
                    'sku': str,
                    'name': str,
                    'supplier_id': str, 
                    #'price': str,
                    #'quantity': str
                    }

df_compras = pd.read_csv("INPUTS/BAQ_compras.csv",dtype=format_compras, parse_dates=['delivery_date'], thousands=',', decimal='.')
df_compras.info()
df_compras.id.nunique() # todos son unicos
df_compras.columns
df_compras.to_sql(name="FACT_COMPRAS", con=engine, index=False, if_exists='replace')

# =============================================================================
# PRODUCTOS
# =============================================================================

format_productos = {
'product_id': str,
'sku': str,
'name': str,
'category': str,
'region_code': str,
'product_category_id': str, 
#'mean_shelf_life': str,
#'promised_lead_time': str,
#'purchasing_unit': str,
'buy_unit': str,
#'weight_parameter_apricot': str,
}
df_products = pd.read_csv("INPUTS/Products_BAQ.csv", dtype=format_productos, thousands=',', decimal='.')
df_products.info()
print(df_products.product_category_id.nunique()) # solamente hay un registro con valor igual a 1
df_products.columns
#df_products.drop(columns=['product_category_id'])
# df_compras.to_sql(name="FACT_COMPRAS", con=engine, index=False, if_exists='replace')
# df_products
df_products.to_sql(name="DIM_PRODUCTS", con=engine, index=False, if_exists='replace')


# =============================================================================
# VENTAS
# =============================================================================

# importar ventas

format_ventas = {
'nro_orden': str, 
'fecha': str, 
'producto': str, 
#'cantidad': str, 
#'precio': str, 
#'descuento': str, 
'customer_id': str, 
'sku': str, 
'product_id': str, 
#'product_quantity_x_step_unit': str, 
#'product_step_unit': str, 
'product_unit': str, 
'sku_parent': str, 
'month': str, 
}

dir_archivos_ventas = os.listdir("INPUTS/Ventas/")
list_archivos_ventas = []
for archivo in dir_archivos_ventas:
    df_ventas = pd.read_pickle("INPUTS/Ventas/"+archivo)
    list_archivos_ventas.append(df_ventas)
df_hist_ventas = pd.concat(list_archivos_ventas).reset_index(drop=True)
df_hist_ventas["cantidad"] = df_hist_ventas.cantidad.astype('float64')
df_hist_ventas["precio"] = df_hist_ventas.precio.astype('float64')
df_hist_ventas["descuento"] = df_hist_ventas.descuento.astype('float64')
df_hist_ventas["product_quantity_x_step_unit"] = df_hist_ventas.product_quantity_x_step_unit.astype('float64')
df_hist_ventas["product_step_unit"] = df_hist_ventas.product_step_unit.astype('float64')

df_hist_ventas.info()
# df_hist_ventas.columns
df_hist_ventas.to_sql(name="FACT_VENTAS", con=engine, index=False, if_exists='replace')

# =============================================================================
# TABLA DE PRODUCTOS ESTANDARIZADOS MANUALMENTE
# =============================================================================

DIM_producto_final = pd.read_excel("INPUTS/DIM_productos.xlsx")
DIM_producto_final.to_sql(name="DIM_VENTAS_FINAL", con=engine, index=False, if_exists='replace')

# =============================================================================
# VENTAS CON SEGMENTACION
# =============================================================================
canastas = pd.read_excel("INPUTS/VENTAS_CON_SEGMENTACION.xlsx")
canastas.to_sql(name="FACT_VENTAS_SEGMENTACION", con=engine, index=False, if_exists='replace')


# =============================================================================
# CANASTAS
# =============================================================================
canastas = pd.read_excel("INPUTS/canastas.xlsx")
canastas.to_sql(name="FACT_CANASTAS", con=engine, index=False, if_exists='replace')

# =============================================================================
# SEGMENTACION CLIENTES
# =============================================================================
canastas = pd.read_excel("INPUTS/segmentacion_clientes.xlsx")
canastas.to_sql(name="DIM_SEGMENTACION", con=engine, index=False, if_exists='replace')


# =============================================================================
# IMPACTO CANASTAS
# =============================================================================


with open('SCRIPTS/sql/IMPACTO_CANASTAS.sql', 'r') as archivo_sql:
    sql_impacto_canastas = archivo_sql.read()

# Imprime el contenido leído

impacto_canastas = pd.read_sql(sql_impacto_canastas,con=engine)

impacto_canastas.to_sql(name="RESULT_IMPACTO", con=engine, index=False, if_exists='replace')



