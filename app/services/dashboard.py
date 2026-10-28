from app.db.unit_of_work import UnitOfWork
from app.models.dashboard import DashboardResponse
from app.models.role import UserRole
from app.cache.memory import get, set

class DashboardService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def get_dashboard(
        self,
        user_id: int,
        user_role: str,
    ) -> DashboardResponse:
        cache_key = f"dashboard:{user_id}"

        cached_dashboard = get(cache_key)

        if cached_dashboard is not None:
            print(
                f"Dashboard cache HIT: {cache_key}"
            )

            return cached_dashboard

        print(
            f"Dashboard cache MISS: {cache_key}"
        )

        is_admin = user_role == UserRole.ADMIN.value

        with self.uow:
            projects = self.uow.dashboard.count_projects(
                user_id=user_id, 
                is_admin=is_admin
            )

            test_suites = self.uow.dashboard.count_test_suites(
                user_id=user_id,
                is_admin=is_admin
            )

            test_cases = self.uow.dashboard.count_test_cases(
                user_id=user_id,
                is_admin=is_admin
            )

            executions = self.uow.dashboard.count_executions(
                user_id=user_id,
                is_admin=is_admin
            )

            dashboard = DashboardResponse(
                projects=projects,
                test_suites=test_suites,
                test_cases=test_cases,
                executions=executions,
            )

            set(
                cache_key,
                dashboard
            )
            return dashboard