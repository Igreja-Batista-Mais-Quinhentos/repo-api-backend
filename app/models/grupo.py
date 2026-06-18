from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Grupo(Base):
    __tablename__ = "grupos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255), nullable=False)
    descricao = Column(String(500), nullable=True)
    criado_em = Column(DateTime, server_default=func.now())

    lider_id = Column(Integer, ForeignKey("membros.id"), nullable=False)
    lider = relationship("Membro", back_populates="grupos_liderados")

    membros = relationship("GrupoMembro", back_populates="grupo")
    avisos = relationship("Aviso", back_populates="grupo")

class GrupoMembro(Base):
    __tablename__ = "grupo_membros"

    grupo_id = Column(Integer, ForeignKey("grupos.id"), primary_key=True)
    membro_id = Column(Integer, ForeignKey("membros.id"), primary_key=True)

    grupo = relationship("Grupo", back_populates="membros")
    membro = relationship("Membro", back_populates="grupos")
