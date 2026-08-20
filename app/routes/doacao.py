from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.doacao import FundoDoacao, ConfiguracaoDoacao
from app.models.usuario import Usuario, Papel
from app.schemas.doacao import (
    FundoDoacaoCreate, FundoDoacaoResponse,
    ConfiguracaoDoacaoInput, ConfiguracaoDoacaoResponse,
)
from app.middlewares.auth import get_usuario_atual, requer_papel

router = APIRouter(prefix="/doacao", tags=["Doação"])

@router.get("/fundos", response_model=list[FundoDoacaoResponse])
def listar_fundos(
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_usuario_atual),
):
    return db.query(FundoDoacao).filter(FundoDoacao.ativo == True).all()

@router.post("/fundos", response_model=FundoDoacaoResponse, status_code=201)
def criar_fundo(
    body: FundoDoacaoCreate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(requer_papel(Papel.PASTOR, Papel.TESOUREIRO)),
):
    if db.query(FundoDoacao).filter(FundoDoacao.key == body.key).first():
        raise HTTPException(status_code=400, detail="Já existe um fundo com essa chave")
    fundo = FundoDoacao(**body.model_dump())
    db.add(fundo)
    db.commit()
    db.refresh(fundo)
    return fundo

@router.delete("/fundos/{id}", status_code=204)
def desativar_fundo(
    id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(requer_papel(Papel.PASTOR, Papel.TESOUREIRO)),
):
    fundo = db.query(FundoDoacao).filter(FundoDoacao.id == id).first()
    if not fundo:
        raise HTTPException(status_code=404, detail="Fundo não encontrado")
    fundo.ativo = False
    db.commit()

@router.get("/config", response_model=ConfiguracaoDoacaoResponse)
def obter_config(
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_usuario_atual),
):
    config = db.query(ConfiguracaoDoacao).filter(ConfiguracaoDoacao.id == 1).first()
    if not config:
        return ConfiguracaoDoacaoResponse(pix_key=None, dados_bancarios=None)
    return config

@router.put("/config", response_model=ConfiguracaoDoacaoResponse)
def atualizar_config(
    body: ConfiguracaoDoacaoInput,
    db: Session = Depends(get_db),
    _: Usuario = Depends(requer_papel(Papel.PASTOR, Papel.TESOUREIRO)),
):
    config = db.query(ConfiguracaoDoacao).filter(ConfiguracaoDoacao.id == 1).first()
    if not config:
        config = ConfiguracaoDoacao(id=1, **body.model_dump())
        db.add(config)
    else:
        for campo, valor in body.model_dump().items():
            setattr(config, campo, valor)
    db.commit()
    db.refresh(config)
    return config
