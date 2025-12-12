from typing import List, Optional, Annotated
from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from decimal import Decimal

from app.database import get_db
from app.core.security import allowed_roles     
from app.models.course import Curso
from app.models.status_course import StatusCurso
from app.schemas.status_course import StatusCursoResponse

# ajustar este import para o nome exato do schema de curso
from app.schemas.course import CursoResponse as CursoSchema

router = APIRouter(tags=["courses (admin)"])

# --- payloads simples ---

PriceType = Annotated[Decimal, Field(..., ge=0, description="Preço do curso (>= 0)")]

class PriceIn(BaseModel):
    preco: PriceType

class InstructorIn(BaseModel):
    instrutor_id: int

# Funções para procurar curso(por id) e status de publicação(npor nome) =============

def _get_curso(db: Session, curso_id: int) -> Optional[Curso]:
    return db.query(Curso).filter(Curso.id == curso_id).first()

def _get_status(db: Session, descricao: str) -> Optional[StatusCurso]:
    return db.query(StatusCurso).filter(StatusCurso.descricao == descricao).first()


# ================   ROTAS CURSOS apenas para admin ===============#

# GET /courses/pending-publish 
# (lista de cursos com solicitacao de publicacao - PODEM SE TORNAR FILTROS DA ROTA GET: "/courses")
@router.get("/courses/pending-publish", response_model=List[CursoSchema])
def listar_pub_pendentes(
    db: Session = Depends(get_db), 
    admin = Depends(allowed_roles("admin"))):
    status_obj = _get_status(db, "aguardando_publicacao")
    if not status_obj:
        raise HTTPException(status_code=400, detail="Status 'aguardando_publicacao' não encontrado.")
    cursos = db.query(Curso).filter(Curso.status_id == status_obj.id).all()
    return cursos




# GET /courses/pending-unpublish
# lista de cursos com solicitacao de despublicacao pendente - PODEM SE TORNAR FILTROS DA ROTA GET: "/courses"
@router.get("/courses/pending-unpublish", response_model=List[CursoSchema])
def listar_unpub_pendentes(
    db: Session = Depends(get_db), 
    admin = Depends(allowed_roles("admin"))):
        status_obj = _get_status(db, "Despublicacao_pendente")
        if not status_obj:
            raise HTTPException(status_code=400, detail="Status 'Despublicacao_pendente' não encontrado.")
        cursos = db.query(Curso).filter(Curso.status_id == status_obj.id).all()
        return cursos





# PATCH /courses/{id}/publish
@router.patch("/courses/{id}/publish", response_model=CursoSchema)
def publicar_curso(
    id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    admin = Depends(allowed_roles("admin"))
):
    curso = _get_curso(db, id)
    if not curso:
        raise HTTPException(status_code=404, detail="Curso não encontrado")

    status_atual = curso.status.descricao if curso.status else None

    # regra: só publicar se estiver 'aguardando_publicacao' ou criado pelo admin que requisita
    criado_por_admin = getattr(curso, "criado_por_admin_id", None) == admin.get("id") if isinstance(admin, dict) else getattr(curso, "criado_por_admin_id", None) == getattr(admin, "id", None)
    if status_atual != "aguardando_publicacao" and not criado_por_admin:
        raise HTTPException(status_code=400, detail="Só é possível publicar cursos que estejam 'aguardando_publicacao' ou que você tenha criado.")

    destino = _get_status(db, "publicado")
    if not destino:
        raise HTTPException(status_code=400, detail="Status 'publicado' não encontrado. Seed via migration.")

    curso.status_id = destino.id
    db.add(curso)
    db.commit()
    db.refresh(curso)
    return curso





# PATCH /courses/{id}/unpublish
@router.patch("/courses/{id}/unpublish", response_model=CursoSchema)
def despublicar_curso(
    id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    admin = Depends(allowed_roles("admin"))
):
    curso = _get_curso(db, id)
    if not curso:
        raise HTTPException(status_code=404, detail="Curso não encontrado")

    status_atual = curso.status.descricao if curso.status else None
    if status_atual != "publicado":
        raise HTTPException(status_code=400, detail="Só é possível despublicar cursos que estejam 'publicado'.")

    destino = _get_status(db, "aguardando_despublicacao")
    if not destino:
        raise HTTPException(status_code=400, detail="Status 'aguardando_despublicacao' não encontrado.")

    curso.status_id = destino.id
    db.add(curso)
    db.commit()
    db.refresh(curso)
    return curso



# POST /courses/{id}/pricing
@router.post("/courses/{id}/pricing", response_model=CursoSchema)
def definir_preco(
    id: int = Path(..., gt=0),
    payload: PriceIn = None,
    db: Session = Depends(get_db),
    admin = Depends(allowed_roles("admin"))
):
    if payload is None:
        raise HTTPException(status_code=400, detail="Payload inválido")
    curso = _get_curso(db, id)
    if not curso:
        raise HTTPException(status_code=404, detail="Curso não encontrado")

    curso.preco = float(payload.preco)
    db.add(curso)
    db.commit()
    db.refresh(curso)
    return curso




# PATCH /courses/{id}/instructor
@router.patch("/courses/{id}/instructor", response_model=CursoSchema)
def definir_instructor(
    id: int = Path(..., gt=0),
    payload: InstructorIn = None,
    db: Session = Depends(get_db),
    admin = Depends(allowed_roles("admin"))
):
    if payload is None:
        raise HTTPException(status_code=400, detail="Payload inválido")
    curso = _get_curso(db, id)
    if not curso:
        raise HTTPException(status_code=404, detail="Curso não encontrado")

    curso.instrutor_id = payload.instrutor_id
    db.add(curso)
    db.commit()
    db.refresh(curso)
    return curso
