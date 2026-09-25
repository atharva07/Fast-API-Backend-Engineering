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

"""
    In FastAPI when the request is received by the server along with authentication token (JWT), it needs to resolve the dependency 
    before executing the API Call received from the User. So Fast API Starts going down the dependency tree.
    Ex: In GET Projects API, we have current_user dependency which call require_project_permission. This returns permission_checker.
    Now conceptually, permission checker takes 2 arguments -> current_user and membership.
    So now FastAPI needs 2 things: get_current_user and get_project_membership

    get_current_user --> get_current_user_id, this will decode token, get user ID. At this point we have authenticated identity. 
    FastAPI will resolve get current user. 
    
    get_project_membership --> This will get resolved on the basis of project_id and current_user which we got from get_current_user method. 
    This will check if the user has access to a resource (project). get_membership will return the membership of user with project.

    Membership answers: Does this user belongs to this project ?
    Role/Permission answers: What can this user do ?

    (Here, we need both)

    So now, require_project_perission will check the permission is present in the Permissions for the particular role which user has. Here, we 
    have role QA_ENGINEER and required_permission as PROJECT_VIEW. So, it will check if the permission is present in set of permissions which QA has.

    Now, after resolving the dependency, FastAPI finally executes get_project method and return the project associated with the user.
"""


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
def get_project(project_id: int, current_user: User = Depends(require_project_permission(Permission.PROJECT_VIEW)), 
                uow: UnitOfWork = Depends(get_unit_of_work)):
    service = ProjectService(uow)

    return service.get_project(project_id)

"""
PUT Request
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
PATCH Request
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
DELETE Request
"""
@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int, current_user = Depends(require_project_permission(Permission.PROJECT_DELETE)), 
                   uow: UnitOfWork = Depends(get_unit_of_work)):    
    service = ProjectService(uow)

    service.delete_project(project_id=project_id)

    return Response(status_code=204)