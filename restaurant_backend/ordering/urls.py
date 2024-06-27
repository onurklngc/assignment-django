from django.urls import path
from .views import OrderCreateView, OrderListView, OrderCancelView

urlpatterns = [
    path('create', OrderCreateView.as_view(), name='order-create'),
    path('cancel/<int:order_id>', OrderCancelView.as_view(), name='order-cancel'),
    path('list', OrderListView.as_view(), name='order-list'),
]
