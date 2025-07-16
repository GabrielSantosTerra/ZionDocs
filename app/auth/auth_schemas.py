from pydantic import BaseModel, EmailStr

class LoginInput(BaseModel):
    email: EmailStr
    senha: str
