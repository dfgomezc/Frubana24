WITH 

UltimaVenta 
	AS (
		SELECT 
			A.[fecha],
			A.[precio],
			B.[Nombre_estandarizado] AS producto,
			ROW_NUMBER() OVER (PARTITION BY [producto] ORDER BY [fecha] DESC) AS rn
		FROM [FRUBANA].[dbo].[FACT_VENTAS_SEGMENTACION] as A
		LEFT JOIN [FRUBANA].[dbo].[DIM_VENTAS_FINAL] AS B
		  ON A.[SKU] = B.[SKU]

	)
,precio_reciente 
	AS (
		SELECT producto, precio
		FROM UltimaVenta
		WHERE rn = 1
		)
, VENTAS_UN_PRODUCTO 
	AS (
	SELECT 
		a.[cantidad],
		D.[SEGMENTACION]  AS Segmento,
		B.[Nombre_estandarizado] AS producto
	FROM [FRUBANA].[dbo].[FACT_VENTAS] as A
	LEFT JOIN [FRUBANA].[dbo].[DIM_VENTAS_FINAL] AS B
		  ON A.[SKU] = B.[SKU]
		LEFT JOIN DIM_SEGMENTACION AS D
		ON A.[customer_id] = D.[customer_id]
	WHERE a.[nro_orden] IN (
		SELECT [nro_orden]
		FROM [FRUBANA].[dbo].[FACT_VENTAS_SEGMENTACION]
		GROUP BY [nro_orden]
		HAVING COUNT(*) = 1)
		)

,PRODUCTO_ESTANDARIZADO 
	AS (
		SELECT A.nro_orden
				,A.cantidad
				,D.[SEGMENTACION] AS Segmento
			  ,B.[Nombre_estandarizado] AS producto

		  FROM [FRUBANA].[dbo].[FACT_VENTAS_SEGMENTACION] AS A
		  LEFT JOIN [FRUBANA].[dbo].[DIM_VENTAS_FINAL] AS B
		  ON A.[SKU] = B.[SKU]
		  LEFT JOIN DIM_SEGMENTACION D
		  ON D.[customer_id] = a.[customer_id]
		  WHERE A.fecha >= '2023-01-01'
		)
 , PRODUCTOS_CANASTAS 
	 AS (
		 SELECT * FROM PRODUCTO_ESTANDARIZADO
		 where producto IN (SELECT [antecedents] FROM [FRUBANA].[dbo].[FACT_CANASTAS])
		 or producto IN (SELECT [consequents] FROM [FRUBANA].[dbo].[FACT_CANASTAS])
		 )
 , COMBINACIONES_CANASTAS
	 AS (
	 SELECT A.nro_orden, A.Segmento, A.cantidad AS cantidad_antecedente, A.producto AS prodcuto_antecedente
	 ,B.cantidad AS cantidad_consecuente, B.producto AS prodcuto_consecuente
	 FROM PRODUCTOS_CANASTAS AS A
	 LEFT JOIN PRODUCTOS_CANASTAS AS B
	 ON A.nro_orden = B.nro_orden 
	 )

, relacion_compra_productos AS (
 
 SELECT prodcuto_antecedente, prodcuto_consecuente, Segmento,
sum(cantidad_consecuente)/sum(cantidad_antecedente) AS cantidad_relativa
 
 FROM COMBINACIONES_CANASTAS

 GROUP BY prodcuto_antecedente, prodcuto_consecuente, Segmento )

 , probabilidad_compra AS (
 SELECT  [antecedents]
      ,[consequents]
	  ,[Segmento]
      ,MAX([confidence]) AS [confidence]
      
  FROM [FRUBANA].[dbo].[FACT_CANASTAS]

  GROUP BY [antecedents],[consequents],[Segmento]
 )

, impacto_por_compra 
	AS (
	SELECT 
	A.[producto],
	A.[cantidad],
	A.[Segmento],
	B.prodcuto_consecuente,
	B.cantidad_relativa
	,c.precio
	,d.confidence
	FROM VENTAS_UN_PRODUCTO A
	INNER JOIN relacion_compra_productos B
	ON A.[producto] = B.prodcuto_antecedente
	INNER JOIN precio_reciente C
	ON B.[prodcuto_consecuente] = C.producto
	INNER JOIN probabilidad_compra	D
	ON A.[producto] = D.[antecedents]
		AND A.[Segmento] = D.[Segmento]
		AND B.prodcuto_consecuente = D.[consequents]
	)

SELECT segmento, 
		sum(cantidad_relativa*precio*confidence) AS estimado

FROM impacto_por_compra
GROUP BY segmento

SELECT sum([precio]*[product_quantity_x_step_unit]-descuento) 
FROM [FRUBANA].[dbo].[FACT_VENTAS]

