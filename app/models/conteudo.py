from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from app.database import Base

class Ministerio(Base):
    __tablename__ = "ministerios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255), nullable=False)
    tag = Column(String(100), nullable=False)
    descricao = Column(Text, nullable=False)
    lider = Column(String(255), nullable=True)
    quando = Column(String(255), nullable=True)
    foto_url = Column(String(500), nullable=True)
    ativo = Column(Boolean, default=True)
    criado_em = Column(DateTime, server_default=func.now())

class Noticia(Base):
    __tablename__ = "noticias"

    id = Column(Integer, primary_key=True, autoincrement=True)
    categoria = Column(String(100), nullable=False)
    titulo = Column(String(255), nullable=False)
    resumo = Column(String(500), nullable=True)
    corpo = Column(Text, nullable=False)
    foto_url = Column(String(500), nullable=True)
    ativo = Column(Boolean, default=True)
    publicado_em = Column(DateTime, server_default=func.now())

    autor_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
