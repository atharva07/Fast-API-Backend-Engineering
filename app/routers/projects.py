from fastapi import APIRouter, Depends, Response, status
from app.db.dependencies import get_unit_of_work
from app.db.unit_of_work import UnitOfWork
from app.models.project import (ProjectCreate, ProjectResponse, ProjectUpdate)
from app.services.project import ProjectService
from app.db.models.user import User
from app.security.dependencies import get_current_user
from app.security.authorization import get_project_membership
from app.security.authorization import require_project_permission, require_global_permission
from app.models.permission import Permission

router = APIRouter(
    prefix="/api/projects",
    tags=["Projects"],
)

"""
POST Request
"""
@router.post("/", response_model=ProjectResponse, status_code=201)
def create_project(project: ProjectCreate, current_user = Depends(require_global_permission(Permission.PROJECT_CREATE)), 
                   uow: UnitOfWork = Depends(get_unit_of_work)):
    service = ProjectService(uow)

    return service.create_project(
        name=project.name,
        description=project.description,
    )

"""
GET Request
"""
@router.get("/", response_model=list[ProjectResponse])
def get_all_projects(current_user: User = Depends(get_current_user), uow: UnitOfWork = Depends(get_unit_of_work)):
    service = ProjectService(uow)

    return service.get_project_for_users(
        user_id=current_user.id,
        current_user=current_user
    )

"""
GET by ID
"""
@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(project_id: int, current_user: User = Depends(require_project_permission(Permission.PROJECT_VIEW)), uow: UnitOfWork = Depends(get_unit_of_work)):
    service = ProjectService(uow)

    return service.get_project(project_id)

"""
PUT Reqest
"""
@router.put("/{project_id}", response_model=ProjectResponse)
def replace_project(project_id: int, project: ProjectCreate, current_user = Depends(require_project_permission(Permission.PROJECT_UPDATE)), 
                    uow: UnitOfWork = Depends(get_unit_of_work)):
    service = ProjectService(uow)

    return service.replace_project(
        project_id=project_id,
        name=project.name,
        description=project.description
    )

"""
PATCH
"""
@router.patch("/{project_id}", response_model=ProjectResponse)
def update_project(project_id: int, project: ProjectUpdate, current_user = Depends(require_project_permission(Permission.PROJECT_UPDATE)), 
                   uow: UnitOfWork = Depends(get_unit_of_work)):
    service = ProjectService(uow)

    return service.update_project(
        project_id=project_id,  
        name=project.name,
        description=project.description
    )

"""
DELETE
"""
@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int, current_user = Depends(require_project_permission(Permission.PROJECT_DELETE)), uow: UnitOfWork = Depends(get_unit_of_work)):    
    service = ProjectService(uow)

    service.delete_project(project_id=project_id)

    return Response(status_code=204)