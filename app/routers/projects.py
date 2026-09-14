from fastapi import APIRouter, Depends
from app.db.dependencies import get_unit_of_work
from app.db.unit_of_work import UnitOfWork
from app.models.project import (
    ProjectCreate,
    ProjectResponse
)
from app.services.project import ProjectService

router = APIRouter(
    prefix="/api/projects",
    tags=["Projects"],
)
@router.post(
    "/",
    response_model=ProjectResponse,
    status_code=201
)
def create_project(
    project: ProjectCreate,
    uow: UnitOfWork = Depends(get_unit_of_work)
):
    service = ProjectService(uow)

    return service.create_project(
        name=project.name,
        description=project.description,
    )