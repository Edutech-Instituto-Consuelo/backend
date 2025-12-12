from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.database import get_db
from app.core.security import allowed_roles
from app.models.enrollment import Matricula
from app.models.progress import ProgressoAulas
from app.models.course import Curso
from app.models.user import Usuario
from app.models.lesson import Aula
from app.models.module import Modulo
from app.models.instructor import Instrutor
from typing import List, Optional
from datetime import datetime

router = APIRouter(
    prefix="/enrollments",
    tags=["Enrollments"]
)


# Função auxiliar para checar autorização de acesso à matrícula
def check_enrollment_access(matricula: Matricula, usuario: dict, db: Session, resource: str = "enrollment") -> bool:
    """
    Verifica se o usuário tem permissão para acessar a matrícula.
    
    Args:
        matricula: Objeto da matrícula
        usuario: Dict com dados do usuário autenticado (id, role)
        db: Sessão do banco
        resource: Tipo de recurso para mensagem de erro
    
    Returns:
        True se tem acesso, lança HTTPException caso contrário
    """
    role = usuario.get("role")
    user_id = usuario.get("id")

    if role == "admin":
        return True

    if role == "aluno":
        if matricula.aluno_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Acesso negado a este {resource}"
            )
        return True

    # instrutor
    if role == "instrutor":
        curso = db.query(Curso).filter(Curso.id == matricula.curso_id).first()
        if not curso or curso.instrutor_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Acesso negado a este {resource}"
            )
        return True

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=f"Acesso negado a este {resource}"
    )


# Função auxiliar para serializar matricula com dados do aluno, curso e instrutor
def serialize_enrollment(matricula: Matricula, db: Session) -> dict:
    """Serializa uma matrícula em um dicionário com dados completos"""
    aluno = db.query(Usuario).filter(Usuario.id == matricula.aluno_id).first()
    curso = db.query(Curso).filter(Curso.id == matricula.curso_id).first()
    instrutor = db.query(Instrutor).filter(Instrutor.id == curso.instrutor_id).first()
    usuario_instrutor = db.query(Usuario).filter(Usuario.id == instrutor.id).first() if instrutor else None

    return {
        "id": matricula.id,
        "id_aluno": matricula.aluno_id,
        "aluno": f"{aluno.nome} {aluno.sobrenome}" if aluno else "",
        "id_curso": matricula.curso_id,
        "curso": curso.titulo if curso else "",
        "id_instrutor": curso.instrutor_id if curso else None,
        "instrutor": f"{usuario_instrutor.nome} {usuario_instrutor.sobrenome}" if usuario_instrutor else "",
        "status_matricula": matricula.status_matricula,
        "data_conclusao": matricula.data_conclusao
    }


@router.get("", response_model=List[dict])
def list_enrollments(
    id_curso: Optional[int] = None,
    id_aluno: Optional[int] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    usuario=Depends(allowed_roles("aluno", "instrutor", "admin"))
):
    """
    Lista matrículas com filtros opcionais.
    
    - Aluno: vê apenas suas próprias matrículas
    - Instrutor: vê matrículas dos alunos em seus cursos
    - Admin: vê todas as matrículas
    
    Query params:
    - id_curso: filtrar por curso
    - id_aluno: filtrar por aluno
    - status: filtrar por status da matrícula
    """
    role = usuario.get("role")
    user_id = usuario.get("id")

    # Query base
    query = db.query(Matricula)

    # Aplicar filtros por role
    if role == "aluno":
        query = query.filter(Matricula.aluno_id == user_id)
    elif role == "instrutor":
        # Buscar cursos do instrutor e filtrar matrículas desses cursos
        curso_ids = [c.id for c in db.query(Curso).filter(Curso.instrutor_id == user_id).all()]
        if not curso_ids:
            return []
        query = query.filter(Matricula.curso_id.in_(curso_ids))

    # Aplicar filtros fornecidos
    if id_curso is not None:
        query = query.filter(Matricula.curso_id == id_curso)
    if id_aluno is not None:
        # Instrutor só pode filtrar alunos de seus cursos
        if role == "instrutor":
            curso_ids = [c.id for c in db.query(Curso).filter(Curso.instrutor_id == user_id).all()]
            query = query.filter(and_(Matricula.aluno_id == id_aluno, Matricula.curso_id.in_(curso_ids)))
        elif role == "aluno":
            # Aluno só pode ver a si mesmo
            query = query.filter(Matricula.aluno_id == user_id)
        else:
            # Admin pode ver qualquer aluno
            query = query.filter(Matricula.aluno_id == id_aluno)
    if status is not None:
        query = query.filter(Matricula.status_matricula == status)

    matriculas = query.all()
    return [serialize_enrollment(m, db) for m in matriculas]


