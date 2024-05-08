# 1. Carga de librerías

import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors

# 2. Función PlayTimeGenre

# def PlayTimeGenre( genero : str ): Debe devolver año con mas horas jugadas para dicho género.
# Ejemplo de retorno: {"Año de lanzamiento con más horas jugadas para Género X" : 2013}

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
        df_games_genres = pd.read_parquet('df_games_genres.parquet', columns=["item_id", genero])
        df_games_tec = pd.read_parquet('df_games_tec.parquet', columns=["app_name", "item_id", "release_year"])
        df_items = pd.read_parquet('df_items.parquet', columns=["item_id", "playtime_forever"])
    except FileNotFoundError:
        return "Archivo no encontrado."
    
    # Utilizar las columnas de género como índices booleanos para filtrar más rápido
    df_genero_especifico = df_games_genres[df_games_genres[genero] == 1]
    
    # Verificar si no hay datos para el género especificado
    #if df_genero_especifico.empty:
    #   return f"No hay datos para el género '{genero}'."
    
    # Combinar los DataFrames relevantes
    merged_df = pd.merge(df_games_tec, df_genero_especifico, on='item_id', how='inner')
    merged_df = pd.merge(merged_df, df_items, on='item_id', how='inner')

    # Eliminar los DataFrames cargados una vez realizada la fusión
    del df_games_tec
    del df_games_genres
    del df_items
    
    # Agrupar por año de lanzamiento y sumar las horas jugadas
    df_horas_jugadas_por_ano = merged_df.groupby('release_year')['playtime_forever'].sum()
    
    # Encontrar el año con la mayor cantidad de horas jugadas acumuladas
    max_total_playtime_year = df_horas_jugadas_por_ano.idxmax()
    
    return f"Año de lanzamiento con más horas jugadas para Género {genero}: {max_total_playtime_year}"

# 3. Función UserForGenre

# def UserForGenre( genero : str ): Debe devolver el usuario que acumula más horas jugadas para el género dado y una lista de la acumulación de horas jugadas por año.
# Ejemplo de retorno: {"Usuario con más horas jugadas para Género X" : us213ndjss09sdf, "Horas jugadas":[{Año: 2013, Horas: 203}, {Año: 2012, Horas: 100}, {Año: 2011, Horas: 23}]}

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
        df_games_genres = df_games_genres[df_games_genres[genero] == 1]
        
        # Obtener los item_id relevantes
        relevant_item_ids = df_games_genres['item_id'].unique()
        
        # Filtrar df_items y df_games_tec
        df_items = pd.read_parquet('df_items.parquet', columns=["user_id", "item_id", "playtime_forever"])
        df_items = df_items[df_items['item_id'].isin(relevant_item_ids)]
        
        df_games_tec = pd.read_parquet('df_games_tec.parquet', columns=["item_id", "release_year"])
        df_games_tec = df_games_tec[df_games_tec['item_id'].isin(relevant_item_ids)]
        
    except FileNotFoundError:
        return "Archivo no encontrado."
    
    # Verificar si no hay datos para el género especificado
    if df_games_genres.empty:
        return f"No hay datos para el género '{genero}'."
    
    # Fusionar los DataFrames necesarios
    df_merged = pd.merge(df_items, df_games_genres[['item_id']], on='item_id', how='inner')
    del df_items, df_games_genres  # Liberar memoria
    
    df_merged = pd.merge(df_merged, df_games_tec, on='item_id', how='inner')
    del df_games_tec  # Liberar memoria
    
    # Calcula la suma total de playtime_forever para cada usuario
    suma_playtime_por_usuario = df_merged.groupby('user_id')['playtime_forever'].sum()
    
    # Encuentra el usuario con la mayor suma de playtime_forever
    usuario_max_playtime = suma_playtime_por_usuario.idxmax()
    
    # Filtra el DataFrame original para obtener solo las filas asociadas con ese usuario
    df_usuario_max_playtime = df_merged[df_merged['user_id'] == usuario_max_playtime]
    
    # Agrupa las horas jugadas por año para ese usuario
    horas_por_anio = df_usuario_max_playtime.groupby('release_year')['playtime_forever'].sum()
    
    # Construye la cadena de texto con el formato deseado
    resultado_str = (f"Usuario con más horas jugadas para Género {genero}: {usuario_max_playtime}, " +
                 "Horas jugadas: [" +
                 ", ".join([f"{{'Año': {año}, 'Horas': {horas}}}" for año, horas in horas_por_anio.items()]) +
                 "]")

    return resultado_str

# 4. Función UsersRecommend
# def UsersRecommend( año : int ): Devuelve el top 3 de juegos MÁS recomendados por usuarios para el año dado. 
# (reviews.recommend = True y comentarios positivos/neutrales)

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
    # Cargar el DataFrame desde el archivo
    sentiment_counts = pd.read_csv('sentiment_counts.csv', index_col='release_year')
    
    # Verificar si el año especificado está presente en el DataFrame
    if anio not in sentiment_counts.index:
        return "Año no encontrado en la base de datos."
    
    # Obtener la cuenta de análisis de sentimientos para el año especificado
    sentiment_counts_anio = sentiment_counts.loc[anio]
    
    resultado = f"Sentiment analysis para el año {anio}: [Negative:{sentiment_counts_anio.get(0, 0)}, Neutral:{sentiment_counts_anio.get(1, 0)}, Positive:{sentiment_counts_anio.get(2, 0)}]"

    return resultado

# 6. def recomendacion_juego( id de producto ): 
# Ingresando el id de producto, deberíamos recibir una lista con 5 juegos recomendados similares al ingresado.

def recomendacion_juego(id):
    # Carga de datos
    df_sist_reco_v4 = pd.read_parquet('df_sist_reco_v4.parquet')
    games_dummies = df_sist_reco_v4.drop(columns=['item_id', 'app_name'])
    games_id_names = df_sist_reco_v4[['item_id', 'app_name']]

    # Entrenamiento del modelo
    n_neighbors = 6
    nneighbors = NearestNeighbors(n_neighbors=n_neighbors, metric='cosine').fit(games_dummies)

    # Evaluación del juego
    index = games_dummies.index[games_id_names['item_id'] == id][0]
    game_eval = np.array(games_dummies.iloc[index]).reshape(1, -1)
    dif, ind = nneighbors.kneighbors(game_eval)

    # Construir la cadena de juegos recomendados
    juegos_recomendados_str = ("Juegos recomendados --->" +
                                " # 1: " + games_id_names.at[ind[0][1], "app_name"]  +
                                " # 2: " + games_id_names.at[ind[0][2], "app_name"]  +
                                " # 3: " + games_id_names.at[ind[0][3], "app_name"]  +
                                " # 4: " + games_id_names.at[ind[0][4], "app_name"]  +
                                " # 5: " + games_id_names.at[ind[0][5], "app_name"])

    return juegos_recomendados_str