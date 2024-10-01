from django.db import models

# Create your models here.


class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone  = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.name}'


class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=250)


    def __str__(self):
        return self.name