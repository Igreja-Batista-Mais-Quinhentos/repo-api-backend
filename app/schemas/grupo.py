from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class GrupoCreate(BaseModel):
    nome: str
    descricao: Optional[str] = None
    lider_id: int

class GrupoResponse(BaseModel):
    id: int
    nome: str
    descricao: Optional[str] = None
    lider_id: int
    criado_em: datetime
    total_membros: int = 0

    class Config:
        from_attributes = True

class FrequenciaRegistro(BaseModel):
    evento_id: int
    membro_id: int
    presente: bool = True

class FrequenciaResponse(BaseModel):
    id: int
    presente: bool
    registrado_em: datetime
    membro_id: int
    evento_id: int

    class Config:
        from_attributes = True

class ResumoFrequencia(BaseModel):
    evento_id: int
    total_presentes: int
    total_ausentes: int
    percentual_presenca: float
