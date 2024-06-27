from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Order, OrderStatus
from .publisher_service import PublisherService
from .serializers import OrderSerializer


class OrderCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.data["user"] = request.user.id
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save(user=request.user)
            PublisherService.publish(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderCancelView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id, user=request.user.id)
        except Order.DoesNotExist:
            return Response({'error': 'Order does not exist'}, status=status.HTTP_406_NOT_ACCEPTABLE)

        if order.status == OrderStatus.PENDING.value[0]:
            order.status = OrderStatus.CANCELED.value[0]
            order.save()
            response = Response(OrderSerializer(order).data)
        else:
            order_status = Order.STATUS_CHOICES[order.status][1]
            response = Response({'error': f'Order status is already {order_status}.'},
                                status=status.HTTP_406_NOT_ACCEPTABLE)
        return response


class OrderListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
