from rest_framework import serializers

from .models import Restaurant, Category, Dish, Order, OrderDish


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = '__all__'


class OrderDishSerializer(serializers.ModelSerializer):
    dish = serializers.PrimaryKeyRelatedField(queryset=Dish.objects.all())

    class Meta:
        model = OrderDish
        fields = ['dish', 'quantity']

    def create(self, validated_data):
        return OrderDish.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.dish = validated_data.get('dish', instance.dish)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.save()
        return instance


class OrderSerializer(serializers.ModelSerializer):
    order_dishes = OrderDishSerializer(many=True, required=False)
    status_str = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'status_str', 'created_at', 'order_dishes']

    def get_status_str(self, obj):
        return Order.STATUS_CHOICES[obj.status][1]

    def create(self, validated_data):
        order_dishes_data = validated_data.pop('order_dishes', [])
        order = Order.objects.create(**validated_data)
        for order_dish_data in order_dishes_data:
            OrderDish.objects.create(order=order, **order_dish_data)
        return order

    def update(self, instance, validated_data):
        order_dishes_data = validated_data.pop('order_dishes', [])
        instance.status = validated_data.get('status', instance.status)
        instance.save()

        # Update or create order dishes
        existing_ids = set(instance.order_dishes.values_list('id', flat=True))
        for order_dish_data in order_dishes_data:
            if 'id' in order_dish_data:
                if order_dish_data['id'] in existing_ids:
                    order_dish = OrderDish.objects.get(id=order_dish_data['id'])
                    order_dish.quantity = order_dish_data.get('quantity', order_dish.quantity)
                    order_dish.save()
                    existing_ids.remove(order_dish.id)
                else:
                    OrderDish.objects.create(order=instance, **order_dish_data)
            else:
                OrderDish.objects.create(order=instance, **order_dish_data)

        # Delete any remaining order dishes not in the updated data
        OrderDish.objects.filter(id__in=existing_ids).delete()

        return instance
