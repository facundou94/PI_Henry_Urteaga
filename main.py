

# Carga de librerías

import numpy as np
import pandas as pd
from fastapi import FastAPI
import funciones

# Carga de archivos

df_games_tec = pd.read_parquet('df_games_tec.parquet')
df_games_genres = pd.read_parquet('df_games_genres.parquet')
df_games_specs = pd.read_parquet('df_games_specs.parquet')
df_games_tags = pd.read_parquet('df_games_tags.parquet')
df_reviews_con_sa = pd.read_parquet('df_reviews_con_sa.parquet')
df_items = pd.read_parquet('df_items.parquet')

app = FastAPI()

@app.get('/developer')
def developer(developer: str):
    resultado = funciones.developer(developer)
    return resultado

@app.get('/userdata')
def userdata(user_id: str):
    resultado = funciones.userdata(user_id)
    return resultado

@app.get('/UserForGenre')
def UserForGenre(genero: str):
    resultado = funciones.UserForGenre(genero)
    return resultado

@app.get('/best_developer_year')
def best_developer_year(year: int):
    resultado = funciones.best_developer_year(year)
    return resultado

@app.get('/developer_reviews_analysis')
def developer_reviews_analysis(desarrolladora: int):
    resultado = funciones.developer_reviews_analysis(desarrolladora)
    return resultado