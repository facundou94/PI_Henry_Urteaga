# Carga de librerías

import numpy as np
import pandas as pd
from fastapi import FastAPI
import funciones

app = FastAPI()

@app.get('/')
def home():
    return {"message": "Hello World"}

@app.get('/prueba_string')
def prueba_string(palabra: str):
    if palabra == "correcta":
        print("Palabra correcta. Esto es un print")
        return "Palabra correcta. Esto es un return"
    else:
        print("Palabra incorrecta. Esto es un print")
        return "Palabra incorrecta. Esto es un return"

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