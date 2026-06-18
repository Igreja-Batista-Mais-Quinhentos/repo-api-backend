from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional
from decimal import Decimal
from app.models.financeiro import TipoLancamento

class CategoriaCreate(BaseModel):
    nome: str
    tipo: TipoLancamento

class CategoriaResponse(BaseModel):
    id: int
    nome: str
    tipo: TipoLancamento

    class Config:
        from_attributes = True

class CampanhaCreate(BaseModel):
    nome: str
    descricao: Optional[str] = None
    meta_valor: Optional[Decimal] = None
    data_inicio: date
    data_fim: Optional[date] = None

class CampanhaResponse(BaseModel):
    id: int
    nome: str
    descricao: Optional[str] = None
    meta_valor: Optional[Decimal] = None
    data_inicio: date
    data_fim: Optional[date] = None

    class Config:
        from_attributes = True

class LancamentoCreate(BaseModel):
    tipo: TipoLancamento
    valor: Decimal
    data: date
    descricao: Optional[str] = None
    membro_id: Optional[int] = None
    campanha_id: Optional[int] = None
    categoria_id: int

class LancamentoResponse(BaseModel):
    id: int
    tipo: TipoLancamento
    valor: Decimal
    data: date
    descricao: Optional[str] = None
    comprovante_url: Optional[str] = None
    membro_id: Optional[int] = None
    campanha_id: Optional[int] = None
    categoria_id: int
    criado_em: datetime

    class Config:
        from_attributes = True

class ResumoMensal(BaseModel):
    mes: int
    ano: int
    total_dizimos: Decimal
    total_doacoes: Decimal
    total_despesas: Decimal
    saldo: Decimal
