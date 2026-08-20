import bcrypt
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.usuario import Usuario, Papel
from app.models.membro import Membro
from app.schemas.auth import RegisterInput, LoginInput, TokenResponse, UsuarioResponse
from app.middlewares.auth import create_token, get_usuario_atual
from app.limiter import limiter

router = APIRouter(prefix="/auth", tags=["Autenticação"])

@router.post("/cadastrar", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("10/minute")
def cadastrar(request: Request, body: RegisterInput, db: Session = Depends(get_db)):
    if db.query(Usuario).filter(Usuario.email == body.email).first():
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")

    senha_hash = bcrypt.hashpw(body.senha.encode(), bcrypt.gensalt()).decode()

    usuario = Usuario(email=body.email, senha_hash=senha_hash, papel=Papel.MEMBRO)
    db.add(usuario)
    db.commit()
    db.refresh(usuario)

    membro_existente = db.query(Membro).filter(Membro.email == body.email).first()
    if membro_existente:
        if not membro_existente.usuario_id:
            membro_existente.usuario_id = usuario.id
    else:
        db.add(Membro(nome=body.email.split("@")[0], email=body.email, usuario_id=usuario.id))
    db.commit()

    token = create_token({
        "sub": str(usuario.id),
        "email": usuario.email,
        "papel": usuario.papel,
        "exp": datetime.now(timezone.utc) + timedelta(days=7)
    })

    return {"access_token": token}

@router.post("/login", response_model=TokenResponse)
@limiter.limit("10/minute")
def login(request: Request, body: LoginInput, db: Session = Depends(get_db)):
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
    return UsuarioResponse(
        id=usuario.id,
        email=usuario.email,
        papel=usuario.papel,
        ativo=usuario.ativo,
        membro_id=usuario.membro.id if usuario.membro else None,
    )
