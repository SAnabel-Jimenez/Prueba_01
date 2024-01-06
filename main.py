# Ya está listo para poder codear las APIs con Fastapi
# Se usará el framework FastAPI 

#================================== Librerías ===================================================
# Importar librerias
from fastapi import FastAPI # Importa la clase FastAPI del modulo fastapi
import pandas as pd 
from functions import PlayTimeGenre,UserForGenre,UsersRecommend,UsersWorstDeveloper,sentiment_analysis

# Se crea una instancia llamada app
app = FastAPI() # Se crea la aplicacion

#http://127.0.0.1:8000   #borrar esta linea

# Se crea las definiciones de los métodos
# Define un decorador de operaciones de ruta
@app.get("/") 
async def index():
    return {"Proyecto": "PI - Machine Learning Operations (MLOps)"}

#=================================== ENDPOINTS ===================================================
# ENDPOINT 1
@app.get("/PlayTimeGenre/{genero}") # Parametro:genero
def Endpoint1_PlayTimeGenre(genero: str):
    result = PlayTimeGenre(genero)

    return result


# ENDPOINT 2
@app.get("/UserForGenre/{genero}") # Parametro:genero
def Endpoint2_UserForGenre(genero: str):
    result = UserForGenre(genero)

    return result



# ENDPOINT 3
@app.get("/UsersRecommend/{year}") # Parametro:genero
def Endpoint3_UsersRecommend(year: int):
    result = UsersRecommend(year)

    return result


# ENDPOINT 4
@app.get("/UsersWorstDeveloper/{year}") # Parametro:genero
def Endpoint4_UsersWorstDeveloper(year: int):
    result = UsersWorstDeveloper(year)

    return result


# ENDPOINT 5
@app.get("/sentiment_analysis/{empresa_desarrolladora}") # Parametro:genero
def Endpoint5_sentiment_analysis(empresa_desarrolladora: str):
    result = sentiment_analysis(empresa_desarrolladora)

    return result
