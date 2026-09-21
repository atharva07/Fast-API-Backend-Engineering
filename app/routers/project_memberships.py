from fastapi import APIRouter, Depends, status
from app.db.dependencies import get_unit_of_work
from app.db.unit_of_work import UnitOfWork
from app.models.project_membership import ProjectMembership, ProjectMembershipResponse
from app.services.project_membership import ProjectMembershipService

router = APIRouter(
    prefix="/api/projects",
    tags=["Project Memberships"],
)

@router.post("/{project_id}/members", response_model=ProjectMembershipResponse, status_code=status.HTTP_201_CREATED)
def add_member(project_id: int, membership: ProjectMembership, uow: UnitOfWork = Depends(get_unit_of_work)):
    service = ProjectMembershipService(uow)

    return service.add_member(
        project_id=project_id,
        user_id=membership.user_id,
        role=membership.role.value
    )

@router.get("/{project_id}/members/{user_id}")
def get_membership(project_id: int, user_id: int, uow: UnitOfWork = Depends(get_unit_of_work)):
    service = ProjectMembershipService(uow)

    return service.get_membership(
        project_id=project_id,
        user_id=user_id
    )