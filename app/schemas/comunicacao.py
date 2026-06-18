from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AvisoCreate(BaseModel):
    titulo: str
    conteudo: str
    grupo_id: Optional[int] = None

class AvisoResponse(BaseModel):
    id: int
    titulo: str
    conteudo: str
    ativo: bool
    publicado_em: datetime
    autor_id: int
    grupo_id: Optional[int] = None

    class Config:
        from_attributes = True

class EventoCreate(BaseModel):
    titulo: str
    descricao: Optional[str] = None
    local: Optional[str] = None
    data_inicio: datetime
    data_fim: Optional[datetime] = None

class EventoResponse(BaseModel):
    id: int
    titulo: str
    descricao: Optional[str] = None
    local: Optional[str] = None
    data_inicio: datetime
    data_fim: Optional[datetime] = None
    cancelado: bool
    criado_em: datetime
    criado_por: int
    total_confirmacoes: int = 0

    class Config:
        from_attributes = True

class PedidoOracaoCreate(BaseModel):
    conteudo: str
    privado: bool = False

class PedidoOracaoResponse(BaseModel):
    id: int
    conteudo: str
    privado: bool
    respondido: bool
    criado_em: datetime
    membro_id: int
    total_oracoes: int = 0

    class Config:
        from_attributes = True
