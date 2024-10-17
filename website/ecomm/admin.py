from django.contrib import admin
from .models import Category, Customer, Product
from cart.models import Cart, CartItem, Order

admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Cart)
admin.site.register(CartItem)