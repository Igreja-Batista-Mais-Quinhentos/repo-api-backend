from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.interessado import Interessado
from app.models.usuario import Usuario, Papel
from app.schemas.interessado import InteressadoCreate, InteressadoResponse
from app.middlewares.auth import requer_papel

router = APIRouter(prefix="/interessados", tags=["Interessados"])

@router.post("", response_model=InteressadoResponse, status_code=status.HTTP_201_CREATED)
def registrar(body: InteressadoCreate, db: Session = Depends(get_db)):
    interessado = Interessado(**body.model_dump())
    db.add(interessado)
    db.commit()
    db.refresh(interessado)
    return interessado

@router.get("", response_model=list[InteressadoResponse])
def listar(db: Session = Depends(get_db), _: Usuario = Depends(requer_papel(Papel.PASTOR, Papel.LIDER))):
    return db.query(Interessado).order_by(Interessado.criado_em.desc()).all()