@router.get("/{enrollment_id}/progress")
def get_enrollment_progress(
    enrollment_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(allowed_roles("aluno", "instrutor", "admin"))
):
    """
    Retorna o progresso completo de uma matrícula, incluindo:
    - Percentual geral do curso
    - Lista de aulas com seus status e progresso
    
    Autorização:
    - Aluno: apenas suas próprias matrículas
    - Instrutor: apenas matrículas de seus cursos
    - Admin: qualquer matrícula
    """
    matricula = db.query(Matricula).filter(Matricula.id == enrollment_id).first()
    if not matricula:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Matrícula não encontrada"
        )

    # Verificar autorização
    check_enrollment_access(matricula, usuario, db, "matrícula")

    # Dados básicos da matrícula
    aluno = db.query(Usuario).filter(Usuario.id == matricula.aluno_id).first()
    curso = db.query(Curso).filter(Curso.id == matricula.curso_id).first()
    instrutor = db.query(Instrutor).filter(Instrutor.id == curso.instrutor_id).first()
    usuario_instrutor = db.query(Usuario).filter(Usuario.id == instrutor.id).first() if instrutor else None

    # Buscar todos os módulos e aulas do curso
    modulos = db.query(Modulo).filter(Modulo.curso_id == matricula.curso_id).order_by(Modulo.ordem).all()

    # Preparar lista de aulas com progresso
    aulas_list = []
    total_aulas = 0
    aulas_concluidas = 0

    for modulo in modulos:
        aulas = db.query(Aula).filter(Aula.modulo_id == modulo.id).order_by(Aula.ordem_aula).all()
        
        for aula in aulas:
            total_aulas += 1
            
            # Buscar progresso dessa aula para essa matrícula
            progresso = db.query(ProgressoAulas).filter(
                and_(
                    ProgressoAulas.matricula_id == enrollment_id,
                    ProgressoAulas.aula_id == aula.id
                )
            ).first()

            if progresso:
                if progresso.concluido:
                    aulas_concluidas += 1
                progresso_percentual = progresso.progresso_percentual
                data_conclusao_aula = progresso.data_conclusao
            else:
                progresso_percentual = 0
                data_conclusao_aula = None

            aulas_list.append({
                "id_aula": aula.id,
                "titulo_aula": aula.titulo,
                "ordem_aula": aula.ordem_aula,
                "id_modulo": modulo.id,
                "titulo_modulo": modulo.titulo,
                "ordem_modulo": modulo.ordem,
                "progresso_aula": progresso_percentual,
                "concluido": progresso.concluido if progresso else False,
                "data_conclusao": data_conclusao_aula
            })

    # Calcular percentual do curso
    progresso_curso = (aulas_concluidas / total_aulas * 100) if total_aulas > 0 else 0

    return {
        "id": matricula.id,
        "id_aluno": matricula.aluno_id,
        "aluno": f"{aluno.nome} {aluno.sobrenome}" if aluno else "",
        "id_curso": matricula.curso_id,
        "curso": curso.titulo if curso else "",
        "id_instrutor": curso.instrutor_id if curso else None,
        "instrutor": f"{usuario_instrutor.nome} {usuario_instrutor.sobrenome}" if usuario_instrutor else "",
        "status_matricula": matricula.status_matricula,
        "data_conclusao": matricula.data_conclusao,
        "progresso_curso": round(progresso_curso, 2),
        "aulas": aulas_list
    }


