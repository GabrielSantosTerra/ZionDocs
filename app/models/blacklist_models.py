from sqlalchemy import Column, Integer, String, DateTime, func
from app.database.connection import Base

class BlacklistToken(Base):
    __tablename__ = "tb_blacklist"

    id = Column(Integer, primary_key=True, index=True)
    jti = Column(String, nullable=False, unique=True)
    data_insercao = Column(DateTime, default=func.now())
