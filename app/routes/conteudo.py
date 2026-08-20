from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.conteudo import Ministerio, Noticia
from app.models.usuario import Usuario, Papel
from app.schemas.conteudo import (
    MinisterioCreate, MinisterioResponse,
    NoticiaCreate, NoticiaResponse,
)
from app.middlewares.auth import requer_papel

router = APIRouter(prefix="/conteudo", tags=["Conteúdo"])

# ========================
# MINISTÉRIOS
# ========================
@router.get("/ministerios", response_model=list[MinisterioResponse])
def listar_ministerios(
    apenas_ativos: bool = Query(True),
    db: Session = Depends(get_db),
):
    query = db.query(Ministerio)
    if apenas_ativos:
        query = query.filter(Ministerio.ativo == True)
    return query.order_by(Ministerio.nome.asc()).all()

@router.post("/ministerios", response_model=MinisterioResponse, status_code=201)
def criar_ministerio(
    body: MinisterioCreate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(requer_papel(Papel.PASTOR, Papel.LIDER)),
):
    ministerio = Ministerio(**body.model_dump())
    db.add(ministerio)
    db.commit()
    db.refresh(ministerio)
    return ministerio

@router.patch("/ministerios/{id}", response_model=MinisterioResponse)
def atualizar_ministerio(
    id: int,
    body: MinisterioCreate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(requer_papel(Papel.PASTOR, Papel.LIDER)),
):
    ministerio = db.query(Ministerio).filter(Ministerio.id == id).first()
    if not ministerio:
        raise HTTPException(status_code=404, detail="Ministério não encontrado")
    for campo, valor in body.model_dump().items():
        setattr(ministerio, campo, valor)
    db.commit()
    db.refresh(ministerio)
    return ministerio

@router.delete("/ministerios/{id}", status_code=204)
def desativar_ministerio(
    id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(requer_papel(Papel.PASTOR, Papel.LIDER)),
):
    ministerio = db.query(Ministerio).filter(Ministerio.id == id).first()
    if not ministerio:
        raise HTTPException(status_code=404, detail="Ministério não encontrado")
    ministerio.ativo = False
    db.commit()

# ========================
# NOTÍCIAS
# ========================
@router.get("/noticias", response_model=list[NoticiaResponse])
def listar_noticias(
    apenas_ativos: bool = Query(True),
    db: Session = Depends(get_db),
):
    query = db.query(Noticia)
    if apenas_ativos:
        query = query.filter(Noticia.ativo == True)
    return query.order_by(Noticia.publicado_em.desc()).all()

@router.post("/noticias", response_model=NoticiaResponse, status_code=201)
def criar_noticia(
    body: NoticiaCreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(requer_papel(Papel.PASTOR, Papel.LIDER)),
):
    noticia = Noticia(**body.model_dump(), autor_id=usuario.id)
    db.add(noticia)
    db.commit()
    db.refresh(noticia)
    return noticia

@router.patch("/noticias/{id}", response_model=NoticiaResponse)
def atualizar_noticia(
    id: int,
    body: NoticiaCreate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(requer_papel(Papel.PASTOR, Papel.LIDER)),
):
    noticia = db.query(Noticia).filter(Noticia.id == id).first()
    if not noticia:
        raise HTTPException(status_code=404, detail="Notícia não encontrada")
    for campo, valor in body.model_dump().items():
        setattr(noticia, campo, valor)
    db.commit()
    db.refresh(noticia)
    return noticia

@router.delete("/noticias/{id}", status_code=204)
def desativar_noticia(
    id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(requer_papel(Papel.PASTOR, Papel.LIDER)),
):
    noticia = db.query(Noticia).filter(Noticia.id == id).first()
    if not noticia:
        raise HTTPException(status_code=404, detail="Notícia não encontrada")
    noticia.ativo = False
    db.commit()
