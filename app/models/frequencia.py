from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Frequencia(Base):
    __tablename__ = "frequencias"

    id = Column(Integer, primary_key=True, autoincrement=True)
    presente = Column(Boolean, default=True)
    registrado_em = Column(DateTime, server_default=func.now())

    membro_id = Column(Integer, ForeignKey("membros.id"), nullable=False)
    evento_id = Column(Integer, ForeignKey("eventos.id"), nullable=False)

    membro = relationship("Membro", back_populates="frequencias")
    evento = relationship("Evento", back_populates="frequencias")
