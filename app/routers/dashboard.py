from fastapi import APIRouter, Depends
from app.db.dependencies import get_unit_of_work
from app.db.unit_of_work import UnitOfWork
from app.models.dashboard import DashboardResponse
from app.security.dependencies import get_current_user
from app.services.dashboard import DashboardService

router = APIRouter(
    prefix="/api/dashboard",
    tags=["Dashboard"],
)

@router.get("",response_model=DashboardResponse)
def get_dashboard(current_user = Depends(get_current_user), uow: UnitOfWork = Depends(get_unit_of_work)):
    service = DashboardService(uow)

    return service.get_dashboard(
        user_id=current_user.id,
        user_role=current_user.user_role,
    )