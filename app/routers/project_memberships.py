from fastapi import APIRouter, Depends, status
from app.db.dependencies import get_unit_of_work
from app.db.unit_of_work import UnitOfWork
from app.models.project_membership import ProjectMembership, ProjectMembershipResponse
from app.services.project_membership import ProjectMembershipService
from app.db.models.user import User
from app.security.authorization import require_global_permission
from app.models.permission import Permission

router = APIRouter(
    prefix="/api/projects",
    tags=["Project Memberships"],
)

@router.post("/{project_id}/members", response_model=ProjectMembershipResponse, status_code=status.HTTP_201_CREATED)
def add_member(project_id: int, membership: ProjectMembership, 
               current_user: User = Depends(require_global_permission(Permission.MEMBER_MANANGE)),
               uow: UnitOfWork = Depends(get_unit_of_work)):
    service = ProjectMembershipService(uow)

    return service.add_member(
        project_id=project_id,
        user_id=membership.user_id,
    )

@router.get("/{project_id}/members/{user_id}")
def get_membership(project_id: int, user_id: int, 
                   current_user: User = Depends(require_global_permission(Permission.MEMBER_VIEW)),
                   uow: UnitOfWork = Depends(get_unit_of_work)):
    service = ProjectMembershipService(uow)

    return service.get_membership(
        project_id=project_id,
        user_id=user_id
    )