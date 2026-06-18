import bcrypt
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.usuario import Usuario
from app.schemas.auth import RegisterInput, LoginInput, TokenResponse, UsuarioResponse
from app.middlewares.auth import create_token, get_usuario_atual

router = APIRouter(prefix="/auth", tags=["Autenticação"])

@router.post("/cadastrar", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def cadastrar(body: RegisterInput, db: Session = Depends(get_db)):
    if db.query(Usuario).filter(Usuario.email == body.email).first():
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")

    senha_hash = bcrypt.hashpw(body.senha.encode(), bcrypt.gensalt()).decode()

    usuario = Usuario(email=body.email, senha_hash=senha_hash, papel=body.papel)
    db.add(usuario)
    db.commit()
    db.refresh(usuario)

    token = create_token({
        "sub": str(usuario.id),
        "email": usuario.email,
        "papel": usuario.papel,
        "exp": datetime.now(timezone.utc) + timedelta(days=7)
    })

    return {"access_token": token}

@router.post("/login", response_model=TokenResponse)
def login(body: LoginInput, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == body.email).first()

    if not usuario or not bcrypt.checkpw(body.senha.encode(), usuario.senha_hash.encode()):
        raise HTTPException(status_code=401, detail="E-mail ou senha incorretos")

    if not usuario.ativo:
        raise HTTPException(status_code=403, detail="Usuário inativo")

    usuario.ultimo_acesso = datetime.now(timezone.utc)
    db.commit()

    token = create_token({
        "sub": str(usuario.id),
        "email": usuario.email,
        "papel": usuario.papel,
        "exp": datetime.now(timezone.utc) + timedelta(days=7)
    })

    return {"access_token": token}

@router.get("/me", response_model=UsuarioResponse)
def me(usuario: Usuario = Depends(get_usuario_atual)):
    return usuario
