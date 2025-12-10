from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.course import Curso
from app.models.course_request import CourseRequest
from app.dependencies.auth import allowed_roles


router = APIRouter(
	prefix="/courses",
	tags=["courses"]
)


@router.post("/{course_id}/request-publish", status_code=status.HTTP_201_CREATED)
def request_publish(course_id: int, current_user = Depends(allowed_roles("instructor"), db: Session = Depends(get_db))):
	"""Instrutor pede para publicar o curso"""

	course = db.query(Curso).filter(Curso.id == course_id).first()

	if not course:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="Curso não encontrado")

	if course.instructor_id != current_user.id:
		raise HTTPException(
			status_code=status.HTTP_403_FORBIDDEN,
			detail="Você não é o instrutor responsável por este curso")

	request_obj = CourseRequest(
		course_id=course.id,
		requester_id=current_user.id,
		request_type="publish")

	db.add(request_obj)
	db.commit()
	db.refresh(request_obj)

	return {"message": "Solicitação de publicação criada com sucesso"}


@router.post("/{course_id}/request-unpublish", status_code=status.HTTP_201_CREATED)
def request_unpublish(course_id: int, current_user = Depends(allowed_roles("instructor"), db: Session = Depends(get_db))):
	"""Instrutor pede para despublicar o curso"""

	course = db.query(Curso).filter(Curso.id == course_id).first()

	if not course:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="Curso não encontrado"
		)

	if course.instructor_id != current_user.id:
		raise HTTPException(
			status_code=status.HTTP_403_FORBIDDEN,
			detail="Você não é o instrutor responsável por este curso"
		)

	request_obj = CourseRequest(
		course_id=course.id,
		requester_id=current_user.id,
		request_type="unpublish"
	)

	db.add(request_obj)
	db.commit()
	db.refresh(request_obj)

	return {"message": "Solicitação de despublicação criada com sucesso"}
