from fastapi.security import HTTPBearer
from fastapi import Request, HTTPException
from jwt_manager import create_token, validate_token

class JWTBearer(HTTPBearer):
     async def __call__(self, request: Request):
          #La funcion call necesita de una
          #request. en nuestro caso el objeto
          #request
          auth =  await super().__call__(request)
     #En este return de este metodo call.
     #lo que hacemos es invocar a el
     #metodo call de la clase super o padre

     #La llamada del metodo puede tomar tiempo
     #por lo cual se le agrega un await
     # y se indica que la funcion sera asincrona

     #Guardamos datos de credenciales en la variable
     #auth
          data = validate_token(auth.credentials)
          #Validamos el token. El token
          #se encuentra en la propiedad
          #credentials (de tipo HTTPAuthorizationCredentials) de nuestro variable
          #auth

          if data["email"] != 'admin@gmail.com':
          #Si la data no coincide con la que originalmente se definio
          #se debe lanzar una exception de HTTP
               return HTTPException(status_code=403, detail="Credenciales son invalidas")
          #se puede pasar detalle del eror. 

