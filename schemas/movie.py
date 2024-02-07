
from pydantic import BaseModel, Field
from typing import Optional


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
