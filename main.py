# Carga de librerías

import numpy as np
import pandas as pd
from fastapi import FastAPI
from funciones import PlayTimeGenre

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get('/GetPlayTimeGenre')
async def GetPlayTimeGenre(genero: str):
    try:
        resultado = PlayTimeGenre(genero)
        return resultado
    except Exception as e:
        return f"Error al procesar la solicitud: {str(e)}"
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

    datos_str = str(datos)
    
    return datos_str

@app.get('/suma_sencilla')
def suma_sencilla(primer_valor : int, segundo_valor : int):
    suma = primer_valor + segundo_valor
    return suma 

########################################################################################################################