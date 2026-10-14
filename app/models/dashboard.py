from pydantic import BaseModel

class DashboardResponse(BaseModel):
    projects: int
    test_suites: int
    test_cases: int
    executions: int