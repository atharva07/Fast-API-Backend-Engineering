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
                │   ├── GET    /api/projects/{project_id}
                │   ├── PUT    /api/projects/{project_id}
                │   ├── PATCH  /api/projects/{project_id}
                │   └── DELETE /api/projects/{project_id}
                │
                ├── Project Members
                │   ├── GET    /api/projects/{id}/members
                │   ├── POST   /api/projects/{id}/members
                │   ├── PATCH  /api/projects/{id}/members/{user_id}
                │   └── DELETE /api/projects/{id}/members/{user_id}
                │
                ├── Test Suites
                │   ├── POST   /api/projects/{project_id}/suites
                │   ├── GET    /api/projects/{project_id}/suites
                │   ├── GET    /api/suites/{suite_id}
                │   ├── PUT    /api/suites/{suite_id}
                │   ├── PATCH  /api/suites/{suite_id}
                │   └── DELETE /api/suites/{suite_id}
                │
                ├── Test Cases
                │   ├── POST   /api/suites/{suite_id}/test_cases
                │   ├── GET    /api/suites/{suite_id}/test_cases
                │   ├── GET    /api/test_cases/{id}
                │   ├── PUT    /api/test-cases/{id}
                │   ├── PATCH  /api/test-cases/{id}
                │   ├── DELETE /api/test-cases/{id}
                │   └── POST   /api/test-cases/{test_case_id}/execute
                │
                ├── Test Results
                │   ├── GET    /api/test-cases/{id}/results
                │   └── GET    /api/results/{id}
                │
                └── Audit Logs
                    ├── GET    /api/projects/{id}/audit-logs
                    └── GET    /api/test-cases/{id}/audit-logs


Passwords for Testing

Atharva             atharva123              atharva@gmail.com
Rahul               rahul123                rahul123@gmail.com
Priya               priya123                priya123@gmail.com
Tony Stark          temporary123            tony@example.com
Point Break         PointBreak123           pointBreak@avengers.com
Captain America     CaptainAmerica123       captainRodgers@avengers.com 


# Running tests

Install the dependencies and run the baseline sanity suite:

```bash
.venv/bin/pip install -r requirements.txt
.venv/bin/python -m pytest
```

The tests in `tests/` exercise validation, authentication primitives, authorization
rules, the health response, and project-service behavior without requiring a
PostgreSQL connection.