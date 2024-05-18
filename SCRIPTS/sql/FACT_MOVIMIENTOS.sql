SELECT 
'Venta' as TIPO_REGISTRO,
CONCAT('V', [nro_orden])  as  ID_TRANSACCION,
fecha as FECHA_TRANSACCION,
sku AS SKU,
CASE WHEN sku_parent = 'No value' THEN NULL else sku_parent END AS SKU_PARENT,
[customer_id] AS CUSTOMER_ID,
precio AS PRECIO,
descuento AS DESCUENTO,
product_quantity_x_step_unit as CANTIDAD,
precio * product_quantity_x_step_unit - descuento AS VALOR_MOVIMIENTO
FROM DBO.FACT_VENTAS
WHERE sku IN (SELECT [SKU]   FROM [FRUBANA].[dbo].[DIM_VENTAS_FINAL] WHERE VENTA = 1 and COMPRA = 1)

UNION ALL

SELECT 
	  'Compra' as TIPO_REGISTRO,
	  CONCAT('C', [id]) as  ID_TRANSACCION
	  ,[delivery_date] as FECHA_TRANSACCION
      ,[sku] AS SKU
	  ,NULL AS SKU_PARENT	
      ,[supplier_id] AS CUSTOMER_ID
      ,[price] AS PRECIO
	  ,NULL AS DESCUENTO
      ,[quantity] AS CANTIDAD
	  ,[price] * [quantity] AS VALOR_MOVIMIENTO
  FROM [FRUBANA].[dbo].[FACT_COMPRAS]
WHERE [sku] IN (SELECT [SKU]   FROM [FRUBANA].[dbo].[DIM_VENTAS_FINAL] WHERE VENTA = 1 and COMPRA = 1)
