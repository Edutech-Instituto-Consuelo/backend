from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from typing import List

from app.models.instructor import Instrutor
from app.models.specialty import Especialidade
from app.schemas.instructor import InstrutorEspecificoResponse
from app.core.response import success_response

router = APIRouter(
	prefix="/instructors",
	tags=["instructors"]
)

@router.get("/{id_instrutor}", response_model=dict)
def pega_instrutor(
    id_instrutor: int,
    db: Session = Depends(get_db)
):
    resultado = db.query(Instrutor, Especialidade
    ).join(Especialidade, Especialidade.id == Instrutor.especialidade
    ).filter(Instrutor.id == id_instrutor
    ).first()

    if not resultado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Instrutor com id {id_instrutor} não encontrado"
        )

    instrutor, especialidade = resultado
    data = {
        "id": instrutor.id,
        "nome": instrutor.usuario.nome,
        "id_especialidade": especialidade.id,
        "especialidade": especialidade.nome,
        "biografia": instrutor.biografia
    }

    return success_response(
        data=data,
        message="Instrutor encontrado com sucesso",
        status_code=status.HTTP_200_OK
    )
