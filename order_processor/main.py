import argparse
import json
import logging
from time import sleep

import MySQLdb
import pika

import settings as s
from src.models import OrderStatus

GET_STATUS_QUERY = "SELECT `status` FROM `ordering_order` WHERE (`id` = %s)"
UPDATE_QUERY = "UPDATE `ordering_order` SET `status` = %s WHERE (`id` = %s)"

logger = logging.getLogger(__name__)
db_connection = None
db_cursor = None


def get_order_status(order_id, retry=True):
    order_status = None
    db_cursor.execute(GET_STATUS_QUERY % order_id)
    order_data = db_cursor.fetchone()
    if not order_data:
        if retry:
            connect_to_db()
            order_status = get_order_status(order_id, retry=False)
        else:
            logger.error(f"Order #{order_id} is not found.")
    else:
        order_status = order_data[0]
    return order_status


def process_request(message_body):
    message_data = json.loads(message_body)
    order_id = message_data["id"]
    logger.info(" [x] Received %r" % message_data)

    sleep(s.VIRTUAL_DELAY)  # Virtual delay
    order_status = get_order_status(order_id)
    if order_status is None:
        return
    if order_status != OrderStatus.PENDING.value:
        order_status = OrderStatus(order_status).name
        logger.error(f"Order status is already {order_status}.")
        return
    sleep(2 * s.VIRTUAL_DELAY)  # Prepare order
    db_cursor.execute(UPDATE_QUERY, (2, order_id))
    db_connection.commit()
    logger.info(f"Order #{order_id} is completed successfully!")


def queue_callback(ch, method, properties, body):
    try:
        process_request(body)
    except Exception:
        logger.exception(f"Error: unable to process queue message: {body}")


def listen_queue(rabbitmq_connection_parameters):
    connection = pika.BlockingConnection(rabbitmq_connection_parameters)
    channel = connection.channel()
    channel.queue_declare(queue=s.QUEUE_NAME)
    channel.basic_consume(queue=s.QUEUE_NAME, auto_ack=True, on_message_callback=queue_callback)
    logger.info(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


def connect_to_db():
    global db_connection, db_cursor
    db_connection = MySQLdb.connect(
        host=s.MYSQL_HOST,
        port=s.MYSQL_PORT,
        user=s.MYSQL_USER,
        password=s.MYSQL_PASSWORD,
        database=s.MYSQL_SCHEMA_NAME
    )
    db_cursor = db_connection.cursor()
    return db_connection, db_cursor


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--log_level', help='log level', default=s.LOG_LEVEL)

    parser.add_argument('--rabbitmq_host', help='rabbitmq host', default=s.RABBITMQ_HOST)
    parser.add_argument('--rabbitmq_port', help='rabbitmq port', default=s.RABBITMQ_PORT)

    args = parser.parse_args()

    logging.basicConfig(level=getattr(logging, args.log_level),
                        format=s.LOGGING_FORMAT, datefmt=s.TIME_FORMAT)
    logger.info(args)
    rabbitmq_connection_parameters = pika.ConnectionParameters(host=args.rabbitmq_host, port=args.rabbitmq_port)
    connect_to_db()
    while True:
        try:
            listen_queue(rabbitmq_connection_parameters)
        except (KeyboardInterrupt, InterruptedError):
            logging.info('Preparing to terminate...')
            break
        except Exception:
            logger.exception("Error occurred while listening queue:")
    if db_cursor:
        db_cursor.close()
