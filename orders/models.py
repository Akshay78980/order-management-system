from django.db import models

from products.models import Item
from core.models import Customer, Restaurant

# Create your models here.

ORDER_STATUS = [
    ('pending','Pending'),
    ('order_placed','Order Placed'),
    ('assigned','Assigned'),
    ('picked','Picked'),
    ('completed','Completed')
]


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS,  default='pending')



class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)