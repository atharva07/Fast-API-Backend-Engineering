import math
from app.models.test_result import PaginatedTestResultResponse, TestResultStatus
from app.db.unit_of_work import UnitOfWork
from app.db.models.test_result import TestResult
from app.exceptions.test_result import TestResultNotFoundError
from app.exceptions.test_case import TestCaseNotFoundError

class TestResultService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def get_results_by_test_case(self, test_case_id: int) -> list[TestResult]:
        with self.uow:
            test_case = self.uow.test_cases.get_by_id(test_case_id)

            if test_case is None:
                raise TestCaseNotFoundError("Test Case not found Error")

            return self.uow.test_results.get_by_test_case(test_case_id)

    def get_results(self, result_id: int) -> TestResult:
        with self.uow:
            result = self.uow.test_results.get_by_id(result_id)

            if result is None:
                raise TestResultNotFoundError("Test Result Not Found")

            return result

    def get_results_page(self, page: int, page_size: int, status: TestResultStatus | None = None, test_case_id: int | None = None) -> PaginatedTestResultResponse:
        offset = (page - 1) * page_size

        with self.uow:
            results = self.uow.test_results.get_page(offset=offset, limit=page_size, status=status, test_case_id=test_case_id)
            total = self.uow.test_results.count_all(status=status, test_case_id=test_case_id)
            total_pages = math.ceil(total / page_size)

            return PaginatedTestResultResponse(
                items=results,
                page=page,
                page_size=page_size,
                total=total,
                total_pages=total_pages
            )

    def get_all_results(self) -> list[TestResult]:
        with self.uow:
            return self.uow.test_results.get_all()