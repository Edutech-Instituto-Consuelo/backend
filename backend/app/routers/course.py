from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import func

from app.database import get_db
from app.models.course import Curso
from app.models.level import Nivel
from app.models.instructor import Instrutor
from app.models.evaluation import AvaliacaoCurso

from app.schemas.course import (
    CursoResponse,
    CursoEspecificoResponse,
    CursoControleCriar,
    CursoControleAtualizar,
    CursoControleResponse,
    CursoEstatisticaItem,  # usar pra /statistics
)
from typing import Literal

from app.core.security import allowed_roles  # ⬅️ vem do security.py

LEVEL_ID_TO_TEXT = {
    1: "Iniciante",
    2: "Intermediário",
    3: "Avançado",
}

LEVEL_TEXT_TO_ID = {value: key for key, value in LEVEL_ID_TO_TEXT.items()}


router = APIRouter(
	prefix="/courses",
	tags=["courses"]
)

precoList = Literal["pago", "gratuito"]

def _garantir_instrutor_ou_admin(usuario: dict) -> None:
    """
    Garante que apenas instrutores ou admins possam usar
    os endpoints de controle de cursos.
    """
    if usuario.get("role") not in ("instrutor", "admin"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso proibido! Apenas instrutores ou administradores podem gerenciar cursos.",
        )


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

@router.post(
    "",
    response_model=CursoControleResponse,
    status_code=status.HTTP_201_CREATED,
)
def criar_curso(
    curso_in: CursoControleCriar,
    db: Session = Depends(get_db),
    usuario: dict = Depends(allowed_roles()),
):
    """
    POST /courses

    Criar novo curso (somente instrutor ou admin).

    Regras:
    - status default ⇒ rascunho (ainda não temos coluna no model, fica como TODO)
    - se a role for admin, pode criar curso para qualquer/nenhum instrutor
    - se a role for instrutor, id_instrutor = id do usuário logado
    """
    _garantir_instrutor_ou_admin(usuario)

    user_id = usuario["id"]
    role = usuario["role"]

    # Regra do instrutor:
    if role == "instrutor":
        curso_in.id_instrutor = user_id

    # Converter id_nivel (int) -> nivel (texto) salvo no model
    nivel_texto = LEVEL_ID_TO_TEXT.get(curso_in.id_nivel)
    if not nivel_texto:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="id_nivel inválido. Use um dos níveis configurados.",
        )

    novo_curso = Curso(
        titulo=curso_in.titulo,
        # 'sobre' equivale à descrição -> priorizamos sobre, se vier preenchido
        descricao=curso_in.sobre or curso_in.descricao,
        categoria_id=curso_in.id_categoria,
        instrutor_id=curso_in.id_instrutor,
        preco=curso_in.preco if curso_in.preco is not None else 0.0,
        carga_horaria=curso_in.carga_horaria if hasattr(curso_in, "carga_horaria") else 0,
        nivel=nivel_texto,
    )
    # OBS: não temos campo 'status' no model ainda → TODO futura migration

    db.add(novo_curso)
    db.commit()
    db.refresh(novo_curso)

    # Converter o texto salvo de volta para o id_nivel pra resposta
    id_nivel_resp = LEVEL_TEXT_TO_ID.get(novo_curso.nivel, curso_in.id_nivel)

    return CursoControleResponse(
        id=novo_curso.id,
        titulo=novo_curso.titulo,
        descricao=novo_curso.descricao,
        sobre=0.0,  # por enquanto, sem avaliações -> média 0
        id_categoria=novo_curso.categoria_id,
        id_nivel=id_nivel_resp,
        id_instrutor=novo_curso.instrutor_id,
        preco=novo_curso.preco,
    )



@router.put(
    "/{curso_id}",
    response_model=CursoControleResponse,
)
def atualizar_curso(
    curso_id: int,
    curso_in: CursoControleAtualizar,
    db: Session = Depends(get_db),
    usuario: dict = Depends(allowed_roles()),
):
    """
    PUT /courses/{id}

    Editar curso (somente se for o instrutor atual ou admin).
    """
    _garantir_instrutor_ou_admin(usuario)

    user_id = usuario["id"]
    role = usuario["role"]

    if curso_in.id != curso_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID do corpo da requisição é diferente do ID da URL.",
        )

    curso_db: Curso | None = db.query(Curso).filter(Curso.id == curso_id).first()
    if not curso_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Curso não encontrado.",
        )

    # Permissão: instrutor só pode editar os cursos dele
    if role == "instrutor" and curso_db.instrutor_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para editar este curso.",
        )

    # Converter id_nivel -> texto
    nivel_texto = LEVEL_ID_TO_TEXT.get(curso_in.id_nivel)
    if not nivel_texto:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="id_nivel inválido. Use um dos níveis configurados.",
        )

    curso_db.titulo = curso_in.titulo
    curso_db.descricao = curso_in.sobre or curso_in.descricao
    curso_db.categoria_id = curso_in.id_categoria
    curso_db.preco = curso_in.preco if curso_in.preco is not None else 0.0
    curso_db.nivel = nivel_texto

    if role == "admin":
        curso_db.instrutor_id = curso_in.id_instrutor
    else:
        curso_db.instrutor_id = user_id

    db.commit()
    db.refresh(curso_db)

    id_nivel_resp = LEVEL_TEXT_TO_ID.get(curso_db.nivel, curso_in.id_nivel)

    return CursoControleResponse(
        id=curso_db.id,
        titulo=curso_db.titulo,
        descricao=curso_db.descricao,
        sobre=curso_db.descricao,
        id_categoria=curso_db.categoria_id,
        id_nivel=id_nivel_resp,
        id_instrutor=curso_db.instrutor_id,
        preco=curso_db.preco,
    )

