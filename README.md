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