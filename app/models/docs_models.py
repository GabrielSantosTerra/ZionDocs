from sqlalchemy import Column, Integer, String, DateTime, func
from app.database.connection import Base

class Documento(Base):
    __tablename__ = "tb_documentos"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String, unique=True, nullable=False)
    id_cliente = Column(Integer, nullable=False)
    tag = Column(String, nullable=True)
    s3_key = Column(String, nullable=False)
    url = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
