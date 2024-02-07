from fastapi import APIRouter
from fastapi import Path, Query, Depends
#Path es para el uso de parametros de ruta
#Query nos permite hacer validacion de datos en los parametros query
from fastapi.responses import JSONResponse
#importamos la clase de respuesta en HTML
from pydantic import BaseModel, Field
from typing import Optional, List
from config.database import Session
#importamos la session, el engine y la base 
from models.movie import Movie as MovieModel #No queremos confundir nombres==
#improtamos el modelo movie 
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer
from services.movie import MovieService
movie_router = APIRouter() #Es como crear una aplicacion
#pero a nivel de router.


#Tomamos todas las rutas que tengan que ver con movie.
#Cambiariamos el decorador @app por @movie_router, en cada ruta


#Esquema de peliculas
class Movie(BaseModel):
     #Clase Field permite validacion de datos
     id: Optional[int] = None #Seria un entero pero tambien puede no existir y por
     # puede no existir y por defecto no existira
     #Opcional de tipo entero
     title: str = Field(min_length=5 ,max_length=15) 
     #Valor por default
     #Minimo 5 digitos
     #Maximo 15 digitos
     overview: str = Field(min_length=15 ,max_length=50) 
     year: int = Field(le=2022)
     #Menor a un integer 2022  
     rating: float = Field(ge=0,le=10)
     category: str = Field(min_length=4 ,max_length=25)
     #Podemos eliminar el campo por defecto 
     #en la definicion de la clase y ponerlo 
     #en otro lugar
     class Config:
          json_schema_extra = {
               "example" :
               {
                    "id": 1,
                    "title": "Mi película",
                    "overview": "Descripción de la pelicula",
                    "year": 2022,
                    "rating":9.8,
                    "category": "Acción",
                    }
                    }

     #Diccionario de atrbutos
     #Se crea un esquema de ejemplo con los valores por defecto
     #Para ser precargados en el body



