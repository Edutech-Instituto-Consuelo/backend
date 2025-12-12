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
    CursoEstatisticaItem,
)
from typing import Literal

from app.core.security import allowed_roles  # ⬅️ vem do security.py


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
    usuario: dict = Depends(allowed_roles("instrutor", "admin")),
):
    """
    POST /courses

    Criar novo curso (somente instrutor ou admin).

    Regras:
    - status default ⇒ rascunho (ainda não temos coluna no model, fica como TODO)
    - se a role for admin, pode criar curso para qualquer/nenhum instrutor
    - se a role for instrutor, id_instrutor = id do usuário logado
    """
    user_id = usuario["id"]
    role = usuario["role"]

    # Se for instrutor, força ser o próprio instrutor
    if role == "instrutor":
        curso_in.id_instrutor = user_id

    # Se for admin, id_instrutor precisa ser informado (colado com model, que não aceita NULL)
    if curso_in.id_instrutor is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="id_instrutor é obrigatório para administradores.",
        )

    novo_curso = Curso(
        titulo=curso_in.titulo,
        descricao=curso_in.descricao,
        categoria_id=curso_in.id_categoria,
        nivel_id=curso_in.id_nivel,
        instrutor_id=curso_in.id_instrutor,
        preco=curso_in.preco if curso_in.preco is not None else 0.0,
        carga_horaria=1,
        #carga_horaria=curso_in.carga_horaria if hasattr(curso_in, "carga_horaria") else 0,
    )

    db.add(novo_curso)
    db.commit()
    db.refresh(novo_curso)

    return CursoControleResponse(
        id=novo_curso.id,
        titulo=novo_curso.titulo,
        descricao=novo_curso.descricao,
        id_categoria=novo_curso.categoria_id,
        id_nivel=novo_curso.nivel_id,
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
    usuario: dict = Depends(allowed_roles("instrutor", "admin")),
):
    """
    PUT /courses/{id}

    Editar curso (somente se for o instrutor atual ou admin).

    Regras:
    - id do body deve bater com id da URL
    - instrutor só pode editar cursos em que ele é o instrutor
    - admin pode editar qualquer curso e trocar o instrutor
    """
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

    # Atualiza campos básicos
    curso_db.titulo = curso_in.titulo
    curso_db.descricao = curso_in.descricao
    curso_db.categoria_id = curso_in.id_categoria
    curso_db.nivel_id = curso_in.id_nivel
    curso_db.preco = curso_in.preco if curso_in.preco is not None else 0.0

    # Atualiza instrutor conforme role
    if role == "admin":
        # admin pode trocar o instrutor
        if curso_in.id_instrutor is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="id_instrutor é obrigatório para administradores.",
            )
        curso_db.instrutor_id = curso_in.id_instrutor
    else:
        # instrutor sempre continua sendo ele próprio
        curso_db.instrutor_id = user_id

    db.commit()
    db.refresh(curso_db)

    return CursoControleResponse(
        id=curso_db.id,
        titulo=curso_db.titulo,
        descricao=curso_db.descricao,
        id_categoria=curso_db.categoria_id,
        id_nivel=curso_db.nivel_id,
        id_instrutor=curso_db.instrutor_id,
        preco=curso_db.preco,
        sobre=0.0,  # TODO: recalcular média
    )

@router.delete(
    "/{curso_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def deletar_curso(
    curso_id: int,
    db: Session = Depends(get_db),
    usuario: dict = Depends(allowed_roles("instrutor", "admin")),
):
    """
    DELETE /courses/{id}

    Regras:
    - Somente instrutor dono do curso ou admin
    - Só pode deletar se o curso estiver como 'rascunho'
      (regra atual: curso sem módulos associados)
    - Hard delete
    """
    user_id = usuario["id"]
    role = usuario["role"]

    curso_db: Curso | None = db.query(Curso).filter(Curso.id == curso_id).first()
    if not curso_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Curso não encontrado.",
        )

    # Permissão: instrutor só pode deletar seus cursos
    if role == "instrutor" and curso_db.instrutor_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para excluir este curso.",
        )

    # Regra de rascunho: curso sem módulos associados
    if curso_db.modulos and len(curso_db.modulos) > 0:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Curso não pode ser deletado porque já possui módulos (não é mais rascunho).",
        )

    db.delete(curso_db)
    db.commit()
    return

@router.get(
    "/{curso_id}/statistics",
    response_model=List[CursoEstatisticaItem],
)
def estatisticas_curso(
    curso_id: int,
    db: Session = Depends(get_db),
    usuario: dict = Depends(allowed_roles("instrutor", "admin")),
):
    """
    GET /courses/{id}/statistics

    Retorna estatísticas consolidadas do curso:
    - categoria / nível / instrutor
    - média das avaliações
    - quantidade de alunos matriculados
    - percentual médio de conclusão (real, baseado no progresso das aulas)
    - datas de criação / publicação (publicação ainda não existe → retorna None)
    """

    # Buscar o curso
    curso = db.query(Curso).filter(Curso.id == curso_id).first()
    if not curso:
        raise HTTPException(status_code=404, detail="Curso não encontrado.")

    # Categoria, nível, instrutor
    categoria = curso.categoria.descricao if curso.categoria else ""
    nivel = curso.nivel.descricao if curso.nivel else ""
    instrutor = curso.instrutor.usuario.nome if curso.instrutor else ""

    # Média das avaliações (AvaliacaoCurso)
    media_notas = (
        db.query(func.avg(AvaliacaoCurso.nota))
        .filter(AvaliacaoCurso.curso_id == curso_id)
        .scalar()
    )
    media_notas = float(media_notas) if media_notas else 0.0

    # Quantidade de alunos (usando relacionamento curso.matriculas)
    matriculas = curso.matriculas or []
    quantidade_alunos = len(matriculas)

    # Total de aulas do curso (modulos → aulas, via relacionamento)
    total_aulas = 0
    for modulo in curso.modulos or []:
        # cada módulo deve ter relationship "aulas"
        total_aulas += len(modulo.aulas or [])

    # Percentual médio de conclusão REAL
    percentual_medio = 0.0

    if quantidade_alunos > 0 and total_aulas > 0:
        percentuais = []

        for matricula in matriculas:
            progresso = matricula.progresso_aulas or []

            if not progresso:
                percentuais.append(0.0)
                continue

            aulas_concluidas = sum(1 for p in progresso if p.concluido)
            percentual = (aulas_concluidas / total_aulas) * 100
            percentuais.append(percentual)

        if percentuais:
            percentual_medio = sum(percentuais) / len(percentuais)

    # Montar resposta (ARRAY, conforme contrato do front)
    return [
        CursoEstatisticaItem(
            id=curso.id,
            titulo=curso.titulo,
            id_categoria=curso.categoria_id,
            categoria=categoria,
            id_nivel=curso.nivel_id,
            nivel=nivel,
            id_instrutor=curso.instrutor_id,
            instrutor=instrutor,
            percentual_conclusao=percentual_medio,
            media_notas=media_notas,
            quantidade_alunos=quantidade_alunos,
            data_criacao=curso.data_criacao,
            data_publicacao=None,  # ainda não existe no model
        )
    ]
