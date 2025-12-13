from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.security import allowed_roles
from app.models.category import Categoria
from app.schemas.category import CategoriaCreate, CategoriaResponse, CategoriaUpdate
from typing import List
from app.core.response import success_response


router = APIRouter(
	prefix="/categories",
	tags=["categories"]
)

@router.post("/", response_model=CategoriaResponse, status_code=status.HTTP_201_CREATED)
def cria_categoria(
	categoria_request: CategoriaCreate,
	db: Session = Depends(get_db),
	require = Depends(allowed_roles("admin"))):
	"""Rota que adiciona uma categoria"""

	categoria_db = db.query(Categoria).filter(
		Categoria.nome == categoria_request.nome).first()

	if categoria_db:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail="Categoria ja existe"
		)

	categoria_add = Categoria(
		nome = categoria_request.nome,
		descricao = categoria_request.descricao
	)

	db.add(categoria_add)
	db.commit()
	db.refresh(categoria_add)

	return success_response(
		data=CategoriaResponse.model_validate(categoria_add),
		message="Categoria criada com sucesso.",
		status_code=status.HTTP_201_CREATED
	)


@router.get("/", response_model=List[CategoriaResponse])
def listar_categoria(
	db: Session = Depends(get_db)
):
	categorias = db.query(Categoria)

	return success_response(
		data=[CategoriaResponse.model_validate(c) for c in categorias],
		message="Categorias listadas com sucesso."
	)

@router.patch("/{id_categoria}", response_model=CategoriaResponse)
def atualiza_categoria(
	id_categoria: int,
	categoria_update: CategoriaUpdate,
	db: Session = Depends(get_db),
	require = Depends(allowed_roles("admin"))
):
	categoria_db = db.query(Categoria).filter(
		Categoria.id == id_categoria).first()

	if not categoria_db:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail=f"Categoria com ID{id_categoria} não encontrado"
		)

	update_data = categoria_update.model_dump(exclude_unset=True)
	for campo, valor in update_data.items():
		print(campo, valor)
		setattr(categoria_db, campo, valor)

	db.commit()
	db.refresh(categoria_db)

	return success_response(
		data=CategoriaResponse.model_validate(categoria_db),
		message="Categoria atualizada com sucesso."
	)

@router.delete("/{id_categoria}", status_code=status.HTTP_204_NO_CONTENT)
def deleta_categoria(
	id_categoria: int,
	db: Session = Depends(get_db),
	require = Depends(allowed_roles("admin"))
):
	categoria_db = db.query(Categoria).filter(
		Categoria.id == id_categoria).first()
	if not categoria_db:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail=f"Categoria com ID{id_categoria} não encontrado"
		)

	db.delete(categoria_db)
	db.commit()

	return success_response(
		data=None,
		message="Categoria removida com sucesso.",
		status_code=status.HTTP_200_OK
	)
