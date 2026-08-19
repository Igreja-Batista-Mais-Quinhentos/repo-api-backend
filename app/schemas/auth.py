from pydantic import BaseModel, EmailStr
from typing import Optional
from app.models.usuario import Papel

class RegisterInput(BaseModel):
    email: EmailStr
    senha: str

class LoginInput(BaseModel):
    email: EmailStr
    senha: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UsuarioResponse(BaseModel):
    id: int
    email: str
    papel: Papel
    ativo: bool
    membro_id: Optional[int] = None

    class Config:
        from_attributes = True
