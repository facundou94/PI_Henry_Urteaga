# 1. Carga de librerías

import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors

# 2. Función PlayTimeGenre

# def PlayTimeGenre( genero : str ): Debe devolver año con mas horas jugadas para dicho género.
# Ejemplo de retorno: {"Año de lanzamiento con más horas jugadas para Género X" : 2013}

# OPTIMIZACIÓN HECHA:
    # Carga de datos selectiva: Cargar solo las columnas necesarias de los archivos parquet para reducir el tiempo de carga y el uso de memoria.
    # Utilizar columnas de género como índices booleanos: Convertir las columnas de género en índices booleanos para evitar iterar sobre todas las columnas cada vez que se llama a la función.
    # Uso de métodos integrados de pandas: Utilizar los métodos integrados de pandas para calcular sumas y encontrar el año con la mayor cantidad de horas jugadas.

def PlayTimeGenre(genero):
    
    # Lista de géneros disponibles
    generos_disponibles = ['Utilities', 'Racing', 'Massively Multiplayer', 'Sports', 'Action', 
                           'Audio Production', 'Indie', 'Web Publishing', 'RPG', 'Photo Editing', 
                           'Casual', 'Software Training', 'Animation & Modeling', 
                           'Design & Illustration', 'Simulation', 'Adventure', 'Early Access', 
                           'Video Production', 'Education', 'Accounting', 'Free to Play', 'Strategy']
    
    
    # Verificar si el género especificado existe en el DataFrame df_games_genres
    if genero not in generos_disponibles:
        return f"No se encontró el género '{genero}' en la base de datos. Géneros disponibles: {', '.join(generos_disponibles)}"
    
    try:
        # Cargar solo las columnas necesarias de los archivos parquet
        df_games_tec = pd.read_parquet('df_games_tec.parquet', columns=["app_name", "item_id", "release_year"])
        df_games_genres = pd.read_parquet('df_games_genres.parquet', columns=["item_id", genero])
        df_items = pd.read_parquet('df_items.parquet', columns=["item_id", "playtime_forever"])
    except FileNotFoundError:
        return "Archivo no encontrado."
    
    # Utilizar las columnas de género como índices booleanos para filtrar más rápido
    df_genero_especifico = df_games_genres[df_games_genres[genero] == 1]
    
    # Verificar si no hay datos para el género especificado
    if df_genero_especifico.empty:
        return f"No hay datos para el género '{genero}'."
    
    # Combinar los DataFrames relevantes
    merged_df = pd.merge(df_games_tec, df_genero_especifico, on='item_id', how='inner')
    merged_df = pd.merge(merged_df, df_items, on='item_id', how='inner')
    
    # Agrupar por año de lanzamiento y sumar las horas jugadas
    df_horas_jugadas_por_ano = merged_df.groupby('release_year')['playtime_forever'].sum()
    
    # Encontrar el año con la mayor cantidad de horas jugadas acumuladas
    max_total_playtime_year = df_horas_jugadas_por_ano.idxmax()
    
    return f"Año de lanzamiento con más horas jugadas para Género {genero}: {max_total_playtime_year}"

# 3. Función UserForGenre

# def UserForGenre( genero : str ): Debe devolver el usuario que acumula más horas jugadas para el género dado y una lista de la acumulación de horas jugadas por año.
# Ejemplo de retorno: {"Usuario con más horas jugadas para Género X" : us213ndjss09sdf, "Horas jugadas":[{Año: 2013, Horas: 203}, {Año: 2012, Horas: 100}, {Año: 2011, Horas: 23}]}

# OPTIMIZACIÓN HECHA:
    # Carga selectiva de datos: Cargar solo las columnas necesarias de los archivos parquet.
    # Utilización eficiente de la unión de DataFrames: Minimizar la cantidad de uniones redundantes y fusionar los DataFrames solo cuando sea necesario.
    # Uso de métodos integrados de pandas: Utilizar los métodos de pandas para realizar cálculos y operaciones de agrupación de manera más eficiente.

