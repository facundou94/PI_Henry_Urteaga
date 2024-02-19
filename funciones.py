# Scripts con las funciones

#######################################################################################################################################

# Carga de librerías
import numpy as np
import pandas as pd

# Carga de archivos
df_games_tec = pd.read_parquet('df_games_tec.parquet')
df_games_genres = pd.read_parquet('df_games_genres.parquet')
df_games_specs = pd.read_parquet('df_games_specs.parquet')
df_games_tags = pd.read_parquet('df_games_tags.parquet')
df_reviews_con_sa = pd.read_parquet('df_reviews_con_sa.parquet')
df_items = pd.read_parquet('df_items.parquet')

#######################################################################################################################################

def CargarArchivos():

    df_games_tec = pd.read_parquet('df_games_tec.parquet')
    df_games_genres = pd.read_parquet('df_games_genres.parquet')
    df_games_specs = pd.read_parquet('df_games_specs.parquet')
    df_games_tags = pd.read_parquet('df_games_tags.parquet')
    df_reviews_con_sa = pd.read_parquet('df_reviews_con_sa.parquet')
    df_items = pd.read_parquet('df_items.parquet')
    
#######################################################################################################################################
     
def developer(desarrollador : str):

    CargarArchivos()

    # Paso 1: Filtra el DataFrame original
    df_func_1 = df_games_tec[['item_id', 'developer', 'release_year', 'price']]
    df_func_1_filtrado = df_func_1[df_func_1['developer'] == desarrollador]

    # Paso 2: Contar la cantidad de elementos por año y la cantidad de elementos con price = 0 para cada año
    conteo_por_anio = df_func_1_filtrado['release_year'].value_counts()
    cantidad_price_cero_por_anio = (df_func_1_filtrado['price'] == 0).groupby(df_func_1_filtrado['release_year']).sum()

    # Paso 3: Asegurarse de que ambos DataFrames tengan el mismo índice y tipo de datos para la columna de años
    conteo_por_anio = conteo_por_anio.astype(int)
    cantidad_price_cero_por_anio.index = cantidad_price_cero_por_anio.index.astype(int)

    # Paso 4: Llenar los valores faltantes con ceros
    indices_totales = set(conteo_por_anio.index) | set(cantidad_price_cero_por_anio.index)
    conteo_por_anio = conteo_por_anio.reindex(indices_totales, fill_value=0)
    cantidad_price_cero_por_anio = cantidad_price_cero_por_anio.reindex(indices_totales, fill_value=0)

    # Paso 5: Crear un nuevo DataFrame con los resultados
    df_resultado = pd.DataFrame({
        'Año de lanzamiento': conteo_por_anio.index,
        'Cantidad de items': conteo_por_anio.values,
        'Cantidad de contenido Free': cantidad_price_cero_por_anio.values,
        "Porcentaje de contenido Free (%)": cantidad_price_cero_por_anio.values
    })

    # Paso 6: Ordenar los años de mayor a menor
    df_resultado = df_resultado.sort_values(by='Año de lanzamiento', ascending=False)

    # Paso 7: Expresar como porcentaje
    for iter in (range(0, len(df_resultado))):
        df_resultado.at[iter,"Porcentaje de contenido Free (%)"] = round((df_resultado["Cantidad de contenido Free"].iloc[iter]/
                                                                    df_resultado["Cantidad de items"].iloc[iter])*100,2)
        
    df_resultado = df_resultado.drop(columns=['Cantidad de contenido Free'])
    # Mostrar el DataFrame resultado
    
    print(df_resultado)

#######################################################################################################################################

def userdata(user_id : str):

    try:
        
        CargarArchivos()

        # Obtener recomendaciones
        reco_usuario = df_reviews_con_sa[df_reviews_con_sa['user_id'] == user_id]
        reco_positiva = len(reco_usuario[reco_usuario['recommend'] == True])

        df_items_filtrado = df_items[df_items['user_id'] == user_id]

        df_func_2 = pd.merge(df_games_tec[["item_id","price"]], df_items_filtrado[["user_id","item_id"]], on='item_id', how='inner')

        # Calcula el total del dinero gastado por el usuario
        dinero_gastado = round(df_func_2['price'].sum(),2)

        # Calcula el porcentaje de recomendación del usuario
        porcentaje_recomendacion = round((reco_positiva / len(df_func_2)) * 100,2)

        # Calcula la cantidad total de items comprados por el usuario
        cantidad_items = len(df_func_2)

        # Retorna los resultados en un diccionario con el formato deseado
        resultado = {
            "Usuario": user_id,
            "Dinero gastado": f"{dinero_gastado} USD",
            "% de recomendación": f"{porcentaje_recomendacion:.2f}%",
            "Cantidad de items": cantidad_items }
        
        return resultado

    except Exception as e:
        
        return {"Error": str(e)}

    #######################################################################################################################################

    def UserForGenre(genero):

        CargarArchivos()

        # Filtro inicialmente los juegos del genero seleccionado
        df_genre = df_games_genres[df_games_genres[genre] == True]
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
            "Usuario con más horas jugadas para Género X": usuario_max_playtime,
            "Horas jugadas": [{"Año": año, "Horas": horas} for año, horas in horas_por_anio.items()]
                    }
        
        return resultado

    #######################################################################################################################################

    def best_developer_year(year : int):

        CargarArchivos()

        df_games_year = df_games_tec[df_games_tec["release_year"] == year]

        df_func_4 = pd.merge(df_games_year[["app_name",'item_id',"developer"]], df_reviews_con_sa[["item_id",'recommend','sentiment_analysis']], on='item_id', how='inner')

        # Calcular el valor de (recommend + sentiment_analysis * 0.25) para cada item_id para cada user_id
        df_func_4['score'] = df_func_4['recommend'] + df_func_4['sentiment_analysis'] * 0.25

        # Calcular el valor de (recommend + sentiment_analysis * 0.25) para cada desarrollador
        df_func_4['score'] = df_func_4['recommend'] + df_func_4['sentiment_analysis'] * 0.25

        # Agrupar por desarrolladores y obtener el top 3
        top_3_desarrolladores = df_func_4.groupby('developer')['score'].sum().nlargest(3)

        # Construir una lista de diccionarios con el formato deseado
        resultado = [{"Puesto {}: {}".format(i + 1, desarrollador[0]): desarrollador[1]} for i, desarrollador in enumerate(top_3_desarrolladores.items())]

        return resultado
    
#######################################################################################################################################

def developer_reviews_analysis(desarrolladora : str):

    CargarArchivos()
    
    # Filtrar el DataFrame por el desarrollador dado
    df_games_developer = df_games_tec[df_games_tec["developer"] == desarrolladora]

    # Realizar la fusión de DataFrames
    df_func_5 = pd.merge(df_games_developer[['item_id', "developer"]], df_reviews_con_sa[["item_id", 'sentiment_analysis']], on='item_id', how='inner')

    # Calcular el total de negativos y positivos
    total_negativos = (df_func_5['sentiment_analysis'] == 0).sum()
    total_positivos = (df_func_5['sentiment_analysis'] == 2).sum()

    # Construir el diccionario con el formato deseado
    resultado = {developer: {"Negative": total_negativos, "Positive": total_positivos}}

    return resultado

#######################################################################################################################################