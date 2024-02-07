from starlette.middleware.base import BaseHTTPMiddleware, DispatchFunction, RequestResponseEndpoint
from fastapi import FastAPI , Request , Response
from fastapi.responses import JSONResponse

class ErrorHandler(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI) -> None:
        super().__init__(app)
        #inicializa la clase padre (super())

        #La inicializacion requiere de una aplicacion
        #en este caso de tipo FASTAPI.

    async def dispatch(self, request: Request, call_next) -> Response | JSONResponse:
        try:
            return await call_next(request) #retorna una llamada en caso 
            #de que no haya ningun error, esta funciona debe tener
            #el prefijo await, ya que es una funciona asincrona.
        except Exception as e: #Si atrapa una excepcion la traemos como e
            return JSONResponse(status_code=500, content={"error": str(e)})


    
    #crearemos un metodo dispatch asincrono.
    #Se requiere parametro request o a todas la peticiones que llegaran

    #call_next representa a la siguiente llamada.

    #la respuesta del metodo puede ser tanto un Response como un
    #JSONResponde.