def UserForGenre(genero):
    
    # Lista de géneros disponibles
    generos_disponibles = ['Utilities', 'Racing', 'Massively Multiplayer', 'Sports', 'Action', 
                           'Audio Production', 'Indie', 'Web Publishing', 'RPG', 'Photo Editing', 
                           'Casual', 'Software Training', 'Animation & Modeling', 
                           'Design & Illustration', 'Simulation', 'Adventure', 'Early Access', 
                           'Video Production', 'Education', 'Accounting', 'Free to Play', 'Strategy']
    
    # Verificar si el género especificado existe en la base de datos
    if genero not in generos_disponibles:
        return f"No se encontró el género '{genero}' en la base de datos. Géneros disponibles: {', '.join(generos_disponibles)}"
    
    try:
        # Cargar solo las columnas necesarias de los archivos parquet
        df_games_genres = pd.read_parquet('df_games_genres.parquet', columns=["item_id", genero])
        df_items = pd.read_parquet('df_items.parquet', columns=["user_id", "item_id", "playtime_forever"])
        df_games_tec = pd.read_parquet('df_games_tec.parquet', columns=["item_id", "release_year"])
    except FileNotFoundError:
        return "Archivo no encontrado."
    
    # Filtro inicialmente los juegos del género seleccionado
    df_genre = df_games_genres[df_games_genres[genero]]
    
    # Verificar si no hay datos para el género especificado
    if df_genre.empty:
        return f"No hay datos para el género '{genero}'."
    
    # Fusionar los DataFrames necesarios
    df_merged = pd.merge(df_items, df_genre[['item_id']], on='item_id', how='inner')
    df_merged = pd.merge(df_merged, df_games_tec, on='item_id', how='inner')
    
    # Calcula la suma total de playtime_forever para cada usuario
    suma_playtime_por_usuario = df_merged.groupby('user_id')['playtime_forever'].sum()
    
    # Encuentra el usuario con la mayor suma de playtime_forever
    usuario_max_playtime = suma_playtime_por_usuario.idxmax()
    
    # Filtra el DataFrame original para obtener solo las filas asociadas con ese usuario
    df_usuario_max_playtime = df_merged[df_merged['user_id'] == usuario_max_playtime]
    
    # Agrupa las horas jugadas por año para ese usuario
    horas_por_anio = df_usuario_max_playtime.groupby('release_year')['playtime_forever'].sum()
    
    # Construye el diccionario con el formato deseado
    resultado = {
        f"Usuario con más horas jugadas para Género {genero}": usuario_max_playtime,
        "Horas jugadas": [{"Año": año, "Horas": horas} for año, horas in horas_por_anio.items()]
    }
    
    return resultado

# 4. Función UsersRecommend
# def UsersRecommend( año : int ): Devuelve el top 3 de juegos MÁS recomendados por usuarios para el año dado. 
# (reviews.recommend = True y comentarios positivos/neutrales)

# OPTIMIZACIÓN HECHA:
    # Carga de datos optimizada: Solo se cargan las columnas necesarias de los archivos parquet para reducir el tiempo de carga y la memoria utilizada.
    # Manejo de excepciones mejorado: Se añadió un manejo de excepciones para manejar el caso en que los archivos parquet no sean encontrados.
    # Optimización de conteo de valores: Se utilizó value_counts() en lugar de groupby para contar las no recomendaciones por juego, lo que es más eficiente.

def UsersRecommend(anio):
    try:
        # Cargar solo las columnas necesarias de los archivos parquet
        df_games_tec = pd.read_parquet('df_games_tec.parquet', columns=["item_id", "app_name", "release_year"])
        df_reviews_con_sa = pd.read_parquet('df_reviews_con_sa.parquet', columns=["item_id", "recommend", "sentiment_analysis"])
    except FileNotFoundError:
        return "Archivo no encontrado."
    
    # Filtrar solo las reseñas del año especificado
    df_reviews_juegos = df_reviews_con_sa.merge(df_games_tec, on='item_id', how='inner')
    df_anio = df_reviews_juegos[df_reviews_juegos['release_year'] == anio]
    
    # Verificar si hay datos para el año especificado
    if df_anio.empty:
        return "No hay reseñas para el año especificado."
    
    # Filtrar solo las reseñas con recomendación positiva o neutral
    df_recomendados = df_anio[(df_anio['recommend']) & (df_anio['sentiment_analysis'].isin([1, 2]))]
    
    # Contar las recomendaciones por juego
    recomendados_por_juego = df_recomendados['app_name'].value_counts().reset_index()
    recomendados_por_juego.columns = ['app_name', 'recommend_count']
    
    # Ordenar los juegos por la cantidad de recomendaciones y obtener el top 3
    top_3_juegos = recomendados_por_juego.nlargest(3, 'recommend_count')
    
    # Formatear el resultado en el formato de cadena de caracteres requerido
    resultado = [{"Puesto " + str(i+1): juego} for i, juego in enumerate(top_3_juegos['app_name'])]
    
    return resultado

# 4. Función UsersNotRecommend
# def UsersNotRecommend( año : int ): Devuelve el top 3 de juegos MENOS recomendados por usuarios para el año dado. 
# (reviews.recommend = False y comentarios negativos)

