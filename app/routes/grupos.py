from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.models.grupo import Grupo, GrupoMembro
from app.models.frequencia import Frequencia
from app.models.comunicacao import Evento
from app.models.membro import Membro
from app.models.usuario import Usuario, Papel
from app.schemas.grupo import (
    GrupoCreate, GrupoResponse,
    FrequenciaRegistro, FrequenciaResponse,
    ResumoFrequencia,
)
from app.middlewares.auth import get_usuario_atual, requer_papel

router = APIRouter(tags=["Grupos & Frequência"])

# ========================
# GRUPOS
# ========================
@router.get("/grupos", response_model=list[GrupoResponse])
def listar_grupos(
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_usuario_atual),
):
    grupos = db.query(Grupo).order_by(Grupo.nome).all()
    result = []
    for g in grupos:
        total = db.query(GrupoMembro).filter(GrupoMembro.grupo_id == g.id).count()
        item = GrupoResponse.model_validate(g)
        item.total_membros = total
        result.append(item)
    return result

@router.post("/grupos", response_model=GrupoResponse, status_code=201)
def criar_grupo(
    body: GrupoCreate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(requer_papel(Papel.PASTOR, Papel.LIDER)),
):
    if not db.query(Membro).filter(Membro.id == body.lider_id).first():
        raise HTTPException(status_code=404, detail="Líder não encontrado")
    grupo = Grupo(**body.model_dump())
    db.add(grupo)
    db.commit()
    db.refresh(grupo)
    item = GrupoResponse.model_validate(grupo)
    item.total_membros = 0
    return item

@router.post("/grupos/{id}/membros", status_code=204)
def adicionar_membro_grupo(
    id: int,
    membro_id: int = Query(...),
    db: Session = Depends(get_db),
    _: Usuario = Depends(requer_papel(Papel.PASTOR, Papel.LIDER)),
):
    if not db.query(Grupo).filter(Grupo.id == id).first():
        raise HTTPException(status_code=404, detail="Grupo não encontrado")
    if not db.query(Membro).filter(Membro.id == membro_id).first():
        raise HTTPException(status_code=404, detail="Membro não encontrado")
    existe = db.query(GrupoMembro).filter(
        GrupoMembro.grupo_id == id,
        GrupoMembro.membro_id == membro_id,
    ).first()
    if not existe:
        db.add(GrupoMembro(grupo_id=id, membro_id=membro_id))
        db.commit()

@router.delete("/grupos/{id}/membros", status_code=204)
def remover_membro_grupo(
    id: int,
    membro_id: int = Query(...),
    db: Session = Depends(get_db),
    _: Usuario = Depends(requer_papel(Papel.PASTOR, Papel.LIDER)),
):
    vinculo = db.query(GrupoMembro).filter(
        GrupoMembro.grupo_id == id,
        GrupoMembro.membro_id == membro_id,
    ).first()
    if vinculo:
        db.delete(vinculo)
        db.commit()

# ========================
# FREQUÊNCIA
# ========================
@router.post("/frequencias", response_model=FrequenciaResponse, status_code=201)
def registrar_frequencia(
    body: FrequenciaRegistro,
    db: Session = Depends(get_db),
    _: Usuario = Depends(requer_papel(Papel.PASTOR, Papel.LIDER)),
):
    if not db.query(Evento).filter(Evento.id == body.evento_id).first():
        raise HTTPException(status_code=404, detail="Evento não encontrado")
    if not db.query(Membro).filter(Membro.id == body.membro_id).first():
        raise HTTPException(status_code=404, detail="Membro não encontrado")

    existente = db.query(Frequencia).filter(
        Frequencia.evento_id == body.evento_id,
        Frequencia.membro_id == body.membro_id,
    ).first()
    if existente:
        existente.presente = body.presente
        db.commit()
        db.refresh(existente)
        return existente

    freq = Frequencia(**body.model_dump())
    db.add(freq)
    db.commit()
    db.refresh(freq)
    return freq

@router.get("/frequencias/resumo", response_model=ResumoFrequencia)
def resumo_frequencia(
    evento_id: int = Query(...),
    db: Session = Depends(get_db),
    _: Usuario = Depends(requer_papel(Papel.PASTOR, Papel.LIDER)),
):
    if not db.query(Evento).filter(Evento.id == evento_id).first():
        raise HTTPException(status_code=404, detail="Evento não encontrado")

    presentes = db.query(Frequencia).filter(
        Frequencia.evento_id == evento_id,
        Frequencia.presente == True,
    ).count()
    ausentes = db.query(Frequencia).filter(
        Frequencia.evento_id == evento_id,
        Frequencia.presente == False,
    ).count()
    total = presentes + ausentes
    percentual = (presentes / total * 100) if total > 0 else 0.0

    return ResumoFrequencia(
        evento_id=evento_id,
        total_presentes=presentes,
        total_ausentes=ausentes,
        percentual_presenca=round(percentual, 1),
    )

@router.get("/frequencias", response_model=list[FrequenciaResponse])
def listar_frequencias(
    evento_id: Optional[int] = Query(None),
    membro_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    _: Usuario = Depends(requer_papel(Papel.PASTOR, Papel.LIDER)),
):
    query = db.query(Frequencia)
    if evento_id:
        query = query.filter(Frequencia.evento_id == evento_id)
    if membro_id:
        query = query.filter(Frequencia.membro_id == membro_id)
    return query.order_by(Frequencia.registrado_em.desc()).all()