@movie_router.get('/movies', tags=["Movies"], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    db = Session()
    #result = db.query(MovieModel).all() 
    #metodo para hacer querys, como parametro le pasamos la tabla que queremos consultar
    #Con .all() indicamos que queremos todos los datos de la tabla

    result = MovieService(db).get_movies()
    #llamamos al servicio (clase) Movie Service y le pasamos el db para inicializarlo
    #con el objeto ejecutamos el metodo get_movies


    #Funcion obtener peliculas
    return JSONResponse(status_code=200,content=jsonable_encoder(result))

#Error al intentar return JSONResponse(status_code=200,content=result)
#Puesto que lo que se entrega es un contenido pero de tipo MovieModel
#Dememos convertir esta clase la cual es el resultado de consulta a
# un objeto.
#Utilizaremos un jsonable encoder

#Usar parametros de funcion.
@movie_router.get('/movies/{id}', tags=['Movies'],  response_model=Movie,status_code=200, dependencies=[Depends(JWTBearer())])
def get_movie(id: int = Path(ge=1,le=2000)) -> Movie:
    #db = Session()
    db = Session()
    #result = db.query(MovieModel).filter(MovieModel.id == id).first()
     #Metodo para filtrar
     #Se le pasa condicion para realizar la busqueda
    #nuestra condicion es que revise los atributos id
    #de cada registro y lo compare con nuestro parametro 
    #de ruta, ademas solo debe tomar el primero que
    #match .first()
    
    result = MovieService(db).get_movie(id)
    if not result:
         return JSONResponse(status_code=404,content={"message": "No encontrado"})
         
    return JSONResponse(status_code=200,content=jsonable_encoder(result))

    #Con Path podemos agregar constrains a 
    #nuestros parametros de tura
    #for item in movies:
     #     if item['id'] == id:
     #           return JSONResponse(status_code=200,content=item)
    #return JSONResponse(status_code=404,content=[])
                  
@movie_router.get('/movies/', tags=['Movies'],response_model=List[Movie],status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies_by_category(category: str = Query(min_length=4,max_length=25)) -> List[Movie]:
           
            db = Session()
            #result = db.query(MovieModel).filter(MovieModel.category == category).all()
            #all para traer todos lo valores

            result = MovieService(db).get_movies_by_category(category)

            if not result:
                 return JSONResponse(status_code=404,content={"message": "Categoria no encontrada"})
            
            return JSONResponse(status_code=200,content=jsonable_encoder(result))      
      
         #Otra solucion:
         #return [item for item in movies if item['category'] == category]
         #data = []
          #Cuando se indican a la Api que necesitamos de un parametros
          #y no lo especifico en la ruta. automaticamente la api lo
          #toma como un parametros query
         #for item in movies:
          #if item['category'] == category:
           #    data.append(item)
          #if data == []:
          #     return JSONResponse(status_code=404,content=data) 
         #return JSONResponse(status_code=200,content=data) 
     #Este parametro query es requerido, esta info puede verse en la documentacion

#Notamos que las ultimas dos rutas especificadas son muy diferentes

@movie_router.post('/movies', tags=['Movies'], response_model=dict,status_code=201)
#Si se pasan parametros a la funcion, ya sea querys o de ruta seran requeridos por la funcion.
# Con = Body() indicamos que pertenece al contenido de la peticion

def create_movie(movie: Movie) -> dict:
     db = Session() #Creamos un db que es instancia de session
     new_movie = MovieModel(**movie.dict())
     #Podemos mejor indicar pasar movie en forma de diccionario
     #indicamos con ** que se trata de un parametro y que extraeremos sus atributos

     db.add(new_movie)
     db.commit()
     #Agregamos la nueva pelicula a la base de datos


     #Ya no pedimos el objeto como parametro, sino un objeto que contenga cada uno de los valores
     #movies.append(movie)
     return JSONResponse(status_code=201,content={"message": "Se ha registrado la película"})
#En la documentacion podemos cambiar el contenido del body al presionar 
#el boton "Try it out"

@movie_router.put('/movies/{id}', tags=["Movies"],response_model=dict, dependencies=[Depends(JWTBearer())])
def update_movies(id: int, movie: Movie) -> dict: #El id si es necesario
     db = Session()
     result = db.query(MovieModel).filter(MovieModel.id == id).first()
     #Solo queremos uno

     if not result:
          return JSONResponse(status_code=404,content={"message": "No encontrado"})
     
     #Modificacion de datos

     result.title = movie.title
     result.overview = movie.overview
     result.year = movie.year
     result.rating = movie.rating
     result.category = movie.category

     db.commit()
     return JSONResponse(content={"message": "Se ha modificado la película"})

    
#     for item in movies:
#          if item['id'] == id:
#                item['title'] = movie.title
#                item['overview'] = movie.overview
#                item['year'] = movie.year
#                item['rating'] = movie.rating
#                item['category'] = movie.category
#                return JSONResponse(content={"message': 'Se ha modificado la película"})

@movie_router.delete('/movies/{id}', tags=["Movies"],response_model=dict,status_code=200,dependencies=[Depends(JWTBearer())])
def delete_movie(id: int) -> dict:

     db = Session()
     result = db.query(MovieModel).filter(MovieModel.id == id).first
     #Solo queremos uno


     if not result:
          return JSONResponse(status_code=404,content={"message": "No encontrado"})
     
     db.delete(result)
     db.commit()

     return JSONResponse(status_code=200, content={"message": "Se ha eliminado película"})
     #for item in movies:
      #    if item['id'] == id:
       #         movies.remove(item)
        #        return JSONResponse(status_code=200, content={"message': 'Se ha eliminado película"})

#Creacion de esquemas
#Todos los datos se estan añadiendo como parametros de la funcion
#En nuestra request Put por ejemplo, esto no es recomendable por que podriamos  querer
#Añadir mas datos de nuestros objetos