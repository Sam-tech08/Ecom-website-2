from django.urls import path
from cart import views

urlpatterns = [
    path('cart/', views.cart_view, name='cart_view'),
    path('add_to_cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),
    path('update_cart/<int:pk>/', views.update_cart, name='update_cart'),
    path('cart/<int:pk>', views.update_cart_item, name='update_cart_item'),
    path('checkoutpage/', views.checkout, name='checkoutpage'),
    path('clear_cart/', views.clear_cart,name='clear_cart'),
]