import enum
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, Enum, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class TipoLancamento(str, enum.Enum):
    DIZIMO = "DIZIMO"
    DOACAO = "DOACAO"
    DESPESA = "DESPESA"

class CategoriaFinanceira(Base):
    __tablename__ = "categorias_financeiras"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255), nullable=False)
    tipo = Column(Enum(TipoLancamento), nullable=False)

    lancamentos = relationship("LancamentoFinanceiro", back_populates="categoria")

class Campanha(Base):
    __tablename__ = "campanhas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255), nullable=False)
    descricao = Column(String(500), nullable=True)
    meta_valor = Column(Numeric(10, 2), nullable=True)
    data_inicio = Column(Date, nullable=False)
    data_fim = Column(Date, nullable=True)

    lancamentos = relationship("LancamentoFinanceiro", back_populates="campanha")

class LancamentoFinanceiro(Base):
    __tablename__ = "lancamentos_financeiros"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tipo = Column(Enum(TipoLancamento), nullable=False)
    valor = Column(Numeric(10, 2), nullable=False)
    data = Column(Date, nullable=False)
    descricao = Column(String(500), nullable=True)
    comprovante_url = Column(String(500), nullable=True)
    criado_em = Column(DateTime, server_default=func.now())

    membro_id = Column(Integer, ForeignKey("membros.id"), nullable=True)
    campanha_id = Column(Integer, ForeignKey("campanhas.id"), nullable=True)
    categoria_id = Column(Integer, ForeignKey("categorias_financeiras.id"), nullable=False)
    registrado_por = Column(Integer, ForeignKey("usuarios.id"), nullable=False)

    membro = relationship("Membro", back_populates="lancamentos")
    campanha = relationship("Campanha", back_populates="lancamentos")
    categoria = relationship("CategoriaFinanceira", back_populates="lancamentos")
    registrado_por_usuario = relationship("Usuario", back_populates="lancamentos")
