# Carga de librerías

import numpy as np
import pandas as pd
from fastapi import FastAPI
import funciones

app = FastAPI()

@app.get('/GetPlayTimeGenre')
def GetPlayTimeGenre(genero: str):
     resultado = funciones.PlayTimeGenre(genero)
     return resultado

@app.get('/GetUserForGenre')
def GetUserForGenre(genero: str):
     resultado = funciones.UserForGenre(genero)
     return resultado

@app.get('/GetUsersRecommend')
def GetUsersRecommend(anio: int):
    resultado = funciones.UsersRecommend(anio)
    return resultado

@app.get('/GetUsersNotRecommend')
def GetUsersNotRecommend(anio: int):
    resultado = funciones.UsersNotRecommend(anio)
    return resultado

@app.get('/GetSentimentAnalysis')
def GetSentimentAnalysis(anio: int):
    resultado = funciones.sentiment_analysis(anio)
    return resultado

@app.get('/recomendacion_juego')
def recomendacion_juego(item_id: str):
    resultado = funciones.recomendacion_juego(item_id)
    return resultado


########################################################################################################################