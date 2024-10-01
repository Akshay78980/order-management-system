from rest_framework import serializers
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source='item.name', read_only=True)
    item_price = serializers.DecimalField(source='item.price', max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = ['item_name', 'quantity', 'item_price']


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True, source='orderitem_set')
    restaurant = serializers.SerializerMethodField()
    customer = serializers.SerializerMethodField()

    def get_customer(self,obj):
        try:
            if obj.customer:
                data = {
                    "id": obj.customer.id,
                    'name':obj.customer.name
                }
                return data
            else:
                return None
        except:
            return None

    def get_restaurant(self,obj):
        try:
            if obj.restaurant:
                data = {
                    "id": obj.restaurant.id,
                    "name": obj.restaurant.name
                }
                return data
            else:
                return None
        except:
            return None


    class Meta:
        model = Order
        fields = ['id', 'customer', 'restaurant', 'order_items', 'total_amount', 'order_status']
