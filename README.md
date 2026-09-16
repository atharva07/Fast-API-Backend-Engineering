# Fast-API-Backend-Engineering

# Database Schema
users
----------------
    id
    name
    email
    password_hash

projects
----------------
    id
    name
    description

test_cases
----------------
    id
    name
    description
    status
    project_id
    created_by

test_results
----------------
    id
    test_case_id
    status
    executed_at

Relationship

        users
        │
        │
        └────────< test_cases
                        │
                        │
        projects ─────────┘
            │
            │
            └────────< test_cases
                            │
                            │
                            └──────< test_results


Current Database looks like below conceptually

                        ┌──────────────┐
                        │    USERS     │
                        ├──────────────┤
                        │ id           │
                        │ name         │
                        │ email        │
                        │ password_hash│
                        └──────┬───────┘
                               │
                               │ created_by
                               ▼
        ┌──────────────┐  ┌──────────────┐
        │   PROJECTS   │  │  TEST_CASES  │
        ├──────────────┤  ├──────────────┤
        │ id           │◄─┤ project_id   │
        │ name         │  │ id           │
        │ description  │  │ name         │
        └──────────────┘  │ description  │
                          │ status       │
                          │ created_by   │
                          └──────┬───────┘
                                 │
                                 │ test_case_id
                                 ▼
                        ┌──────────────┐
                        │ TEST_RESULTS │
                        ├──────────────┤
                        │ id           │
                        │ test_case_id │
                        │ status       │
                        │ executed_at  │
                        └──────────────┘

# QAForge API Collection Schema

                QAForge API
                │
                ├── Health
                │   └── GET    /health
                │
                ├── Auth
                │   ├── POST   /api/auth/register
                │   ├── POST   /api/auth/login
                │   ├── POST   /api/auth/refresh
                │   ├── POST   /api/auth/logout
                │   └── GET    /api/auth/me
                │
                ├── Users
                │   ├── POST   /api/users
                │   ├── GET    /api/users
                │   ├── GET    /api/users/{id}
                │   ├── PATCH  /api/users/{id}
                │   └── DELETE /api/users/{id}
                │
                ├── Projects
                │   ├── POST   /api/projects
                │   ├── GET    /api/projects
                │   ├── GET    /api/projects/{id}
                │   ├── PUT    /api/projects/{id}
                │   ├── PATCH  /api/projects/{id}
                │   └── DELETE /api/projects/{id}
                │
                ├── Project Members
                │   ├── GET    /api/projects/{id}/members
                │   ├── POST   /api/projects/{id}/members
                │   ├── PATCH  /api/projects/{id}/members/{user_id}
                │   └── DELETE /api/projects/{id}/members/{user_id}
                │
                ├── Test Suites
                │   ├── POST   /api/projects/{id}/suites
                │   ├── GET    /api/projects/{id}/suites
                │   ├── GET    /api/suites/{id}
                │   ├── PUT    /api/suites/{id}
                │   ├── PATCH  /api/suites/{id}
                │   └── DELETE /api/suites/{id}
                │
                ├── Test Cases
                │   ├── POST   /api/projects/{id}/test-cases
                │   ├── GET    /api/projects/{id}/test-cases
                │   ├── GET    /api/test-cases/{id}
                │   ├── PUT    /api/test-cases/{id}
                │   ├── PATCH  /api/test-cases/{id}
                │   ├── DELETE /api/test-cases/{id}
                │   └── POST   /api/test-cases/{id}/execute
                │
                ├── Test Results
                │   ├── GET    /api/test-cases/{id}/results
                │   └── GET    /api/results/{id}
                │
                └── Audit Logs
                    ├── GET    /api/projects/{id}/audit-logs
                    └── GET    /api/test-cases/{id}/audit-logs