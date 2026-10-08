import os

RABBITMQ_HOST = os.getenv(
    "RABBITMQ_HOST",
    "localhost"
)

RABBITMQ_PORT = int(
    os.getenv(
        "RABBITMQ_PORT",
        "5672"
    )
)

RABBITMQ_QUEUE = os.getenv(
    "RABBITMQ_QUEUE",
    "qaforge-test-execution"
)

RABBITMQ_DLQ = os.getenv(
    "RABBITMQ_DLQ",
    "qaforge-test-execution-dlq"
)

RABBITMQ_DLX = os.getenv(
    "RABBITMQ_DLX",
    "qaforge-test-execution-dlx"
)

RABBITMQ_RETRY_QUEUE = os.getenv(
    "RABBITMQ_RETRY_QUEUE",
    "qaforge-test-execution-retry"
)

RABBITMQ_RETRY_ROUTING_KEY = os.getenv(
    "RABBITMQ_RETRY_ROUTING_KEY",
    "qaforge-test-execution-tetry"
)