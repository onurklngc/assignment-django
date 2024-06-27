from enum import Enum

from django.contrib.auth.models import User
from django.db import models


class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Dish(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, related_name='dishes', on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, related_name='dishes', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class OrderStatus(Enum):
    PENDING = (0, 'pending')
    RECEIVED = (1, 'received')
    COMPLETED = (2, 'completed')
    CANCELED = (3, 'canceled')


class Order(models.Model):
    STATUS_CHOICES = [status.value for status in OrderStatus]

    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

    def to_json(self):
        return {"user_id": self.user.id, "created_at": self.created_at, "status": self.status}


class OrderDish(models.Model):
    order = models.ForeignKey(Order, related_name='order_dishes', on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)  # Adjust default as needed

    def __str__(self):
        return f"{self.quantity} x {self.dish.name} in Order {self.order.id}"
