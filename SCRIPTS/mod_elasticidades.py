import pandas as pd
import os
import sys
import numpy as np
import statsmodels.api as sm

scripts_dir = os.path.join(os.getcwd(), 'SCRIPTS')
sys.path.append(scripts_dir)

from utils import conn_sql_server, calcular_elasticidad

# Definir una función para calcular la elasticidad y agregar el campo de tipo de elasticidad


from dotenv import dotenv_values

# Cargar las variables de entorno desde el archivo .env
env_vars = dotenv_values(".env")

# Acceder a las variables de entorno
bd = env_vars["bd"]
server = env_vars["server"]
engine = conn_sql_server(bd, server)


productos_descuentos = pd.read_sql("""SELECT A.[nro_orden]
      ,A.[fecha]
      ,A.[producto]
      ,A.[cantidad]
      ,A.[precio]
      ,A.[descuento]
      ,A.[customer_id]
      ,A.[sku]
      ,A.[product_id]
      ,A.[product_quantity_x_step_unit]
      ,A.[product_step_unit]
      ,A.[product_unit]
      ,A.[sku_parent]
      ,A.[month]
	  ,A.[precio]-A.[descuento]/A.[product_quantity_x_step_unit] AS PRECIO_FINAL
	  ,COALESCE(B.[SEGMENTACION],0) AS SEGMENTO
	  ,(SELECT C.[Nombre_estandarizado] FROM [FRUBANA].[dbo].[DIM_VENTAS_FINAL] C WHERE C.[SKU] = A.[sku]) AS nombre_estandarizado
	  ,(SELECT C.[Nom_general] FROM [FRUBANA].[dbo].[DIM_VENTAS_FINAL] C WHERE C.[SKU] = A.[sku]) AS nombre_general
	  
  FROM [FRUBANA].[dbo].[FACT_VENTAS] A
  LEFT JOIN [FRUBANA].[dbo].[SEGMENTACION] B
  ON A.[customer_id] = B.[customer_id]
  WHERE A.[descuento]>0""",con=engine)

productos_descuentos = productos_descuentos.dropna(subset=['PRECIO_FINAL', 'product_quantity_x_step_unit'])
productos_descuentos = productos_descuentos.replace([np.inf, -np.inf], np.nan).dropna()


# Filtrar los datos para eliminar filas con precios o cantidades menores o iguales a cero
productos_descuentos = productos_descuentos[(productos_descuentos['PRECIO_FINAL'] > 0) & 
                                            (productos_descuentos['product_quantity_x_step_unit'] > 0)]



# Calcular la elasticidad, el tipo de elasticidad y el R² ajustado para cada producto
elasticidades_por_producto = productos_descuentos.groupby('nombre_estandarizado').apply(calcular_elasticidad)

productos_sin_descuentos = pd.read_sql("""SELECT A.[nro_orden]
      ,A.[fecha]
      ,A.[producto]
      ,A.[cantidad]
      ,A.[precio] AS PRECIO_FINAL
      ,A.[descuento]
      ,A.[customer_id]
      ,A.[sku]
      ,A.[product_id]
      ,A.[product_quantity_x_step_unit]
      ,A.[product_step_unit]
      ,A.[product_unit]
      ,A.[sku_parent]
      ,A.[month]
	  ,COALESCE(B.[SEGMENTACION],0) AS SEGMENTO
	  ,(SELECT C.[Nombre_estandarizado] FROM [FRUBANA].[dbo].[DIM_VENTAS_FINAL] C WHERE C.[SKU] = A.[sku]) AS nombre_estandarizado
	  ,(SELECT C.[Nom_general] FROM [FRUBANA].[dbo].[DIM_VENTAS_FINAL] C WHERE C.[SKU] = A.[sku]) AS nombre_general
	  
  FROM [FRUBANA].[dbo].[FACT_VENTAS] A
  LEFT JOIN [FRUBANA].[dbo].[SEGMENTACION] B
  ON A.[customer_id] = B.[customer_id]
  WHERE A.[descuento]=0""",con=engine)

elasticidades_por_producto_sin_descuentos = productos_sin_descuentos.groupby('nombre_estandarizado').apply(calcular_elasticidad)

productos_sin_descuentos = productos_sin_descuentos[(productos_sin_descuentos['PRECIO_FINAL'] > 0) & 
                                                    (productos_sin_descuentos['product_quantity_x_step_unit'] > 0)]

comparacion_elasticidades = elasticidades_por_producto_sin_descuentos.merge(elasticidades_por_producto, 
                                                                           left_index=True, right_index=True, 
                                                                           suffixes=('_sin_descuentos', '_con_descuentos'))

# Identificar productos susceptibles a descuentos (elasticidad mayor en el DataFrame con descuentos)
productos_susceptibles_descuentos = comparacion_elasticidades[
    comparacion_elasticidades['elasticidad_con_descuentos'].abs() > comparacion_elasticidades['elasticidad_sin_descuentos'].abs()
]

productos_susceptibles_descuentos.to_sql(name="ELASTICIDAD_PRODUCTOS", con=engine, index=False, if_exists='replace')
