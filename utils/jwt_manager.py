from jwt import encode, decode

def create_token(data: dict):
    token: str = encode(payload=data, key="my_secret_key", algorithm='HS256')
    #payLoad es el contenido
    #que voy a convertir al token

    #Creamos una clave de tipo string
    #Cualquiera que queramos

    #Algoritmo de encriptacion
    return token

def validate_token(token: str) -> dict:
    #Funcion para devolver token
    data: dict = decode(token, key="my_secret_key", algorithms=['HS256'])
    #Para la funcion decode, el parametro algorithms
    #debe ser una lista.

    #El objeto obtenido por el decode,
    #es un diccionario
    return data
