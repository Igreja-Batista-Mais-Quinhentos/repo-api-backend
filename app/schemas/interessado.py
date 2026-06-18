from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class InteressadoCreate(BaseModel):
    nome: str
    email: EmailStr
    telefone: Optional[str] = None
    frequenta: Optional[str] = None
    mensagem: Optional[str] = None

class InteressadoResponse(BaseModel):
    id: int
    nome: str
    email: str
    telefone: Optional[str]
    frequenta: Optional[str]
    mensagem: Optional[str]
    criado_em: datetime

    class Config:
        from_attributes = True
