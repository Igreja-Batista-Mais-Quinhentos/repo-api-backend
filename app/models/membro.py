import enum
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class EstadoCivil(str, enum.Enum):
    SOLTEIRO = "SOLTEIRO"
    CASADO = "CASADO"
    DIVORCIADO = "DIVORCIADO"
    VIUVO = "VIUVO"

class StatusMembro(str, enum.Enum):
    ATIVO = "ATIVO"
    INATIVO = "INATIVO"

class Membro(Base):
    __tablename__ = "membros"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255), nullable=False)
    cpf = Column(String(14), unique=True, nullable=True)
    telefone = Column(String(20), nullable=True)
    email = Column(String(255), unique=True, nullable=True)
    data_nascimento = Column(Date, nullable=True)
    estado_civil = Column(Enum(EstadoCivil), nullable=True)
    endereco = Column(String(500), nullable=True)
    foto_url = Column(String(500), nullable=True)
    data_ingresso = Column(DateTime, server_default=func.now())
    status = Column(Enum(StatusMembro), default=StatusMembro.ATIVO)
    criado_em = Column(DateTime, server_default=func.now())

    usuario_id = Column(Integer, ForeignKey("usuarios.id"), unique=True, nullable=True)
    usuario = relationship("Usuario", back_populates="membro")

    grupos = relationship("GrupoMembro", back_populates="membro")
    grupos_liderados = relationship("Grupo", back_populates="lider")
    frequencias = relationship("Frequencia", back_populates="membro")
    lancamentos = relationship("LancamentoFinanceiro", back_populates="membro")
    eventos_confirmados = relationship("EventoConfirmacao", back_populates="membro")
    pedidos_oracao = relationship("PedidoOracao", back_populates="membro")
    oracoes = relationship("Oracao", back_populates="membro")
