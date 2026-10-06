import pika

from app.core.rabbitmq import (
    RABBITMQ_HOST,
    RABBITMQ_PORT,
)

def create_connection():
    credentials = pika.PlainCredentials(
        username="guest",
        password="guest"
    )

    parameters = pika.ConnectionParameters(
        host=RABBITMQ_HOST,
        port=RABBITMQ_PORT,
        credentials=credentials
    )

    return pika.BlockingConnection(parameters)

def declare_queue(channel):
    channel.queue_declare(
        queue="qaforge-test-execution",
        durable=True
    )