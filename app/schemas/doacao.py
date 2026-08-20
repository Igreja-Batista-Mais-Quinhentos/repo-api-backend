from pydantic import BaseModel
from typing import Optional

class FundoDoacaoCreate(BaseModel):
    key: str
    nome: str
    descricao: Optional[str] = None

class FundoDoacaoResponse(BaseModel):
    id: int
    key: str
    nome: str
    descricao: Optional[str] = None
    ativo: bool

    class Config:
        from_attributes = True

class ConfiguracaoDoacaoInput(BaseModel):
    pix_key: Optional[str] = None
    dados_bancarios: Optional[str] = None

class ConfiguracaoDoacaoResponse(BaseModel):
    pix_key: Optional[str] = None
    dados_bancarios: Optional[str] = None

    class Config:
        from_attributes = True
