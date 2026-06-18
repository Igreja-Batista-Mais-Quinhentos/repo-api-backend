from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.models.membro import Membro, StatusMembro
from app.models.usuario import Usuario, Papel
from app.schemas.membro import MembroCreate, MembroUpdate, MembroResponse
from app.middlewares.auth import get_usuario_atual, requer_papel

router = APIRouter(prefix="/membros", tags=["Membros"])

@router.get("/", response_model=list[MembroResponse])
def listar(
    busca: Optional[str] = Query(None, description="Buscar por nome ou telefone"),
    status: Optional[StatusMembro] = Query(None),
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_usuario_atual)
):
    query = db.query(Membro)

    if busca:
        query = query.filter(
            Membro.nome.ilike(f"%{busca}%") |
            Membro.telefone.ilike(f"%{busca}%")
        )

    if status:
        query = query.filter(Membro.status == status)

    return query.order_by(Membro.nome).all()

@router.get("/{id}", response_model=MembroResponse)
def buscar(
    id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_usuario_atual)
):
    membro = db.query(Membro).filter(Membro.id == id).first()
    if not membro:
        raise HTTPException(status_code=404, detail="Membro não encontrado")
    return membro

@router.post("/", response_model=MembroResponse, status_code=status.HTTP_201_CREATED)
def cadastrar(
    body: MembroCreate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(requer_papel(Papel.PASTOR, Papel.LIDER))
):
    if body.cpf and db.query(Membro).filter(Membro.cpf == body.cpf).first():
        raise HTTPException(status_code=400, detail="CPF já cadastrado")

    if body.email and db.query(Membro).filter(Membro.email == body.email).first():
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")

    membro = Membro(**body.model_dump())
    db.add(membro)
    db.commit()
    db.refresh(membro)
    return membro

@router.put("/{id}", response_model=MembroResponse)
def editar(
    id: int,
    body: MembroUpdate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(requer_papel(Papel.PASTOR, Papel.LIDER))
):
    membro = db.query(Membro).filter(Membro.id == id).first()
    if not membro:
        raise HTTPException(status_code=404, detail="Membro não encontrado")

    for campo, valor in body.model_dump(exclude_unset=True).items():
        setattr(membro, campo, valor)

    db.commit()
    db.refresh(membro)
    return membro

@router.patch("/{id}/status", response_model=MembroResponse)
def alterar_status(
    id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(requer_papel(Papel.PASTOR))
):
    membro = db.query(Membro).filter(Membro.id == id).first()
    if not membro:
        raise HTTPException(status_code=404, detail="Membro não encontrado")

    membro.status = StatusMembro.INATIVO if membro.status == StatusMembro.ATIVO else StatusMembro.ATIVO
    db.commit()
    db.refresh(membro)
    return membro
