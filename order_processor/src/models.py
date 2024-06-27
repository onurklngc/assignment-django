from enum import Enum


class OrderStatus(Enum):
    PENDING = 0
    RECEIVED = 1
    COMPLETED = 2
    CANCELED = 3
