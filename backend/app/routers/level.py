from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.core.security import allowed_roles
from app.models.level import Nivel
from app.schemas.level import NivelCreate, NivelResponse, NivelUpdate

router = APIRouter(
	prefix="/levels",
	tags=["levels"]
)

@router.post("/", response_model=NivelResponse, status_code=status.HTTP_201_CREATED)
def criar_nivel(
	nivel_request: NivelCreate,
	db: Session = Depends(get_db),
	require = Depends(allowed_roles("admin"))
):
	nivel_db = db.query(Nivel).filter(
		Nivel.descricao == nivel_request.descricao).first()

	if nivel_db:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail="level ja existe"
		)
	nivel_add = Nivel(
		descricao = nivel_request.descricao
	)

	db.add(nivel_add)
	db.commit()
	db.refresh(nivel_add)

	return nivel_add

@router.get("/", response_model=List[NivelResponse])
def listar_niveis(
	db: Session = Depends(get_db)
):
	niveis = db.query(Nivel)

	return niveis

@router.patch("/{id_level}", response_model=NivelResponse)
def atualiza_nivel(
	id_level: int,
	nivel_update: NivelUpdate,
	db: Session = Depends(get_db),
	require = Depends(allowed_roles("admin"))
):
	nivel_db = db.query(Nivel).filter(Nivel.id == id_level).first()

	if not nivel_db:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail=f"Nivel com id {id_level}, não encontrado"
		)

	update_data = nivel_update.model_dump(exclude_unset=True)
	for campo, value in update_data.items():
		setattr(nivel_db, campo, value)

	db.commit()
	db.refresh(nivel_db)

	return nivel_db

@router.delete("/{id_nivel}", status_code=status.HTTP_204_NO_CONTENT)
def deleta_nivel(
	id_nivel: int,
	db: Session = Depends(get_db),
	require = Depends(allowed_roles("admin"))
):
	nivel_db = db.query(Nivel).filter(
		Nivel.id == id_nivel).first()
	if not nivel_db:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail=f"Categoria com ID{id_nivel} não encontrado"
		)

	db.delete(nivel_db)
	db.commit()

	return None
