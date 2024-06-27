from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ..models import Order, OrderDish, Dish, OrderStatus, Category, Restaurant


def common_test_setup(test_case):
    test_case.category1 = Category.objects.create(name='Italian')
    test_case.restaurant1 = Restaurant.objects.create(name='Italian Bistro', address='123 Pasta Lane')
    test_case.dish1 = Dish.objects.create(name='Spaghetti Carbonara',
                                          description='Classic Italian pasta with eggs, cheese, pancetta, and pepper.',
                                          price=12.50, category=test_case.category1, restaurant=test_case.restaurant1)

    test_case.dish2 = Dish.objects.create(name='Margherita Pizza',
                                          description='Traditional pizza with tomatoes, mozzarella, and basil.',
                                          price=10.00,
                                          category=test_case.category1, restaurant=test_case.restaurant1)


class OrderCreateViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        common_test_setup(self)
        self.url = reverse('order-create')
        self.client.login(username='testuser', password='testpassword')

    def test_create_order(self):
        payload = {
            "order_dishes": [
                {"dish": self.dish1.id, "quantity": 3},
                {"dish": self.dish2.id, "quantity": 2}
            ]
        }
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(Order.objects.get().user, self.user)


class OrderCancelViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        common_test_setup(self)
        self.order = Order.objects.create(user=self.user, status=OrderStatus.PENDING.value[0])
        self.order_dish = OrderDish.objects.create(order=self.order, dish=self.dish1, quantity=3)
        self.url = reverse('order-cancel', args=[self.order.id])

    def test_cancel_order(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, OrderStatus.CANCELED.value[0])

    def test_cancel_nonexistent_order(self):
        url = reverse('order-cancel', args=[999])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)


class OrderListViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.url = reverse('order-list')
        common_test_setup(self)
        self.order1 = Order.objects.create(user=self.user, status=OrderStatus.PENDING.value[0])
        self.order2 = Order.objects.create(user=self.user, status=OrderStatus.COMPLETED.value[0])
        OrderDish.objects.create(order=self.order1, dish=self.dish1, quantity=3)
        OrderDish.objects.create(order=self.order2, dish=self.dish2, quantity=2)

    def test_list_orders(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
