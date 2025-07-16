from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, declarative_base
import uuid

Base = declarative_base()

class Pessoa(Base):
    __tablename__ = "tb_pessoas"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String, nullable=False)
    cpf = Column(String, unique=True, nullable=False)

    usuario = relationship("Usuario", back_populates="pessoa", uselist=False)

class Usuario(Base):
    __tablename__ = "tb_usuarios"

    id = Column(Integer, primary_key=True, index=True)
    id_pessoa = Column(Integer, ForeignKey("tb_pessoas.id"), nullable=False)
    email = Column(String, unique=True, nullable=False)
    senha_hash = Column(String, nullable=False)

    pessoa = relationship("Pessoa", back_populates="usuario")

