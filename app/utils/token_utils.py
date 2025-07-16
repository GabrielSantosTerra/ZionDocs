from jose import jwt, JWTError
from app.models.blacklist_models import BlacklistToken
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv # ou direto do .env

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

def extrair_jti(token: str) -> str | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("jti")
    except JWTError:
        return None

def adicionar_jti_na_blacklist(jti: str, db: Session):
    if jti:
        ja_existe = db.query(BlacklistToken).filter(BlacklistToken.jti == jti).first()
        if not ja_existe:
            db.add(BlacklistToken(jti=jti))
            db.commit()

def token_blacklist(jti: str, db: Session) -> bool:
    return db.query(BlacklistToken).filter_by(jti=jti).first() is not None