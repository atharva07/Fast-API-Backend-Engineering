import pika

from app.core.rabbitmq import (
    RABBITMQ_HOST,
    RABBITMQ_PORT,
    RABBITMQ_QUEUE,
    RABBITMQ_DLQ,
    RABBITMQ_DLX
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
    channel.exchange_declare(
        exchange=RABBITMQ_DLX,
        exchange_type="direct",
        durable=True,
    )

    channel.queue_declare(
        queue=RABBITMQ_DLQ,
        durable=True,
    )

    channel.queue_bind(
        queue=RABBITMQ_DLQ,
        exchange=RABBITMQ_DLX,
        routing_key=RABBITMQ_DLQ,
    )

    channel.queue_declare(
        queue=RABBITMQ_QUEUE,
        durable=True,
        arguments={
            "x-dead-letter-exchange": RABBITMQ_DLX,
            "x-dead-letter-routing-key": RABBITMQ_DLQ,
        },
    )