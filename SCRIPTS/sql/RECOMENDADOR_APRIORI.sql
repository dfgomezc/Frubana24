SELECT RECO.[Items]
      ,RECO.[Support]
      ,RECO.[Base Items]
      ,RECO.[Add Items]
      ,RECO.[Confidence]
      ,RECO.[Lift]
	  ,max(DIM.Link) AS IMAGEN_SEGMENTADOR
	  ,max(DIM2.Link) AS IMAGEN_RECOMENDACION
  FROM [FRUBANA].[dbo].[RECOMENDACIONES_APRIORI] AS RECO
LEFT JOIN [FRUBANA].[dbo].[DIM_VENTAS_FINAL] as DIM
ON RECO.[Base Items] = DIM.Nombre_estandarizado
LEFT JOIN [FRUBANA].[dbo].[DIM_VENTAS_FINAL] as DIM2
ON RECO.[Add Items] = DIM2.Nombre_estandarizado
GROUP BY RECO.[Items]
      ,RECO.[Support]
      ,RECO.[Base Items]
      ,RECO.[Add Items]
      ,RECO.[Confidence]
      ,RECO.[Lift]