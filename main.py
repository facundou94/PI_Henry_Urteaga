# Carga de librerías

import numpy as np
import pandas as pd
from fastapi import FastAPI
#import funciones

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

# @app.get('/userdata')
# def userdata(user_id: str):
#     try:
#         resultado = userdata2(user_id)
#         return resultado
    
#     except Exception as e:
#         return {"Error": str(e)}

# @app.get('/developer')
# def developer(developer: str):
#     resultado = funciones.developer(developer)
#     return resultado

# @app.get('/UserForGenre')
# def UserForGenre(genero: str):
#     resultado = funciones.UserForGenre(genero)
#     return resultado

# @app.get('/best_developer_year')
# def best_developer_year(year: int):
#     resultado = funciones.best_developer_year(year)
#     return resultado

# @app.get('/developer_reviews_analysis')
# def developer_reviews_analysis(desarrolladora: int):
#     resultado = funciones.developer_reviews_analysis(desarrolladora)
#     return resultado

@app.get('/probar_librerias')
def probar_librerias():
    datos = {
    'Nombre': ['Juan', np.nan, 'Pedro', 'Ana'],
    'Edad': [np.nan, 30, 35, 40],
    }
    creacion = pd.DataFrame(datos)
    return creacion

@app.get('/suma_sencilla')
def suma_sencilla(primer_valor : int, segundo_valor : int):
    lista = [primer_valor, segundo_valor]
    suma = np.sum(lista)
    return suma 

########################################################################################################################

# def userdata2(user_id : str):

#         df_games_tec = pd.read_parquet('df_games_tec.parquet')
#         df_games_genres = pd.read_parquet('df_games_genres.parquet')
#         df_games_specs = pd.read_parquet('df_games_specs.parquet')
#         df_games_tags = pd.read_parquet('df_games_tags.parquet')
#         df_reviews_con_sa = pd.read_parquet('df_reviews_con_sa.parquet')
#         df_items = pd.read_parquet('df_items.parquet')

#         # Obtener recomendaciones
#         reco_usuario = df_reviews_con_sa[df_reviews_con_sa['user_id'] == user_id]
#         reco_positiva = len(reco_usuario[reco_usuario['recommend'] == True])

#         df_items_filtrado = df_items[df_items['user_id'] == user_id]

#         df_func_2 = pd.merge(df_games_tec[["item_id","price"]], df_items_filtrado[["user_id","item_id"]], on='item_id', how='inner')

#         # Calcula el total del dinero gastado por el usuario
#         dinero_gastado = round(df_func_2['price'].sum(),2)

#         # Calcula el porcentaje de recomendación del usuario
#         porcentaje_recomendacion = round((reco_positiva / len(df_func_2)) * 100,2)

#         # Calcula la cantidad total de items comprados por el usuario
#         cantidad_items = len(df_func_2)

#         # Retorna los resultados en un diccionario con el formato deseado
#         resultado = {
#             "Usuario": user_id,
#             "Dinero gastado": f"{dinero_gastado} USD",
#             "% de recomendación": f"{porcentaje_recomendacion:.2f}%",
#             "Cantidad de items": cantidad_items }
        
#         return resultado