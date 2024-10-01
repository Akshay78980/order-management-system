from django.db import models

from core.models import Restaurant

class Item(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()

    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.name}({self.restaurant.name})'