import enum
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Papel(str, enum.Enum):
    PASTOR = "PASTOR"
    LIDER = "LIDER"
    TESOUREIRO = "TESOUREIRO"
    MEMBRO = "MEMBRO"

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    senha_hash = Column(String(255), nullable=False)
    papel = Column(Enum(Papel), default=Papel.MEMBRO, nullable=False)
    ativo = Column(Boolean, default=True)
    criado_em = Column(DateTime, server_default=func.now())
    ultimo_acesso = Column(DateTime, nullable=True)

    membro = relationship("Membro", back_populates="usuario", uselist=False)
    avisos = relationship("Aviso", back_populates="autor")
    eventos = relationship("Evento", back_populates="autor")
    lancamentos = relationship("LancamentoFinanceiro", back_populates="registrado_por_usuario")