# OPTIMIZACIÓN HECHA:
    # Carga de datos optimizada: Solo se cargan las columnas necesarias de los archivos parquet para reducir el tiempo de carga y la memoria utilizada.
    # Manejo de excepciones mejorado: Se añadió un manejo de excepciones para manejar el caso en que los archivos parquet no sean encontrados.
    # Optimización de conteo de valores: Se utilizó value_counts() en lugar de groupby para contar las no recomendaciones por juego, lo que es más eficiente.

def UsersNotRecommend(anio):
    try:
        # Cargar solo las columnas necesarias de los archivos parquet
        df_games_tec = pd.read_parquet('df_games_tec.parquet', columns=["item_id", "app_name", "release_year"])
        df_reviews_con_sa = pd.read_parquet('df_reviews_con_sa.parquet', columns=["item_id", "recommend", "sentiment_analysis"])
    except FileNotFoundError:
        return "Archivo no encontrado."
    
    # Filtrar solo las reseñas del año especificado
    df_reviews_juegos = df_reviews_con_sa.merge(df_games_tec, on='item_id', how='inner')
    df_anio = df_reviews_juegos[df_reviews_juegos['release_year'] == anio]
    
    # Verificar si hay datos para el año especificado
    if df_anio.empty:
        return "No hay reseñas para el año especificado."
    
    # Filtrar solo las reseñas con recomendación negativa y sentimiento neutro
    df_no_recomendados = df_anio[(~df_anio['recommend']) & (df_anio['sentiment_analysis'] == 0)]
    
    # Contar las no recomendaciones por juego
    no_recomendados_por_juego = df_no_recomendados['app_name'].value_counts().reset_index()
    no_recomendados_por_juego.columns = ['app_name', 'recommend_count']
    
    # Obtener el top 3 de juegos con más no recomendaciones
    top_3_juegos = no_recomendados_por_juego.nlargest(3, 'recommend_count')
    
    # Formatear el resultado en el formato de lista de diccionarios
    resultado = [{"Puesto " + str(i+1): juego} for i, juego in enumerate(top_3_juegos['app_name'])]
    
    return resultado

# 5. Función Sentiment_Analysis
# def sentiment_analysis( año : int ): Según el año de lanzamiento, se devuelve una lista con la cantidad de registros 
# de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento.

def sentiment_analysis(anio):

    df_games_tec = pd.read_parquet('df_games_tec.parquet')
    df_reviews_con_sa = pd.read_parquet('df_reviews_con_sa.parquet')

    df_reviews_juegos = pd.merge(df_reviews_con_sa[['item_id', 'recommend','sentiment_analysis']], 
                             df_games_tec[["item_id","app_name","release_year"]], on='item_id', how='inner')
    
    # Verificar si el año especificado está presente en el DataFrame
    if anio not in df_reviews_juegos['release_year'].unique():
        return "Año no encontrado en la base de datos."
    
    # Filtrar el DataFrame por el año especificado
    df_anio = df_reviews_juegos[df_reviews_juegos['release_year'] == anio]
    
    # Contar la cantidad de registros para cada categoría de análisis de sentimiento
    conteo_sentimientos = df_anio['sentiment_analysis'].value_counts()
    
    # Formatear el resultado en el formato requerido
    resultado = {
        "Negative": conteo_sentimientos.get(0, 0),
        "Neutral": conteo_sentimientos.get(1, 0),
        "Positive": conteo_sentimientos.get(2, 0)
    }
    
    return resultado

# 6. def recomendacion_juego( id de producto ): 
# Ingresando el id de producto, deberíamos recibir una lista con 5 juegos recomendados similares al ingresado.

def recomendacion_juego(item_id):

    from sklearn.neighbors import NearestNeighbors
    
    df_sist_reco_v4 = pd.read_parquet('df_sist_reco_v4.parquet')

    games_dummies = df_sist_reco_v4.drop(columns=['item_id', 'app_name'])

    n_neighbors=6
    nneighbors = NearestNeighbors(n_neighbors = n_neighbors, metric = 'cosine').fit(games_dummies)

    # Extraer los vectores de características del juego seleccionado
    game_eval = np.array(games_dummies.loc[item_id]).reshape(1, -1)
    
    # Obtener los índices de los juegos más similares
    dif, ind = nneighbors.kneighbors(game_eval)
    
    # Lista para almacenar los juegos recomendados en formato string
    juegos_recomendados = []
    
    # Juego seleccionado
    juego_seleccionado = {"Juego Seleccionado": df_sist_reco_v4.loc[ind[0][0], 'app_name']}
    juegos_recomendados.append(juego_seleccionado)
    
    # Juegos recomendados
    for i in range(1, 6):  # Tomamos los 5 juegos recomendados
        juego_recomendado = {"Juego Recomendado " + str(i): df_sist_reco_v4.loc[ind[0][i], 'app_name']}
        juegos_recomendados.append(juego_recomendado)
    
    return juegos_recomendados

# 76561198079601835