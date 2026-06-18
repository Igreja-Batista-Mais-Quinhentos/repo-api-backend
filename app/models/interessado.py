from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from app.database import Base

class Interessado(Base):
    __tablename__ = "interessados"

    id         = Column(Integer, primary_key=True, index=True)
    nome       = Column(String(100), nullable=False)
    email      = Column(String(150), nullable=False)
    telefone   = Column(String(20))
    frequenta  = Column(String(20))
    mensagem   = Column(String(500))
    criado_em  = Column(DateTime(timezone=True), server_default=func.now())
