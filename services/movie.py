from models.movie import Movie as MovieModel

class MovieService():
    #Modulo constructor
    def __init__(self,db) -> None:
        self.db = db
        #ya podriamos acceder a la db por medio
        #de la clase, podemos acceder a la db
        #usando otros metodos del servicio

    #cada vez que se llame a este registro.
    #osea se inicicalice, se envie una sesion
    #a la base de datos
    
    def get_movies(self):
        #metodo de clase debe tener
        #el atributo self.
        result = self.db.query(MovieModel).all()
        #self hace referencia a la
        #sesion que me esta llegando
        #en la base de datos ejecutamos
        #un query de todos los datos
        #de movieModels
        return result
    
    def get_movie(self,id):
        result = self.db.query(MovieModel).filter(MovieModel.id == id).first()
        return result
    
    def get_movies_by_category(self,category):
        result = self.db.query(MovieModel).filter(MovieModel.category == category).all()
        return result
    
    