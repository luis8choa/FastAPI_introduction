from config.database import Base
from sqlalchemy import Column, Integer, String, Float
#Clase column para definir cada columna

class Movie(Base):
    #Nombre de la tabla
    __tablename__ = "movies"

    #Campos de mi tabla

    id = Column(Integer, primary_key=True)
    #tipo entero, llave primaria
    title = Column(String)
    overview = Column(String)
    year = Column(Integer)
    rating = Column(Float)
    category = Column(String)

