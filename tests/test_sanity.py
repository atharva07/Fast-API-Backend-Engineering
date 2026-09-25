from types import SimpleNamespace

import pytest

from app.exceptions.auth import InvalidTokenError
from app.exceptions.project import ProjectNotFoundError
from app.exceptions.project_membership import ProjectAccessDeniedError
from app.main import root
from app.models.permission import Permission
from app.models.project import ProjectCreate
from app.models.role import UserRole
from app.security.authorization import get_project_membership, require_global_permission
from app.security.jwt import create_access_token, decode_access_token
from app.security.password import hash_password, verify_password
from app.security.permissions import ROLE_PERMISSIONS
from app.services.project import ProjectService


class FakeProjectRepository:
    def __init__(self, project=None):
        self.project = project
        self.added = []
        self.deleted = []

    def add(self, project):
        self.added.append(project)

    def get_by_id(self, project_id):
        if self.project is not None and self.project.id == project_id:
            return self.project
        return None

    def delete(self, project):
        self.deleted.append(project)


class FakeMembershipRepository:
    def __init__(self, membership=None):
        self.membership = membership
        self.request = None

    def get_membership(self, project_id, user_id):
        self.request = (project_id, user_id)
        return self.membership


class FakeUnitOfWork:
    def __init__(self, projects=None, membership=None):
        self.projects = FakeProjectRepository(projects)
        self.project_memberships = FakeMembershipRepository(membership)
        self.commits = 0
        self.rollbacks = 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            self.rollback()

    def commit(self):
        self.commits += 1

    def rollback(self):
        self.rollbacks += 1


def test_root_health_response():
    assert root() == {"message": "QAForge Backend is Running"}


def test_project_create_requires_a_name_at_least_three_characters():
    with pytest.raises(ValueError):
        ProjectCreate(name="ab")


def test_password_hash_round_trip_and_rejects_wrong_password():
    hashed_password = hash_password("correct horse battery staple")

    assert hashed_password != "correct horse battery staple"
    assert verify_password("correct horse battery staple", hashed_password)
    assert not verify_password("wrong password", hashed_password)


def test_access_token_round_trip():
    token = create_access_token(42)

    assert decode_access_token(token) == 42


def test_invalid_access_token_is_rejected():
    with pytest.raises(InvalidTokenError):
        decode_access_token("not-a-jwt")


def test_role_permissions_allow_admin_every_permission():
    assert ROLE_PERMISSIONS[UserRole.ADMIN] == set(Permission)


def test_global_permission_checker_rejects_role_without_permission():
    checker = require_global_permission(Permission.PROJECT_CREATE)
    viewer = SimpleNamespace(user_role=UserRole.VIEWER.value)

    with pytest.raises(ProjectAccessDeniedError):
        checker(current_user=viewer)


def test_project_membership_allows_admin_without_database_lookup():
    admin = SimpleNamespace(id=1, user_role=UserRole.ADMIN.value)
    unit_of_work = FakeUnitOfWork()

    assert get_project_membership(10, current_user=admin, uow=unit_of_work) is None
    assert unit_of_work.project_memberships.request is None


def test_project_membership_rejects_non_member():
    user = SimpleNamespace(id=7, user_role=UserRole.VIEWER.value)
    unit_of_work = FakeUnitOfWork()

    with pytest.raises(ProjectAccessDeniedError):
        get_project_membership(10, current_user=user, uow=unit_of_work)

    assert unit_of_work.project_memberships.request == (10, 7)


def test_project_service_create_adds_project_and_commits():
    unit_of_work = FakeUnitOfWork()
    service = ProjectService(unit_of_work)

    project = service.create_project("QA Platform", "Test management")

    assert project.name == "QA Platform"
    assert project.description == "Test management"
    assert unit_of_work.projects.added == [project]
    assert unit_of_work.commits == 1


def test_project_service_get_missing_project_raises_domain_error():
    service = ProjectService(FakeUnitOfWork())

    with pytest.raises(ProjectNotFoundError, match="Project Not Found"):
        service.get_project(999)
