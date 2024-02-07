from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field

class User(BaseModel):
     #Objeto de usuario para autenticacion
     email: EmailStr = Field(...)
     password: str