@router.post("", status_code=status.HTTP_201_CREATED)
def create_enrollment(
    payload: dict,
    db: Session = Depends(get_db),
    usuario=Depends(allowed_roles("aluno", "instrutor", "admin"))
):
    """
    Cria uma nova matrícula.
    
    Request:
    {
        "id_curso": int
    }
    
    - Aluno: matricula-se a si mesmo
    - Instrutor/Admin: podem matricular qualquer aluno
    
    Regras:
    - Não permite matrícula duplicada (ativa) no mesmo curso
    - Curso deve existir
    """
    role = usuario.get("role")
    user_id = usuario.get("id")

    id_curso = payload.get("id_curso")

    if not id_curso:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Campo 'id_curso' é obrigatório"
        )

    # Verificar se curso existe
    curso = db.query(Curso).filter(Curso.id == id_curso).first()
    if not curso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Curso não encontrado"
        )

    # Determinar id_aluno
    if role == "aluno":
        id_aluno = user_id
    else:
        # Instrutor/Admin precisam especificar o aluno no payload
        id_aluno = payload.get("id_aluno")
        if not id_aluno:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Campo 'id_aluno' é obrigatório para instrutor/admin"
            )

    # Verificar se aluno existe
    aluno = db.query(Usuario).filter(Usuario.id == id_aluno).first()
    if not aluno:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aluno não encontrado"
        )

    # Evitar duplicidade de matrícula ativa
    existente = db.query(Matricula).filter(
        and_(
            Matricula.curso_id == id_curso,
            Matricula.aluno_id == id_aluno,
            Matricula.status_matricula == "ativa"
        )
    ).first()

    if existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Aluno já possui matrícula ativa neste curso"
        )

    # Criar nova matrícula
    nova_matricula = Matricula(
        aluno_id=id_aluno,
        curso_id=id_curso,
        status_matricula="ativa"
    )

    db.add(nova_matricula)
    db.commit()
    db.refresh(nova_matricula)

    return serialize_enrollment(nova_matricula, db)


@router.delete("/{enrollment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_enrollment(
    enrollment_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(allowed_roles("aluno", "instrutor", "admin"))
):
    """
    Cancela uma matrícula (soft delete).
    
    Autorização:
    - Aluno: apenas suas próprias matrículas
    - Instrutor: apenas matrículas de seus cursos
    - Admin: qualquer matrícula
    
    Response: 204 No Content
    """
    matricula = db.query(Matricula).filter(Matricula.id == enrollment_id).first()
    if not matricula:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Matrícula não encontrada"
        )

    # Verificar autorização
    check_enrollment_access(matricula, usuario, db, "matrícula")

    # Soft delete: marcar como cancelada
    matricula.status_matricula = "cancelada"
    db.commit()


@router.patch("/{enrollment_id}/classes/{class_id}/toggle", status_code=status.HTTP_204_NO_CONTENT)
def toggle_class(
    enrollment_id: int,
    class_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(allowed_roles("aluno", "instrutor", "admin"))
):
    """
    Alterna o status de conclusão de uma aula (marcar/desmarcar concluída).
    
    Autorização:
    - Aluno: apenas suas próprias matrículas
    - Instrutor: apenas matrículas de seus cursos
    - Admin: qualquer matrícula
    
    Lógica:
    - Se não existe registro de progresso, cria um novo (marcado como concluído)
    - Se existe e está concluído, marca como não concluído
    - Se existe e não está concluído, marca como concluído
    
    Response: 204 No Content
    """
    # Verificar se matrícula existe
    matricula = db.query(Matricula).filter(Matricula.id == enrollment_id).first()
    if not matricula:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Matrícula não encontrada"
        )

    # Verificar autorização
    check_enrollment_access(matricula, usuario, db, "matrícula")

    # Verificar se aula existe
    aula = db.query(Aula).filter(Aula.id == class_id).first()
    if not aula:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aula não encontrada"
        )

    # Buscar ou criar progresso
    progresso = db.query(ProgressoAulas).filter(
        and_(
            ProgressoAulas.matricula_id == enrollment_id,
            ProgressoAulas.aula_id == class_id
        )
    ).first()

    if not progresso:
        # Criar novo registro como concluído
        progresso = ProgressoAulas(
            matricula_id=enrollment_id,
            aula_id=class_id,
            progresso_percentual=100,
            concluido=True,
            data_conclusao=datetime.utcnow()
        )
        db.add(progresso)
    else:
        # Toggle: inverte o status
        progresso.concluido = not progresso.concluido
        if progresso.concluido:
            progresso.progresso_percentual = 100
            progresso.data_conclusao = datetime.utcnow()
        else:
            progresso.progresso_percentual = 0
            progresso.data_conclusao = None

    db.commit()