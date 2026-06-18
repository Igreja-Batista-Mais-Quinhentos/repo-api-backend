from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from typing import Optional
from app.models.membro import EstadoCivil, StatusMembro

class MembroCreate(BaseModel):
    nome: str
    cpf: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[EmailStr] = None
    data_nascimento: Optional[date] = None
    estado_civil: Optional[EstadoCivil] = None
    endereco: Optional[str] = None

class MembroUpdate(BaseModel):
    nome: Optional[str] = None
    cpf: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[EmailStr] = None
    data_nascimento: Optional[date] = None
    estado_civil: Optional[EstadoCivil] = None
    endereco: Optional[str] = None

class MembroResponse(BaseModel):
    id: int
    nome: str
    cpf: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[str] = None
    data_nascimento: Optional[date] = None
    estado_civil: Optional[EstadoCivil] = None
    endereco: Optional[str] = None
    foto_url: Optional[str] = None
    data_ingresso: datetime
    status: StatusMembro

    class Config:
        from_attributes = True
