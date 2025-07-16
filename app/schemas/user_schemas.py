from pydantic import BaseModel, EmailStr, Field

class PessoaBase(BaseModel):
    nome: str
    cpf: str = Field(..., min_length=11, max_length=14)

class UsuarioBase(BaseModel):
    email: EmailStr
    senha: str

class PessoaUsuarioCreate(PessoaBase, UsuarioBase):
    pass

class UsuarioOut(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True

class PessoaOut(BaseModel):
    id: int
    nome: str
    cpf: str
    usuario: UsuarioOut

    class Config:
        from_attributes = True
