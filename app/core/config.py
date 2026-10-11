import os

JWT_SECRET_KEY = os.getenv(
    "JWT_SECRET_KEY",
    "development-secret-change-me"
)

if (
    os.getenv("APP_ENV", "development").lower() == "production"
    and JWT_SECRET_KEY == "development-secret-change-me"
):
    raise RuntimeError(
        "JWT_SECRET_KEY must be configured in production"
    )

JWT_ALGORITHM = "HS256"

JWT_ACCESS_TOKEN_EXPIRE_MINUTES = 30