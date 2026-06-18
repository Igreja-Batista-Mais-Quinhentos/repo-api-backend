from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Aviso(Base):
    __tablename__ = "avisos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(255), nullable=False)
    conteudo = Column(Text, nullable=False)
    publicado_em = Column(DateTime, server_default=func.now())
    ativo = Column(Boolean, default=True)

    autor_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    grupo_id = Column(Integer, ForeignKey("grupos.id"), nullable=True)

    autor = relationship("Usuario", back_populates="avisos")
    grupo = relationship("Grupo", back_populates="avisos")

class Evento(Base):
    __tablename__ = "eventos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(255), nullable=False)
    descricao = Column(Text, nullable=True)
    local = Column(String(500), nullable=True)
    data_inicio = Column(DateTime, nullable=False)
    data_fim = Column(DateTime, nullable=True)
    cancelado = Column(Boolean, default=False)
    criado_em = Column(DateTime, server_default=func.now())

    criado_por = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    autor = relationship("Usuario", back_populates="eventos")

    confirmacoes = relationship("EventoConfirmacao", back_populates="evento")
    frequencias = relationship("Frequencia", back_populates="evento")

class EventoConfirmacao(Base):
    __tablename__ = "evento_confirmacoes"

    evento_id = Column(Integer, ForeignKey("eventos.id"), primary_key=True)
    membro_id = Column(Integer, ForeignKey("membros.id"), primary_key=True)

    evento = relationship("Evento", back_populates="confirmacoes")
    membro = relationship("Membro", back_populates="eventos_confirmados")

class PedidoOracao(Base):
    __tablename__ = "pedidos_oracao"

    id = Column(Integer, primary_key=True, autoincrement=True)
    conteudo = Column(Text, nullable=False)
    privado = Column(Boolean, default=False)
    respondido = Column(Boolean, default=False)
    criado_em = Column(DateTime, server_default=func.now())

    membro_id = Column(Integer, ForeignKey("membros.id"), nullable=False)
    membro = relationship("Membro", back_populates="pedidos_oracao")
    oracoes = relationship("Oracao", back_populates="pedido")

class Oracao(Base):
    __tablename__ = "oracoes"

    pedido_id = Column(Integer, ForeignKey("pedidos_oracao.id"), primary_key=True)
    membro_id = Column(Integer, ForeignKey("membros.id"), primary_key=True)

    pedido = relationship("PedidoOracao", back_populates="oracoes")
    membro = relationship("Membro", back_populates="oracoes")
