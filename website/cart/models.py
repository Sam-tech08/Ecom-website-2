from django.db import models
from ecomm.models import Product
from django.contrib.auth.models import User


class Cart(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=4, default=0.00)


    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(max_digits=10, decimal_places=4, default=0.00)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default = 1)
    first_name = models.CharField(max_length=100, default='Unknown')
    last_name = models.CharField(max_length=100, default='Unknown')
    email = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, default ='N/A')

    address1 = models.CharField(max_length=255, default=False)
    address2 = models.CharField(max_length=255, blank=True, null=True, default=False)
    city = models.CharField(max_length=100, default=False)

    state = models.CharField(max_length=100, default=False)
    country = models.CharField(max_length=100, default=False)
    postal_code = models.CharField(max_length=20, default ='N/A')
# Create your models here.
