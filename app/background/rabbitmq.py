import pika
import os
from app.core.rabbitmq import (
    RABBITMQ_HOST,
    RABBITMQ_PORT,
    RABBITMQ_QUEUE,
    RABBITMQ_DLQ,
    RABBITMQ_DLX,
    RABBITMQ_RETRY_QUEUE,
    RABBITMQ_RETRY_ROUTING_KEY
)

def create_connection():
    username = os.getenv("RABBITMQ_USER", "guest")
    password = os.getenv("RABBITMQ_PASSWORD", "guest")

    credentials = pika.PlainCredentials(
        username=username,
        password=password
    )

    parameters = pika.ConnectionParameters(
        host=RABBITMQ_HOST,
        port=RABBITMQ_PORT,
        credentials=credentials
    )

    return pika.BlockingConnection(parameters)

def declare_queue(channel):
    # Dead Letter Exchange
    channel.exchange_declare(
        exchange=RABBITMQ_DLX,
        exchange_type="direct",
        durable=True,
    )

    # Dead Letter Queue
    channel.queue_declare(
        queue=RABBITMQ_DLQ,
        durable=True,
    )

    channel.queue_bind(
        queue=RABBITMQ_DLQ,
        exchange=RABBITMQ_DLX,
        routing_key=RABBITMQ_DLQ,
    )

    # Main execution queue
    channel.queue_declare(
        queue=RABBITMQ_QUEUE,
        durable=True,
        arguments={
            "x-dead-letter-exchange": RABBITMQ_DLX,
            "x-dead-letter-routing-key": RABBITMQ_DLQ,
        },
    )

    # Retry Queue
    channel.queue_declare(
        queue=RABBITMQ_RETRY_QUEUE,
        durable=True,
        arguments={
            "x-dead-letter-exchange": "",
            "x-dead-letter-routing-key": RABBITMQ_QUEUE,
        },
    )