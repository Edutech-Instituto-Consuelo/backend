from fastapi import APIRouter, Depends, status, HTTPException, Path
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.evaluation import AvaliacaoCurso
from app.models.user import Usuario
from app.models.course import Curso
from app.models.enrollment import Matricula
from app.schemas.evaluation import AvaliacaoCriar, AvaliacaoResponse
from app.core.security import allowed_roles

router = APIRouter(
    prefix="/courses",
    tags=["Evaluations"]
)

# Schema customizado para listar avaliações (sem usuario_id, com nome_usuario)
from pydantic import BaseModel
from datetime import datetime

class AvaliacaoListaResponse(BaseModel):
    id: int
    nome_usuario: str
    nota: int
    comentario: str
    data: datetime

    class Config:
        from_attributes = True

# Rota para listar avaliações de um curso
@router.get("/{curso_id}/reviews", response_model=List[AvaliacaoListaResponse])
def listar_avaliacoes(
    curso_id: int = Path(..., gt=0),
    db: Session = Depends(get_db)
):
    """
    Retorna todas as avaliações de um curso.
    Não requer autenticação.
    """
    curso = db.query(Curso).filter(Curso.id == curso_id).first()
    if not curso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Curso não encontrado"
        )

    avaliacoes = db.query(AvaliacaoCurso).filter(
        AvaliacaoCurso.curso_id == curso_id
    ).all()

    # Mapear para resposta com nome_usuario
    resultado = []
    for avaliacao in avaliacoes:
        resultado.append({
            "id": avaliacao.id,
            "nome_usuario": f"{avaliacao.usuario.nome} {avaliacao.usuario.sobrenome}",
            "nota": avaliacao.nota,
            "comentario": avaliacao.comentario,
            "data": avaliacao.data_criacao
        })

    return resultado

# Rota para criar uma nova avaliação
@router.post("/{curso_id}/reviews", response_model=AvaliacaoResponse, status_code=status.HTTP_201_CREATED)
def criar_avaliacao(
    curso_id: int = Path(..., gt=0),
    avaliacao_data: AvaliacaoCriar = None,
    db: Session = Depends(get_db),
    usuario_autenticado = Depends(allowed_roles("aluno"))
):
    """
    Cria uma nova avaliação para um curso.
    Requer que o usuário seja um aluno e esteja matriculado no curso.
    """
    usuario_id = usuario_autenticado["id"]
    
    # Verificar se o curso existe
    curso = db.query(Curso).filter(Curso.id == curso_id).first()
    if not curso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Curso não encontrado"
        )

    # Verificar se o aluno está matriculado no curso
    matricula = db.query(Matricula).filter(
        Matricula.aluno_id == usuario_id,
        Matricula.curso_id == curso_id
    ).first()

    if not matricula:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não está matriculado neste curso"
        )

    # Verificar se o aluno já avaliou este curso
    ja_avaliou = db.query(AvaliacaoCurso).filter(
        AvaliacaoCurso.usuario_id == usuario_id,
        AvaliacaoCurso.curso_id == curso_id
    ).first()

    if ja_avaliou:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Você já avaliou este curso"
        )

    # Criar a avaliação
    nova_avaliacao = AvaliacaoCurso(
        nota=avaliacao_data.nota,
        comentario=avaliacao_data.comentario,
        curso_id=curso_id,
        usuario_id=usuario_id
    )

    db.add(nova_avaliacao)
    db.commit()
    db.refresh(nova_avaliacao)

    return nova_avaliacao