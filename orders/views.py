from django.shortcuts import render
from django.core.cache import cache

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Order, OrderItem, ORDER_STATUS
from core.models import Customer, Restaurant
from products.models import Item
from .serializers import OrderSerializer

from .tasks import update_order_status
from django_q.tasks import schedule


class CreateOrderView(APIView):
    def post(self, request):
        data = request.data

        items = data.get('items',[])
        if not items:
            return Response({"error": "No items where selected."},status=status.HTTP_400_BAD_REQUEST)
        else:
            if any(item_detail['quantity'] <= 0 for item_detail in items):
                return Response({"error": "Quantity must be greater than zero for all items."}, status=status.HTTP_400_BAD_REQUEST)


        try:
            customer = Customer.objects.get(id=data['customer_id'])
            restaurant = Restaurant.objects.get(id=data['restaurant_id'])
            
            order = Order.objects.create(customer=customer,
                                         restaurant=restaurant,
                                         total_amount=0,
                                         order_status='pending'
                                        )
            
            total_amount = 0
            
            for item_detail in data['items']:
                item = Item.objects.get(id=item_detail['item_id'],restaurant = restaurant)  
                quantity = item_detail['quantity']
                price = item.price  
                total_amount += quantity * price

                OrderItem.objects.create(order=order,
                                        item=item,
                                        quantity=quantity,
                                        price=price
                                    )
            
            order.total_amount = total_amount
            order.order_status = 'order_placed'
            order.save()

            data = {
                "message" : "Order has been placed..",
                'total': total_amount
            }

            return Response(data, status=status.HTTP_201_CREATED)
        
        except (Customer.DoesNotExist, Restaurant.DoesNotExist, Item.DoesNotExist) as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    

class DetailOrderView(APIView):
    def get(self, request, order_id):
            
            cache_key = f'order_{order_id}'
            order_data = cache.get(cache_key)

            if order_data:
                return Response(order_data, status=status.HTTP_200_OK)
            
            try:
                order = Order.objects.get(id=order_id)
                serializer = OrderSerializer(order)
                order_data = serializer.data

                cache.set(cache_key,order_data,timeout=60*10)

                return Response(serializer.data, status=status.HTTP_200_OK)
                
            except Order.DoesNotExist:
                return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
        


class UpdateOrderStatusView(APIView):
    def patch(self, request, order_id):
        try:
            new_status = request.data.get('order_status')

            valid_statuses = [choice[0] for choice in ORDER_STATUS]

            if new_status not in valid_statuses:
                return Response({"error":"Please provide a valid order status."},status=status.HTTP_400_BAD_REQUEST)
            
            order = Order.objects.get(id=order_id)
            if not order:
                return Response({'error':"Order does not exist."})

            schedule(
                "orders.tasks.update_order_status",
                order_id,
                new_status,
                schedule_type='O'
            )

            return Response({"message":"Order status updated successfully."}, status=status.HTTP_200_OK)
        
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)






