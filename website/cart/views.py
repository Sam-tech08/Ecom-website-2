from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from cart.models import Cart, CartItem, Order
from ecomm.models import Product
from decimal import Decimal
from .forms import CheckoutForm, CartForm  # Assuming CheckoutForm is in a separate forms.py file
from django.contrib import messages


@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    total_price = Cart.objects.get(user=request.user).total_price
    return render(request, 'ecomm/cart_summary.html', {'cart_items': cart_items, 'total_price': total_price})


@login_required
def add_to_cart(request, pk):
    print(f"Adding product {pk} to cart...")
    product = Product.objects.get(pk=pk)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if created:
        cart_item.quantity = 1
    else:
        cart_item.quantity += 1
    cart_item.save()
    cart.total_price += Decimal(product.price) * cart_item.quantity
    cart.save()
    return redirect('cart_view')


@login_required
def remove_from_cart(request, pk):
    try:
        cart_item = CartItem.objects.get(pk=pk)
        cart = cart_item.cart  # Get the cart associated with the cart item

        # Adjust the cart's total price before deleting the item
        cart.total_price -= cart_item.product.price * cart_item.quantity
        cart.save()

        # Delete the cart item
        cart_item.delete()

        messages.success(request, "Item removed from the cart.")
    except CartItem.DoesNotExist:
        messages.error(request, "Item does not exist in the cart.")

    return redirect('cart_view')

@login_required
def update_cart(request, pk):
    cart_item = CartItem.objects.get(pk=pk)
    form = CartForm(request.POST or None, instance=cart_item)
    if form.is_valid():
        form.save()
        cart = Cart.objects.get(user=request.user)
        cart.total_price = sum([item.product.price or item.product.sale_value * item.quantity for item in CartItem.objects.filter(cart=cart)])
        cart.save()
        return redirect('cart_view')
    return render(request, 'ecomm/cart_summary.html', {'form': form, 'cart_item': cart_item})


def update_cart_item(request, pk):
    cart_item = get_object_or_404(CartItem, pk=pk)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'increment':
            cart_item.quantity += 1
        elif action == 'decrement' and cart_item.quantity > 1:
            cart_item.quantity -= 1
        cart_item.save()

        # Recalculate the total price of the cart
        cart = Cart.objects.get(user=request.user)
        cart.total_price = sum(item.quantity * (item.product.sale_value if item.product.is_sale else item.product.price)
                               for item in CartItem.objects.filter(cart=cart))

        # Save the cart with the updated total price
        cart.save()
        return redirect('cart_view')  # Replace with the URL of your cart page
    return render(request, 'ecomm/cart_summary.html', {'cart_items': CartItem.objects.filter(user=request.user)})


# def checkout(request):
#     if request.method == 'POST':
#         form = CheckoutForm(request.POST)
#         if form.is_valid():
#             # Get customer details from the form
#
#     else:
#         # Render the checkout form
#         return render(request, 'ecomm/checkoutpage.html')
#     return render(request,'ecomm/cart_summary.html', {'form': form, 'order': order})
# # Create your views here.


# def checkout(request):
#   if request.method == 'POST':
#     form = CheckoutForm(request.POST)
#     if form.is_valid():
#         first_name = request.POST.get('first_name')
#         last_name = request.POST.get('last_name')
#         email = request.POST.get('email')
#         phone_number = request.POST.get('phone_number')
#
#         address1 = request.POST.get('address1')
#         address2 = request.POST.get('address2')
#         city = request.POST.get('city')
#         state = request.POST.get('state')
#         country = request.POST.get('country')
#
#         postal_code = request.POST.get('postal_code')
#
#         # Create a new order and save customer details
#         order = Order.objects.create(
#             user=request.user,
#             first_name=first_name,
#             last_name=last_name,
#             email=email,
#             phone_number=phone_number,
#             address1=address1,
#             address2=address2,
#             city=city,
#             state=state,
#             country=country,
#             postal_code=postal_code
#         )
#         order.save()
#         form.save()
#         return redirect('cart_view')
#   else:
#         form = CheckoutForm()
#         return render(request, 'cart/home.html', {'form': form})

def checkout(request):
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Retrieve cleaned data from the form
            cleaned_data = form.cleaned_data

            # Create a new Order instance and set its fields
            order = Order.objects.create(
                user=request.user,
                first_name=cleaned_data['first_name'],
                last_name=cleaned_data['last_name'],
                email=cleaned_data['email'],
                phone_number=cleaned_data['phone_number'],

                address1=cleaned_data['address1'],
                address2=cleaned_data['address2'],
                city=cleaned_data['city'],
                state=cleaned_data['state'],
                country=cleaned_data['country'],
                postal_code= cleaned_data['postal_code']
            )

            # Save the order and redirect to a success page
            order.save()
            messages.success(request, ("YOU HAVE SUCCESSFULLY ORDERED INNN..........."))
            return redirect('homepage')  # Replace with your success page URL

        else:
            messages.success(request, ("Try again....."))
    else:
        form = CheckoutForm()

    context = {'form': form}
    return render(request, 'ecomm/checkoutpage.html', context)


def clear_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    cart_items.delete()
    cart.total_price = 0
    cart.save()
    messages.success(request, ("YOUR ORDER IS PLACED AND IT IS ON ITS WAY......."))
    return redirect('homepage')
