import os
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
#Declarative base sirve para manipilar las tablas de la base de datos

sqlite_file_name = "../database.sqlite"
#Nombre base de datos

base_dir = os.path.dirname(os.path.realpath(__file__))

database_url = f'sqlite:///{os.path.join(base_dir,sqlite_file_name)}'
#sqlite:///url esta es la forma de conectarse a una base de datos
#Pasamos url de la base de datos.

engine = create_engine(database_url, echo = True)
#Motor de la base de datos. Le pasamos la base de datos.
#echo determina si al crear la base de datos, por consola nos mostrara que
#es lo que esta pasando.

Session = sessionmaker(bind=engine)
#La sesion debe ser enlazado a la basede datos.
#le pasamos el parametro bind, el cual se enlaza al motor de la base de datos

Base = declarative_base()
#