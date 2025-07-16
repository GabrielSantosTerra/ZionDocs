from datetime import timedelta
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from app.models.user_models import Pessoa, Usuario
from app.schemas.user_schemas import PessoaUsuarioCreate, PessoaOut
from passlib.context import CryptContext
from fastapi import APIRouter, Depends, HTTPException, Response, Request
from sqlalchemy.orm import Session
from app.database import connection
from app.models.user_models import Usuario, Pessoa
from dotenv import load_dotenv
from app.utils.token_utils import extrair_jti, adicionar_jti_na_blacklist, token_blacklist
from app.utils.auth_utils import verificar_senha, criar_access_token, verificar_token
from jose import jwt, JWTError, ExpiredSignatureError
from app.auth.auth_schemas import LoginInput
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = connection.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/registro", response_model=PessoaOut)
def criar_usuario(dados: PessoaUsuarioCreate, db: Session = Depends(get_db)):

    if db.query(Pessoa).filter_by(cpf=dados.cpf).first():
        raise HTTPException(status_code=400, detail="CPF já cadastrado.")
    if db.query(Usuario).filter_by(email=dados.email).first():
        raise HTTPException(status_code=400, detail="E-mail já cadastrado.")

    pessoa = Pessoa(nome=dados.nome, cpf=dados.cpf)
    db.add(pessoa)
    db.flush()

    senha_hash = pwd_context.hash(dados.senha)
    usuario = Usuario(id_pessoa=pessoa.id, email=dados.email, senha_hash=senha_hash)
    db.add(usuario)
    db.commit()
    db.refresh(pessoa)

    return pessoa

@router.post("/login")
def login(dados: LoginInput, response: Response, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == dados.email).first()
    if not usuario or not verificar_senha(dados.senha, usuario.senha_hash):
        raise HTTPException(status_code=401, detail="E-mail ou senha inválidos")

    payload = {"sub": str(usuario.id)}

    access_token = criar_access_token(payload, expires_delta=timedelta(minutes=60))
    refresh_token = criar_access_token(payload, expires_delta=timedelta(days=30))

    cookie_env = {
        "samesite": "lax",
        "secure": False
    }

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=60 * 60,
        path="/",
        **cookie_env
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        max_age=60 * 60 * 24 * 30,
        path="/",
        **cookie_env
    )

    response.set_cookie(
        key="logged_user",
        value="true",
        httponly=False,
        max_age=60 * 60 * 24 * 7,
        path="/",
        **cookie_env
    )

    return {"message": "Login efetuado com sucesso"}

@router.post("/logout")
def logout(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")

    if token:
        jti = extrair_jti(token)
        if jti:
            adicionar_jti_na_blacklist(jti, db)

    response = JSONResponse(content={"message": "Logout realizado com sucesso"})

    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    response.set_cookie("logged_user", "false", httponly=False)

    return response

@router.get("/me")
def get_me(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Token ausente")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        jti = payload.get("jti")

        if jti and token_blacklist(jti, db):
            raise HTTPException(status_code=401, detail="Token revogado")

        user_id = payload.get("sub")
        usuario = db.query(Usuario).filter(Usuario.id == user_id).first()

        if not usuario or not usuario.pessoa:
            raise HTTPException(status_code=404, detail="Usuário ou pessoa não encontrado")

        return {
            "nome": usuario.pessoa.nome,
            "cpf": usuario.pessoa.cpf,
            "email": usuario.email
        }

    except ExpiredSignatureError:
        jti = extrair_jti(token)
        if jti:
            adicionar_jti_na_blacklist(jti, db)
        raise HTTPException(status_code=401, detail="Token expirado")

    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")
