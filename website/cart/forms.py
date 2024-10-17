from cart.models import Order, CartItem
from django import forms


class CartForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ('quantity',)


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('first_name', 'last_name',  'email', 'phone_number', 'address1', 'address2', 'city', 'state', 'country', 'postal_code')