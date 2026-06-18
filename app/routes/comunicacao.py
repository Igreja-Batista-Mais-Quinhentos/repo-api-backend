from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.models.comunicacao import Aviso, Evento, EventoConfirmacao, PedidoOracao, Oracao
from app.models.usuario import Usuario, Papel
from app.schemas.comunicacao import (
    AvisoCreate, AvisoResponse,
    EventoCreate, EventoResponse,
    PedidoOracaoCreate, PedidoOracaoResponse,
)
from app.middlewares.auth import get_usuario_atual, requer_papel

router = APIRouter(prefix="/comunicacao", tags=["Comunicação"])

# ========================
# AVISOS
# ========================
@router.get("/avisos", response_model=list[AvisoResponse])
def listar_avisos(
    apenas_ativos: bool = Query(True),
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_usuario_atual),
):
    query = db.query(Aviso)
    if apenas_ativos:
        query = query.filter(Aviso.ativo == True)
    return query.order_by(Aviso.publicado_em.desc()).all()

@router.post("/avisos", response_model=AvisoResponse, status_code=201)
def criar_aviso(
    body: AvisoCreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(requer_papel(Papel.PASTOR, Papel.LIDER)),
):
    aviso = Aviso(**body.model_dump(), autor_id=usuario.id)
    db.add(aviso)
    db.commit()
    db.refresh(aviso)
    return aviso

@router.delete("/avisos/{id}", status_code=204)
def desativar_aviso(
    id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(requer_papel(Papel.PASTOR, Papel.LIDER)),
):
    aviso = db.query(Aviso).filter(Aviso.id == id).first()
    if not aviso:
        raise HTTPException(status_code=404, detail="Aviso não encontrado")
    aviso.ativo = False
    db.commit()

# ========================
# EVENTOS
# ========================
@router.get("/eventos", response_model=list[EventoResponse])
def listar_eventos(
    incluir_cancelados: bool = Query(False),
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_usuario_atual),
):
    query = db.query(Evento)
    if not incluir_cancelados:
        query = query.filter(Evento.cancelado == False)
    eventos = query.order_by(Evento.data_inicio.asc()).all()

    result = []
    for evento in eventos:
        total = db.query(EventoConfirmacao).filter(EventoConfirmacao.evento_id == evento.id).count()
        item = EventoResponse.model_validate(evento)
        item.total_confirmacoes = total
        result.append(item)
    return result

@router.post("/eventos", response_model=EventoResponse, status_code=201)
def criar_evento(
    body: EventoCreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(requer_papel(Papel.PASTOR, Papel.LIDER)),
):
    evento = Evento(**body.model_dump(), criado_por=usuario.id)
    db.add(evento)
    db.commit()
    db.refresh(evento)
    item = EventoResponse.model_validate(evento)
    item.total_confirmacoes = 0
    return item

@router.post("/eventos/{id}/confirmar", status_code=204)
def confirmar_presenca(
    id: int,
    membro_id: int = Query(...),
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_usuario_atual),
):
    if not db.query(Evento).filter(Evento.id == id, Evento.cancelado == False).first():
        raise HTTPException(status_code=404, detail="Evento não encontrado")
    existe = db.query(EventoConfirmacao).filter(
        EventoConfirmacao.evento_id == id,
        EventoConfirmacao.membro_id == membro_id,
    ).first()
    if not existe:
        db.add(EventoConfirmacao(evento_id=id, membro_id=membro_id))
        db.commit()

@router.delete("/eventos/{id}/confirmar", status_code=204)
def cancelar_confirmacao(
    id: int,
    membro_id: int = Query(...),
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_usuario_atual),
):
    confirmacao = db.query(EventoConfirmacao).filter(
        EventoConfirmacao.evento_id == id,
        EventoConfirmacao.membro_id == membro_id,
    ).first()
    if confirmacao:
        db.delete(confirmacao)
        db.commit()

# ========================
# PEDIDOS DE ORAÇÃO
# ========================
@router.get("/pedidos-oracao", response_model=list[PedidoOracaoResponse])
def listar_pedidos(
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_atual),
):
    query = db.query(PedidoOracao).filter(
        (PedidoOracao.privado == False) | (PedidoOracao.membro_id == usuario.id)
    )
    pedidos = query.order_by(PedidoOracao.criado_em.desc()).all()

    result = []
    for pedido in pedidos:
        total = db.query(Oracao).filter(Oracao.pedido_id == pedido.id).count()
        item = PedidoOracaoResponse.model_validate(pedido)
        item.total_oracoes = total
        result.append(item)
    return result

@router.post("/pedidos-oracao", response_model=PedidoOracaoResponse, status_code=201)
def criar_pedido(
    body: PedidoOracaoCreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_atual),
):
    from app.models.membro import Membro
    membro = db.query(Membro).filter(Membro.id == usuario.id).first()
    if not membro:
        raise HTTPException(status_code=400, detail="Usuário não possui perfil de membro")

    pedido = PedidoOracao(**body.model_dump(), membro_id=membro.id)
    db.add(pedido)
    db.commit()
    db.refresh(pedido)
    item = PedidoOracaoResponse.model_validate(pedido)
    item.total_oracoes = 0
    return item

@router.post("/pedidos-oracao/{id}/orar", status_code=204)
def registrar_oracao(
    id: int,
    membro_id: int = Query(...),
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_usuario_atual),
):
    pedido = db.query(PedidoOracao).filter(PedidoOracao.id == id).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    if pedido.privado:
        raise HTTPException(status_code=403, detail="Pedido privado")
    existe = db.query(Oracao).filter(
        Oracao.pedido_id == id, Oracao.membro_id == membro_id
    ).first()
    if not existe:
        db.add(Oracao(pedido_id=id, membro_id=membro_id))
        db.commit()

@router.patch("/pedidos-oracao/{id}/respondido", status_code=204)
def marcar_respondido(
    id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(requer_papel(Papel.PASTOR, Papel.LIDER)),
):
    pedido = db.query(PedidoOracao).filter(PedidoOracao.id == id).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    pedido.respondido = True
    db.commit()
