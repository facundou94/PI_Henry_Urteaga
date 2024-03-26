# 1. Carga de librerías

import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors

# 2. Función PlayTimeGenre

# def PlayTimeGenre( genero : str ): Debe devolver año con mas horas jugadas para dicho género.
# Ejemplo de retorno: {"Año de lanzamiento con más horas jugadas para Género X" : 2013}

def PlayTimeGenre(genero):

    df_games_tec = pd.read_parquet('df_games_tec.parquet')
    df_games_genres = pd.read_parquet('df_games_genres.parquet')
    df_items = pd.read_parquet('df_items.parquet')

    merged_df_1 = pd.merge(df_games_tec[["app_name","item_id","release_year"]], df_games_genres, on='item_id', how='inner')
    merged_df_2 = pd.merge(merged_df_1, df_items[["item_id","playtime_forever"]], on='item_id', how='inner')

    # Lista de géneros disponibles
    generos_disponibles = ['Utilities', 'Racing', 'Massively Multiplayer', 'Sports', 'Action', 
                           'Audio Production', 'Indie', 'Web Publishing', 'RPG', 'Photo Editing', 
                           'Casual', 'Software Training', 'Animation & Modeling', 
                           'Design & Illustration', 'Simulation', 'Adventure', 'Early Access', 
                           'Video Production', 'Education', 'Accounting', 'Free to Play', 'Strategy']
    
    # Verifica si el género especificado existe en la base de datos
    if genero not in merged_df_2.columns:
        return f"No se encontró el género '{genero}' en la base de datos. Géneros disponibles: {', '.join(generos_disponibles)}"
    
    # Filtra el DataFrame por el género especificado
    df_genero_especifico = merged_df_2[merged_df_2[genero] == 1]
    
    # Verifica si no hay datos para el género especificado
    if df_genero_especifico.empty:
        return f"No hay datos para el género '{genero}'. Géneros disponibles: {', '.join(generos_disponibles)}"
    
    # Agrupar por año de lanzamiento y sumar las horas jugadas
    df_horas_jugadas_por_ano = df_genero_especifico.groupby('release_year')['playtime_forever'].sum().reset_index()
    
    # Encontrar el año con la mayor cantidad de horas jugadas acumuladas
    max_total_playtime_year = df_horas_jugadas_por_ano.loc[df_horas_jugadas_por_ano['playtime_forever'].idxmax(), 'release_year']
    
    string_return = f"{{'Año de lanzamiento con más horas jugadas para Género {genero}': {max_total_playtime_year}}}"
    return string_return

# 3. Función UserForGenre

# def UserForGenre( genero : str ): Debe devolver el usuario que acumula más horas jugadas para el género dado y una lista de la acumulación de horas jugadas por año.
# Ejemplo de retorno: {"Usuario con más horas jugadas para Género X" : us213ndjss09sdf, "Horas jugadas":[{Año: 2013, Horas: 203}, {Año: 2012, Horas: 100}, {Año: 2011, Horas: 23}]}

def UserForGenre(genero):

    df_games_genres = pd.read_parquet('df_games_genres.parquet')
    df_items = pd.read_parquet('df_items.parquet')
    df_games_tec = pd.read_parquet('df_games_tec.parquet')

    # Lista de géneros disponibles
    generos_disponibles = ['Utilities', 'Racing', 'Massively Multiplayer', 'Sports', 'Action', 
                           'Audio Production', 'Indie', 'Web Publishing', 'RPG', 'Photo Editing', 
                           'Casual', 'Software Training', 'Animation & Modeling', 
                           'Design & Illustration', 'Simulation', 'Adventure', 'Early Access', 
                           'Video Production', 'Education', 'Accounting', 'Free to Play', 'Strategy']
    
    
    # Verificar si el género especificado existe en el DataFrame df_games_genres
    if genero not in df_games_genres.columns:
        return f"No se encontró el género '{genero}' en la base de datos. Géneros disponibles: {', '.join(generos_disponibles)}"
    
    # Filtro inicialmente los juegos del genero seleccionado
    df_genre = df_games_genres[df_games_genres[genero] == True]
    
    # Filtro solo jugadores que hayan jugado juegos de este género
    df_func_3_aux = pd.merge(df_items[["user_id","item_id",'playtime_forever']], df_genre[["item_id"]], on='item_id', how='inner')
    df_func_3 = pd.merge(df_func_3_aux, df_games_tec[["item_id",'release_year']], on='item_id', how='inner')

    # Calcula la suma total de playtime_forever para cada usuario
    suma_playtime_por_usuario = df_func_3.groupby('user_id')['playtime_forever'].sum()

    # Encuentra el usuario con la mayor suma de playtime_forever
    usuario_max_playtime = suma_playtime_por_usuario.idxmax()

    # Filtra el DataFrame original para obtener solo las filas asociadas con ese usuario
    df_usuario_max_playtime = df_func_3[df_func_3['user_id'] == usuario_max_playtime]

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
    top_3_juegos = recomendados_por_juego.nlargest(3, 'recommend')
    
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