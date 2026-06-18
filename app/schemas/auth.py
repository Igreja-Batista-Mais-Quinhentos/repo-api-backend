from pydantic import BaseModel, EmailStr
from app.models.usuario import Papel

class RegisterInput(BaseModel):
    email: EmailStr
    senha: str
    papel: Papel = Papel.MEMBRO

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

    class Config:
        from_attributes = True
