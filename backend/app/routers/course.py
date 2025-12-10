from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import func

from app.database import get_db
from app.models.course import Curso
from app.models.level import Nivel
from app.models.instructor import Instrutor
from app.models.evaluation import AvaliacaoCurso

from app.schemas.course import CursoResponse, CursoEspecificoResponse
from typing import Literal




router = APIRouter(
	prefix="/courses",
	tags=["courses"]
)

precoList = Literal["pago", "gratuito"]

@router.get("",response_model=List[CursoResponse])
def listar_cursos(
	id_categoria: int = 0,
	id_nivel: int = 0,
	preco: precoList | None = None,
	db: Session = Depends(get_db)
):
	"""Retorna as informações do curso"""

	resultados = (
		db.query(
			Curso,
			func.coalesce(func.avg(AvaliacaoCurso.nota), 0).label("avaliacao_media"),
			func.count(AvaliacaoCurso.id).label("quantidade_avaliacoes"),
		)
		.outerjoin(AvaliacaoCurso, AvaliacaoCurso.curso_id == Curso.id)  # LEFT JOIN, pra trazer curso sem avaliação também
		.group_by(Curso.id)
		.all()
	)
	resposta = []
	for curso, avaliacao_media, qtd_avaliacoes in resultados:
		resposta.append(
			CursoResponse(
				id=curso.id,
				url_image=getattr(curso, "url_image", None),
				titulo=curso.titulo,
				id_instrutor=curso.instrutor_id,
				instrutor=curso.instrutor.usuario.nome,
				id_nivel=curso.nivel_id,
				nivel=curso.nivel.descricao,
				avaliacao=float(avaliacao_media or 0.0),
				quantidade_avaliacoes=int(qtd_avaliacoes or 0),
				preco=curso.preco or 0.0,
			)
		)

	return resposta


@router.get("/{id_curso}", response_model=CursoEspecificoResponse)
def pegar_curso(
	id_curso: int,
	db: Session = Depends(get_db)
):
	"""Pega curso especifico"""
	resultado = (
		db.query(
			Curso,
			func.coalesce(func.avg(AvaliacaoCurso.nota), 0).label("avaliacao_media"),
			func.count(AvaliacaoCurso.id).label("quantidade_avaliacoes"),
		)
		.outerjoin(AvaliacaoCurso, AvaliacaoCurso.curso_id == Curso.id)  # LEFT JOIN pra funcionar mesmo sem avaliações
		.filter(Curso.id == id_curso)
		.group_by(Curso.id)
		.first()
	)
	if not resultado:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail=f"Curso com id {id_curso}, não encontado"
		)
	curso, avaliacao_media, qtd_avaliacoes = resultado
	return CursoEspecificoResponse(
		id=curso.id,
		titulo=curso.titulo,
		descricao=curso.descricao,
		avaliacao=float(avaliacao_media or 0.0),
		quantidade_avaliacoes=int(qtd_avaliacoes or 0),
		quantidade_horas=curso.carga_horaria,
		id_nivel=curso.nivel_id,
		nivel=curso.nivel.descricao,
		preco=curso.preco,
		id_instrutor=curso.instrutor_id,
		instrutor=curso.instrutor.usuario.nome,
		id_especialidade=curso.instrutor.especialidade,
		especialidade_instrutor=curso.instrutor.especialidade_rel.nome,
	)
