from fastapi import FastAPI
#Path es para el uso de parametros de ruta
#Query nos permite hacer validacion de datos en los parametros query
from fastapi.responses import HTMLResponse
#importamos la clase de respuesta en HTML
from pydantic import BaseModel
from config.database import engine, Base
#importamos la session, el engine y la base 

from middlewares.error_handler import ErrorHandler
from routers.movie import movie_router
from routers.auth import auth_router

app = FastAPI()
app.title = "Mi aplicacion con FastAPI"
#Podemos setear un titulo para nuestra aplicacion
app.version = "0.0.1"
#la version debe ir entre comillas

#Fastapi tiene opcion para añadir middleware a nivel general de la app

app.add_middleware(ErrorHandler)

#Debemos llamar al router desde la aplicacion principal
app.include_router(movie_router)
app.include_router(auth_router)


Base.metadata.create_all(bind=engine)
#Llamamos a la metadata de Base. creamos todas las tablas guardadas en
#la base, hacemos referencia al motor del cual cargaremos las tablas

movies = [
        {
		"id": 1,
		"title": "Avatar",
		"overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
		"year": "2009",
		"rating": 7.8,
		"category": "Acción"
	},
            {
		"id": 2,
		"title": "Avatar",
		"overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
		"year": "2009",
		"rating": 7.8,
		"category": "Acción"
	}
]

#Creamos una lista de diccionarios.
#Cada diccionario contiene informacion de las peliculas

@app.get('/', tags=['Home']) #los tags se mandan en una lista. 
def message():
    return HTMLResponse("<h1>Hello world</h1>")

#Los tags los podemos usar para agrupar determinadas rutas en nuestra app
