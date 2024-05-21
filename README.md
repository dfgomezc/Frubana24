# Grupo 24

![Frubana](IMG/fondo_frubana_2.jpeg.png)

Bienvenidos al repositorio del Proyecto de Grado de la Maestría de Inteligencia Analítica de Datos de la Universidad de los Andes - segunda cohorte.

# "Generar Recomendaciones Relevantes para los Clientes de Frubana"
El Proyecto contempla el Desarrollo de una herramienta de visualización de datos con el objetivo de obtener insights relevantes para el área comercial de Frubana. Al igual, que preferencias y necesidades de los clientes, y generar recomendaciones
relevantes. 

# ¿Qué es Frubana?
Es una empresa de tecnología que surge con la idea de ofrecer alimentos más baratos para Latinoamérica, optimizando los procesos de compra en el campo y tecnificando el negocio en la plaza de mercado. Se trata de una aplicación disponible para agricultores y dueños de restaurantes, con el fin de integrar la oferta y la demanda de productos alimenticios. De esta forma es posible obtener una importante sinergia entre tecnología, agricultura y gastronomía. Portafolio 7 octubre de 2018.

# ¿Cuáles fueron los Modelos Seleccionados?
Se seleccionó el **Modelo A Priori** por su simplicidad eficiencia y capacidad para adaptarse a segmentos de clientes específicos al enfocarse en la popularidad de los productos dentro de cada segmento de clientes, el modelo a priori puede ofrecer recomendaciones
relevantes y efectivas, incluso en segmentos con poca diversidad de productos.

Para el cálculo de las **Elasticidades** se empleó el modelo **log log** de elasticidad que se basa en tomar logaritmos naturales de las variables involucradas y sus resultados son consistentes.

# ¿Cómo se realizo la segmentación?
Se definió realizar una segmentación general de los clientes. Esta segmentación se basa en dos variables clave: la frecuencia de compras y el valor promedio de las compras. La decisión de escoger estas variables se basa en la gráfica de dispersión que se observa a continuación donde se muestra la concentración de los clientes cerca al origen, sin embargo, también se observan grupos de clientes fuera de esta zona. Al segmentar a los clientes en grupos más homogéneos en función de estos criterios, se obtuvo recomendaciones más precisas y relevantes para cada segmento, buscando mejorar la experiencia de compra de los clientes y aumentar la efectividad de las estrategias de marketing de Frubana.

De igual forma, se definió realizar una segmentación de clientes con reglas duras, esta es una herramienta con un enfoque claro y eficiente que permite personalizar las recomendaciones de canastas de productos de Frubana; al asignar a cada cliente a un segmento exclusivo según su comportamiento de compra. Esta estrategia permite ofrecer sugerencias más relevantes y atractivas, aumentando así la probabilidad de que los clientes realicen compras adicionales y mejoren su satisfacción con la plataforma.

Posteriormente se procedió a fijar los parámetros para definir los segmentos. Para esto se realizaron diferentes iteraciones que tenían como fin balancear cada segmento. Así al final se llegó a dos parámetros para realizar la separación: una frecuencia de 5 o menos compras y un valor promedio de $50,000 en cada compra o menos.

Los cuatro segmentos definidos son:
1. Clientes Ocasionales y de Bajo Gasto: 3.384 clientes.
2. Clientes Ocasionales y de Alto Gasto: 1.280 clientes.
3. Clientes Frecuentes y de Bajo Gasto: 3.733 clientes.
4. Clientes Frecuentes y de Alto Gasto: 2.035 clientes.

# Vista del visualizador de la herramienta en PowerBI













