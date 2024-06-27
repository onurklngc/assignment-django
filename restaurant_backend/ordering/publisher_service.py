import json
import logging

import pika

from .settings import RABBITMQ_HOST, RABBITMQ_PORT, QUEUE_NAME
logger = logging.getLogger(__name__)


class PublisherService:
    rabbitmq_connection_parameters = pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT)
    @staticmethod
    def publish(message_data):
        connection = pika.BlockingConnection(PublisherService.rabbitmq_connection_parameters)
        channel = connection.channel()
        channel.queue_declare(queue=QUEUE_NAME)
        body = json.dumps(message_data).encode()
        channel.basic_publish(exchange='', routing_key=QUEUE_NAME, body=json.dumps(message_data).encode())
        logger.info(f" [x] Sent {body}")
