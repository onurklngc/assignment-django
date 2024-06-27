import json
import logging

import requests

import test_settings as s

HEADERS = {
    'Authorization': 'Basic b251cjoxMjM0',  # Update auth
    'Content-Type': 'application/json',
}

SERVER_ADDRESS = "http://127.0.0.1:8002"
CREATE_ORDER_PATH = "/order/create"
CANCEL_ORDER_PATH = "/order/cancel/"
LIST_ORDERS_PATH = "/order/list"

ORDER_PAYLOAD = json.dumps({
    "order_dishes": [
        {
            "dish": 1,
            "quantity": 3
        },
        {
            "dish": 2,
            "quantity": 2
        }
    ]
})
session = requests.session()
logger = logging.getLogger(__name__)


def create_order():
    response = session.post(SERVER_ADDRESS + CREATE_ORDER_PATH, headers=HEADERS, data=ORDER_PAYLOAD)
    logger.info(f"Created order: {response.text}")
    return response.json()


def cancel_order(order_id):
    response = session.post(SERVER_ADDRESS + CANCEL_ORDER_PATH + str(order_id), headers=HEADERS)
    logger.info(f"Canceled order: {response.text}")


def list_orders():
    response = session.get(SERVER_ADDRESS + LIST_ORDERS_PATH, headers=HEADERS)
    logger.info(f"User orders: {response.text}")


if __name__ == '__main__':
    logging.basicConfig(level=getattr(logging, s.LOG_LEVEL), format=s.LOGGING_FORMAT, datefmt=s.TIME_FORMAT)

    order_info = create_order()
    order2_info = create_order()
    if "id" in order2_info:
        cancel_order(order2_info["id"])
    list_orders()
