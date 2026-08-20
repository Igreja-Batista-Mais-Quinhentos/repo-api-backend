from sqlalchemy import Column, Integer, String, Boolean, Text
from app.database import Base

class FundoDoacao(Base):
    __tablename__ = "fundos_doacao"

    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String(50), unique=True, nullable=False)
    nome = Column(String(255), nullable=False)
    descricao = Column(String(500), nullable=True)
    ativo = Column(Boolean, default=True)

class ConfiguracaoDoacao(Base):
    __tablename__ = "configuracao_doacao"

    id = Column(Integer, primary_key=True, default=1)
    pix_key = Column(String(255), nullable=True)
    dados_bancarios = Column(Text, nullable=True)
