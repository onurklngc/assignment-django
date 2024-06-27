import json
import logging

import pika

import settings as s

ORDER_INFO = {'id': 11, 'status_str': 'pending', 'created_at': '2024-06-26T11:45:10.558219Z',
              'order_dishes': [{'dish': 1, 'quantity': 3}, {'dish': 2, 'quantity': 2}]}

rabbitmq_connection_parameters = pika.ConnectionParameters(host=s.RABBITMQ_HOST, port=s.RABBITMQ_PORT)
logger = logging.getLogger(__name__)


def send_message_to_queue(queue_name, message, connection_parameters=rabbitmq_connection_parameters):
    connection = pika.BlockingConnection(connection_parameters)
    channel = connection.channel()

    channel.queue_declare(queue=queue_name)

    channel.basic_publish(exchange='', routing_key=queue_name, body=json.dumps(message).encode())
    logger.info(f"Sent message: {message}")

    connection.close()


if __name__ == '__main__':
    logging.basicConfig(level=getattr(logging, s.LOG_LEVEL), format=s.LOGGING_FORMAT, datefmt=s.TIME_FORMAT)

    send_message_to_queue(s.QUEUE_NAME, ORDER_INFO)
