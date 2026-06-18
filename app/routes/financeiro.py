from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from typing import Optional
from decimal import Decimal
from app.database import get_db
from app.models.financeiro import CategoriaFinanceira, Campanha, LancamentoFinanceiro, TipoLancamento
from app.models.usuario import Usuario, Papel
from app.schemas.financeiro import (
    CategoriaCreate, CategoriaResponse,
    CampanhaCreate, CampanhaResponse,
    LancamentoCreate, LancamentoResponse,
    ResumoMensal
)
from app.middlewares.auth import get_usuario_atual, requer_papel

router = APIRouter(prefix="/financeiro", tags=["Financeiro"])

# ========================
# CATEGORIAS
# ========================
@router.get("/categorias", response_model=list[CategoriaResponse])
def listar_categorias(
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_usuario_atual)
):
    return db.query(CategoriaFinanceira).order_by(CategoriaFinanceira.nome).all()

@router.post("/categorias", response_model=CategoriaResponse, status_code=201)
def criar_categoria(
    body: CategoriaCreate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(requer_papel(Papel.PASTOR, Papel.TESOUREIRO))
):
    categoria = CategoriaFinanceira(**body.model_dump())
    db.add(categoria)
    db.commit()
    db.refresh(categoria)
    return categoria

# ========================
# CAMPANHAS
# ========================
@router.get("/campanhas", response_model=list[CampanhaResponse])
def listar_campanhas(
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_usuario_atual)
):
    return db.query(Campanha).order_by(Campanha.data_inicio.desc()).all()

@router.post("/campanhas", response_model=CampanhaResponse, status_code=201)
def criar_campanha(
    body: CampanhaCreate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(requer_papel(Papel.PASTOR, Papel.TESOUREIRO))
):
    campanha = Campanha(**body.model_dump())
    db.add(campanha)
    db.commit()
    db.refresh(campanha)
    return campanha

# ========================
# LANÇAMENTOS
# ========================
@router.get("/lancamentos", response_model=list[LancamentoResponse])
def listar_lancamentos(
    tipo: Optional[TipoLancamento] = Query(None),
    membro_id: Optional[int] = Query(None),
    mes: Optional[int] = Query(None),
    ano: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    _: Usuario = Depends(requer_papel(Papel.PASTOR, Papel.TESOUREIRO))
):
    query = db.query(LancamentoFinanceiro)

    if tipo:
        query = query.filter(LancamentoFinanceiro.tipo == tipo)
    if membro_id:
        query = query.filter(LancamentoFinanceiro.membro_id == membro_id)
    if mes:
        query = query.filter(extract('month', LancamentoFinanceiro.data) == mes)
    if ano:
        query = query.filter(extract('year', LancamentoFinanceiro.data) == ano)

    return query.order_by(LancamentoFinanceiro.data.desc()).all()

@router.post("/lancamentos", response_model=LancamentoResponse, status_code=201)
def criar_lancamento(
    body: LancamentoCreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(requer_papel(Papel.PASTOR, Papel.TESOUREIRO))
):
    if not db.query(CategoriaFinanceira).filter(CategoriaFinanceira.id == body.categoria_id).first():
        raise HTTPException(status_code=404, detail="Categoria não encontrada")

    lancamento = LancamentoFinanceiro(**body.model_dump(), registrado_por=usuario.id)
    db.add(lancamento)
    db.commit()
    db.refresh(lancamento)
    return lancamento

# ========================
# RESUMO MENSAL
# ========================
@router.get("/resumo", response_model=ResumoMensal)
def resumo_mensal(
    mes: int = Query(..., ge=1, le=12),
    ano: int = Query(..., ge=2000),
    db: Session = Depends(get_db),
    _: Usuario = Depends(requer_papel(Papel.PASTOR, Papel.TESOUREIRO))
):
    def total_tipo(tipo: TipoLancamento) -> Decimal:
        resultado = db.query(func.sum(LancamentoFinanceiro.valor)).filter(
            LancamentoFinanceiro.tipo == tipo,
            extract('month', LancamentoFinanceiro.data) == mes,
            extract('year', LancamentoFinanceiro.data) == ano
        ).scalar()
        return resultado or Decimal("0")

    dizimos = total_tipo(TipoLancamento.DIZIMO)
    doacoes = total_tipo(TipoLancamento.DOACAO)
    despesas = total_tipo(TipoLancamento.DESPESA)

    return ResumoMensal(
        mes=mes,
        ano=ano,
        total_dizimos=dizimos,
        total_doacoes=doacoes,
        total_despesas=despesas,
        saldo=(dizimos + doacoes) - despesas
    )
