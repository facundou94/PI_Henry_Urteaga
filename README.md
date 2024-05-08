﻿# PI_Henry_Urteaga
<h1 align="center"> Proyecto Individual Nº 1  </h1>
<h3 align="center"> Machine Learning Operations (MLOps) </h3>
<h3 align="center"> Autor: Bioing. Facundo Urteaga  </h3>

<p align="left">
   <img src="https://img.shields.io/badge/ESTADO-EN%20DESAROLLO-green">
   </p>

## Índice

*[Descripción del proyecto](#descripción-del-proyecto)

*[1_Extracción](#1-extraccion)

*[2_Transformación](#2-transformación)

*[3_EDA](#3-EDA)

*[4_Sentiment_Analysis](#4-sentiment-analysis)

*[5_Sistema_de_Recomendación](#5-sistema-de-recomendación)

*[6_Funciones_y_deploying](#6-funciones-y-deploying)

## Descripción del proyecto

<p align="justify">
Situación problemática: Como integrante del equipo de Data Science en Steam, se me ha encomendado la misión de desarrollar un sistema de recomendación de videojuegos para nuestros estimados usuarios. Sin embargo, al adentrarme en la exploración de los datos disponibles, me he percatado de un desafío que requiere nuestra atención: la madurez de los datos es, en términos generales, incipiente. Nos enfrentamos a archivos de datos sin procesar y desprovistos de estructura, y carecemos de mecanismos automatizados para mantenernos actualizados con los lanzamientos más recientes.
Este escenario plantea un reto significativo para la implementación exitosa de nuestro proyecto. No obstante, lo abordaremos como una oportunidad para demostrar nuestras habilidades de ingeniería de datos y establecer los cimientos de un Producto Mínimo Viable (MVP) que oriente nuestros esfuerzos. Aunque la tarea inicial pueda parecer desalentadora, estamos plenamente comprometidos a convertirla en un proyecto exitoso mediante una planificación cuidadosa y una ejecución precisa.
Con este enfoque, nos embarcamos en esta empresa con confianza y determinación, listos para superar los desafíos que surjan en el camino y alcanzar nuestros objetivos con éxito.
A continuación, la descripción de cada capítulo será coincidente con los scripts realizados para el trabajo y con el orden de procesamiento.

## 1 Extracción

</p>
La fase de extracción de datos implicó la implementación de funciones específicas para recuperar información de los archivos "users_items", "users_reviews" y "steam_games". Inicialmente, se planeó desarrollar una función general que pudiera utilizarse para los tres archivos; sin embargo, debido a las singularidades de cada uno, resultó necesario crear una función de extracción individual para cada archivo. Este proceso representó una de las etapas más extensas del proyecto, ya que implicó principalmente un enfoque de prueba y error basado en la verificación empírica. Los archivos originales en formato json, debido a su tamaño, no están incluídos en este repositorio, pero se puede acceder a ellos en el siguiente repositorio: https://drive.google.com/drive/folders/1HqBG2-sUkz_R3h1dZU5F2uAzpRn7BSpj
</p>

## 2 Transformación

</p>
En este proceso, se lleva a cabo el desanidado de columnas específicas que contenían datos anidados, la normalización y la limpieza general de los datos. Además, se realizan una serie de análisis que podrían considerarse una primera parte de EDA. Por ejemplo, identificar que el tiempo jugado por los usuarios  las últimas dos semanas (last_2_weeks) sea "lógico" (Figura 1), o que la distribución del porcentaje de opiniones positivas de los juegos tenga sentido (Figura 2).
</p>

<p align="center">
   <img src="Imagenes/1_dens_2_weeks.jpg" width="400">
</p>
<p align="center">
   <em>Figura 1: Distribución de tiempo jugado las últimas dos semanas por usuario </em>
</p>

<p align="center">
   <img src="Imagenes/2_dens_op_pos.jpg" width="400">
</p>
<p align="center">
   <em>Figura 2: Densidad de opiniones positivas totales (de 0 a 100 %) </em>
</p>

## 3 EDA

</p>
En esta etapa se realiza el análisis exploratorio general, lo cual servirá para entender el comportamiento y el contexto de los datos antes de realizar las funciones y algoritmos posteriores. Dentro de esta etapa se destaca:
* La evolución de la distribución de precios segun las fechas de lanzamiento, donde se observa una tendencia de disminución del promedio de los precios en el paso de los años, pero a su vez por lógica los juegos más caros son los más actuales aunque sean los menos (Figura 3).
* El crecimiento exponencial (Se osberva como un crecimiento lineal ya que es el logaritmo de la frecuencia) de lanzamiento de juegos en el paso de los años (Figura 4).
* La cantidad de items por usuario, donde la mayoría contiene entre 10 y 100 items (Figura 5).
* Las etiquetas mas preponderantes de tags, specs y genres (Figuras 6, 7 y 8)
</p>

<p align="center">
   <img src="Imagenes/3_violin_precios.jpg" width="400">
</p>
<p align="center">
   <em>Figura 3: Violin Plot de precio de venta de los juegos por año de lanzamiento </em>
</p>

p align="center">
   <img src="Imagenes/4_cantidad_juegos.jpg" width="400">
</p>
<p align="center">
   <em>Figura 4: Cantidad de juegos lanzados a la plataforma por año </em>
</p>

p align="center">
   <img src="Imagenes/6_proporcion_tag.jpg" width="400">
</p>
<p align="center">
   <em>Figura 5: Proporciones de tags </em>
</p>

p align="center">
   <img src="Imagenes/6_proporcion_spec.jpg" width="400">
</p>
<p align="center">
   <em>Figura 6: Proporciones de specs </em>
</p>

p align="center">
   <img src="Imagenes/6_proporcion_genres.jpg" width="400">
</p>
<p align="center">
   <em>Figura 7: Proporciones de genres </em>
</p>



### Archivo: 1_preprocesamiento.R

El pre-procesamiento está compuesto por las siguientes etapas:

* Carga de los espectros y su metadata correspondiente

  <p align="center">
     <img src="Imagenes/1_pre_crudo.jpeg" width="400">
   </p>
   <p align="center">
     <em>Figura 1: Espectro cargado sin transformar</em>
   </p>

* <p align="justify"> Control de calidad de los espectros mediante el uso de un estimador robusto Q. A fines prácticos, este control de calidad filtra espectros ruidosos o con el espectro "planchado" debido al fenómeno de supresión iónica en la etapa de adquisición. </p>

* <p align="justify"> Transformación de los espectros. Transformación de intensidad mediante la función raíz cuadrada (sqrt), suavizado del espectro mediante la función "wavelet", detección y remoción de la linea de base y alineamiento de los espectros, en ese orden. </p>

   <p align="center">
   <img src='Imagenes/1_pre_baseline.jpg' width='400'>
   </p>
   <p align="center">
     <em>Figura 2: Detección de la linea de base</em>
   </p>
   
   <p align="center">
   <img src='Imagenes/1_pre_baseline_removed.jpg' width='400'>
   </p>
   <p align="center">
     <em>Figura 3: Espectro con la línea de base removida</em>
   </p>

* Se realiza un promediado de las réplicas técnicas y biológicas.

* <p align="justify">Extracción de picos preponderantes de cada espectro. Esto se logra definiendo un umbral a partir del cual se comienzan a detectar los picos. Este umbral se define a partir de dos veces la relación señal a ruido del espectro (SNR).</p>

   <p align="center">
   <img src='Imagenes/1_pre_snr.jpeg' width='400'>
   </p>
   <p align="center">
     <em>Figura 4: Espectro con la detección del nivel de ruido (en rojo) y la definición del umbral (en azul)</em>
   </p>

   <p align="center">
   <img src='Imagenes/1_pre_picos.jpeg' width='400'>
   </p>
   <p align="center">
     <em>Figura 5: Detección de picos por encima del umbral establecido</em>
   </p>

* <p align="justify">A partir de la detección de los picos en cada espectro, se crea la matriz de intensidad, las cual contiene en sus filas las muestras y en las columnas los picos detectados. Esta matriz también es sujeta a transformaciones para preservar los picos con mayor frecuencia de aparición en los espectros y eliminar los picos "extraños", ya que lo que buscamos en esta instancia es que las variables (en este caso los picos) aporten información al sistema para su posterior análisis. Se crea también la matriz dicotómica, la cual se origina a partir de la definición de un umbral en la matriz de intensidades que transforma los valores de los picos en 1 y 0 segun la presencia o ausencia de cada pico en cada muestra.</p>

   <p align="center">
   <img src='Imagenes/1_pre_matriz_grafica.jpeg' width='400'>
   </p>
   <p align="center">
     <em>Figura 6: Representación gráfica de la matriz de intensidades dicotómica. Las filas corresponden a las muestras y las columnas a los picos. El color celeste indica presencia del pico en esa muestra</em>
   </p>

   
* <p align="justify">Por último, guardar las matrices y los metadatos. Se obtienen matrices de intensidades y dicotómicas tanto para las muestras individuales (matriz de 51 filas x 218 columnas) como para las réplicas biológicas (matriz de 122 filas x 218 columnas)</p>

## Seguimiento de cantidad de muestras

* Muestras iniciales o réplicas técnicas: 303
* Réplicas técnicas luego de control de calidad: 297
   * Réplicas biológicas: 122
   * Réplicas biológicas de días 2 y 4: 107
      * Muestras biológicas independientes: 55
      * Muestras biológicas independientes de días 2 y 4: 43

## Algoritmos No Supervisados

El procedimiento para la realización de los algoritmos No Supervisados fue el siguiente:
   1) Elección de conjunto de muestras (Réplicas biológicas o muestras independientes)
   2) Elección de los tiempos de muestreo (Todos los días o solo los días 2 y 4)
   3) Por medio de la matriz dicotómica, se aplica la función *bindaranking* con la cual se obtienen los picos que mejor variabilidad aportan a partir de un factor que se ingresa como variable de entrada. Este factor puede ser CLP vs SHAM, o días por ejemplo.
   4) Se realizan simulaciones de los modelos variando la cantidad de X primeros picos del análisis realizado en (3) y los algoritmos de clustering. Se realizaron pruebas con kmeans, HKmeans y PAM.
   5) Una vez realizada la clasificación No Supervisada, se comparan los puntos clasificados con su etiqueta de interés real (CLP, SHAM).

Resultados:

   ### Archivo: 2_ns_m122_d1247

   <p align="center">
   <img src='Imagenes/2_ranking_picos.jpg' width='400'>
   </p>
   <p align="center">
     <em>Figura 7: Picos mas preponderantes seleccionados por el algoritmo bindaranking a partir del factor CLP vs SHAM</em>
   </p>

   <p align="center">
   <img src='Imagenes/2_CLP_vs_SHAM_kmeans.jpg' width='400'>
   </p>
   <p align="center">
     <em>Figura 8: Clustering - CLP vs SHAM - Días 1, 2, 4 y 7 - TOP 20 picos - Algoritmo: kmeans</em>
   </p>

   <p align="center">
   <img src='Imagenes/2_tasa_acierto_total.jpg' width='400'>
   </p>
   <p align="center">
     <em>Figura 9: Tasa de acierto total</em>
   </p>

   <p align="center">
   <img src='Imagenes/2_tasa_acierto_por_dia.jpg' width='400'>
   </p>
   <p align="center">
     <em>Figura 10: Tasa de acierto por día</em>
   </p>
   
   ### Archivo: 4_ns_m122_d24

   <p align="center">
   <img src='Imagenes/4_picos_4clusters.jpeg' width='400'>
   </p>
   <p align="center">
     <em>Figura 11: Picos mas preponderantes seleccionados por el algoritmo bindaranking a partir del factor CLP_D2 vs CLP_D4 vs SHAM_D4 vs SHAM_D2</em>
   </p>

   <p align="center">
   <img src='Imagenes/4_hkmeans_4_grupos.jpg' width='400'>
   </p>
   <p align="center">
     <em>Figura 12: Clustering - CLP vs SHAM - Días 2 y 4 - TOP 30 picos - Algoritmo: Hkmeans</em>
   </p>

   <p align="center">
   <img src='Imagenes/4_kmeans_2_clusters_4_grupos.jpg' width='400'>
   </p>
   <p align="center">
     <em>Figura 12: Clustering - CLP vs SHAM - Días 2 y 4 - TOP 15 picos - Algoritmo: kmeans</em>
   </p>

   <p align="center">
   <img src='Imagenes/4_kmeans_top10.jpg' width='400'>
   </p>
   <p align="center">
     <em>Figura 13: Clustering - CLP vs SHAM - Días 2 y 4 - TOP 10 picos - Algoritmo: kmeans</em>
   </p>

   <p align="center">
   <img src='Imagenes/4_pam_2_clusters_4_grupos.jpg' width='400'>
   </p>
   <p align="center">
     <em>Figura 14: Clustering - CLP vs SHAM - Días 2 y 4 - TOP 20 picos - Algoritmo: PAM</em>
   </p>

   <p align="center">
   <img src='Imagenes/4_pam_3_clusters_4_grupos.jpg' width='400'>
   </p>
   <p align="center">
     <em>Figura 15: Clustering - CLP vs SHAM - Días 2 y 4 - 3 clusters - TOP 20 picos - Algoritmo: PAM</em>
   </p>

   <p align="center">
   <img src='Imagenes/4_pam_3_grupos_3_clusters.jpg' width='400'>
   </p>
   <p align="center">
     <em>Figura 16: Clustering - CLP vs SHAM - Días 2 y 4 - 3 clusters - TOP 30 picos - Algoritmo: PAM</em>
   </p>

   <p align="center">
   <img src='Imagenes/4_pam_top10.jpg' width='400'>
   </p>
   <p align="center">
     <em>Figura 17: Clustering - CLP vs SHAM - Días 2 y 4 - TOP 10 picos - Algoritmo: PAM</em>
   </p>
   

   ### Archivo: 5_ns_m51_d24

   <p align="center">
   <img src='Imagenes/5_picos.jpg' width='400'>
   </p>
   <p align="center">
     <em>Figura 18:  Picos mas preponderantes seleccionados por el algoritmo bindaranking a partir del factor CLP_D2 vs CLP_D4 vs SHAM</em>
   </p>

   <p align="center">
   <img src='Imagenes/5_pam_3clusters.jpg' width='400'>
   </p>
   <p align="center">
     <em>Figura 19: Clustering - CLP_D2 vs CLP_D4 vs SHAM - TOP 15 picos - 3 CLUSTERS - Algoritmo: PAM</em>
   </p>
   
   
   ### Archivo: 6_ns_m51_vs_varios

   <p align="center">
   <img src='Imagenes/6_picos_clpd2d4.jpg' width='400'>
   </p>
   <p align="center">
     <em>Figura 20: Picos mas preponderantes seleccionados por el algoritmo bindaranking a partir del factor CLP_D2 vs CLP_D4</em>
   </p>

   <p align="center">
   <img src='Imagenes/6_pam_clp_d2d4.jpg' width='400'>
   </p>
   <p align="center">
     <em>Figura 21:  Clustering - CLP_D2 vs CLP_D4 - TOP 15 picos - 2 CLUSTERS - Algoritmo: PAM</em>
   </p>

   <p align="center">
   <img src='Imagenes/6_picos_clp_sham_d2.jpg' width='400'>
   </p>
   <p align="center">
     <em>Figura 22: Picos mas preponderantes seleccionados por el algoritmo bindaranking a partir del factor CLP_D2 vs SHAM_D2</em>
   </p>

   <p align="center">
   <img src='Imagenes/6_pam_clp_sham_d2.jpg' width='400'>
   </p>
   <p align="center">
     <em>Figura 23:  Clustering - CLP_D2 vs SHAM_D2 - TOP 20 picos - 2 CLUSTERS - Algoritmo: PAM</em>
   </p>

   <p align="center">
   <img src='Imagenes/6_picos_clp_sham_d4.jpg' width='400'>
   </p>
   <p align="center">
     <em>Figura 24: Picos mas preponderantes seleccionados por el algoritmo bindaranking a partir del factor CLP_D4 vs SHAM_D4</em>
   </p>

   <p align="center">
   <img src='Imagenes/6_pam_clp_sham_d4.jpg' width='400'>
   </p>
   <p align="center">
     <em>Figura 25:  Clustering - CLP_D4 vs SHAM_D4 - TOP 15 picos - 2 CLUSTERS - Algoritmo: PAM</em>
   </p>
   
## Algoritmos Supervisados

   ### Archivo: 3_s_m122_d1247.R

   Se probaron modelos de aprendizaje supervisado con las 122 réplicas biológicas correspondiente a todos los días.
   
   1) <p align="justify">Se cargó la matriz dicotómica de 122 réplicas biológicas x 218 picos y se dividieron las muestras en grupo de entrenamiento y grupo de testeo bajo una relación de 60% entrenamiento y 40% testeo.</p>
   2) <p align="justify">Se seleccionan los 20 picos mas preponderantes mediante el algoritmo *bindaranking* bajo el factor CLP/SHAM con el propósito de reducir la cantidad de predictores.</p>
   3) Se entrenaron los siguientes modelos:
         * Binda (Binary Discriminant Analysis)
         * Random Forest
         * kNN (k nearest neighbor)
         * SVM Radial (Support Vector Machine con kernel radial)
   4) Se realizan las predicciones y a partir de ellas se generan las curvas ROC para cada modelo.

   <p align="center">
   <img src='Imagenes/3_sup_curvasROC.jpg' width='400'>
   </p>
   <p align="center">
     <em>Figura 26:  Curvas ROC para cada modelo de entrenamiento y valores de AUC (Área bajo la curva)</em>
   </p>

   ### Archivo: 7_s_m107_d24_top15.ipynb

   Se probaron modelos de aprendizaje supervisado con 107 réplicas biológicas correspondiente a los días 2 y 4.

   1) <p align="justify">Se representaron los porcentajes de muestras correspondiente a cada tipo de factor (CLP_D2, CLP_D4 y SHAM)</p>
   2) <p align="justify">Se entrenó un modelo de Regresión Logística</p>

      *Regresión Logística - accuracy score: 86%*

   <p align="center">
   <img src='Imagenes/7_matriz_confusion_reglog.JPG' width='400'>
   </p>
   <p align="center">
     <em>Figura 27:  Matriz de confusión de la Regresión Logística</em>
   </p>
   
   3) <p align="justify">Se entrenó un modelo de Random Forest</p>

      *Random Forest- accuracy score: 72% (A partir de validación cruzada con k=5)*

   <p align="center">
   <img src='Imagenes/7_picos_rf.JPG' width='400'>
   </p>
   <p align="center">
     <em>Figura 28:  Preponderancia de predictores del Random Forest</em>
   </p>

   <p align="center">
   <img src='Imagenes/7_arbol_decision.jpg' width='400'>
   </p>
   <p align="center">
     <em>Figura 29:  Arbol de decisión del Random Forest</em>
   </p>

## Conclusión
