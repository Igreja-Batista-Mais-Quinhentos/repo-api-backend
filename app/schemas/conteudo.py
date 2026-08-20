from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class MinisterioCreate(BaseModel):
    nome: str
    tag: str
    descricao: str
    lider: Optional[str] = None
    quando: Optional[str] = None
    foto_url: Optional[str] = None

class MinisterioResponse(BaseModel):
    id: int
    nome: str
    tag: str
    descricao: str
    lider: Optional[str] = None
    quando: Optional[str] = None
    foto_url: Optional[str] = None
    ativo: bool
    criado_em: datetime

    class Config:
        from_attributes = True

class NoticiaCreate(BaseModel):
    categoria: str
    titulo: str
    resumo: Optional[str] = None
    corpo: str
    foto_url: Optional[str] = None

class NoticiaResponse(BaseModel):
    id: int
    categoria: str
    titulo: str
    resumo: Optional[str] = None
    corpo: str
    foto_url: Optional[str] = None
    ativo: bool
    publicado_em: datetime
    autor_id: int

    class Config:
        from_attributes = True
