from django.shortcuts import render, redirect, get_object_or_404
from .models import Product,Category
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm


def search(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        searched = Product.objects.filter(name__icontains=searched)
        if not searched:
            messages.success(request, ("The item is not present"))
            return render(request, 'ecomm/search.html', {})
        else:
            messages.success(request, ("The item is present"))
            return render(request, 'ecomm/search.html', {'searched': searched})
    else:
        return render(request, 'ecomm/search.html',{})


def home(request):
    products = Product.objects.all()
    return render(request, 'ecomm/home.html', {'products': products})


def product_view(request, pk):
    pro = Product.objects.get(pk=pk)
    return render(request, 'ecomm/product.html', {'pro': pro})


def about(request):
    return render(request, 'ecomm/about.html', {})


def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("YOU HAVE SUCCESSFULLY LOGGED INNN..........."))
            return redirect('homepage')
        else:
            messages.success(request, ("Incorrect username or password try again....."))
            return redirect('login')
    else:
        return render(request, 'ecomm/login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, ("Logout successfull thanks for stopping by.................."))
    return redirect('homepage')
    # return render(request, 'ecomm/logout.html', {})


# def register_user(request):
#     if request.method == "POST":
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password1']
#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 messages.success(request, "YOU HAVE SUCCESSFULLY REGISTERED!")
#                 return redirect('homepage')
#             else:
#                 messages.error(request, "Authentication failed. Please try again.")
#         else:
#             messages.error(request, "Incorrect username or password. Please try again.")
#     else:
#         form = SignUpForm()
#     return render(request, 'ecomm/register.html', {'form': form})


def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('login')  # Redirect to login page after successful registration
        else:
            return render(request, 'ecomm/register.html', {'form': form})  # Render form with errors
    else:
        form = UserCreationForm()

    return render(request, 'ecomm/register.html', {'form': form})  # Render blank form on GET request


def Category_view(request, name):
    category = get_object_or_404(Category, name=name)
    name = Category.objects.get(name=name)
    products = Product.objects.filter(category=name)
    return render(request,'ecomm/category.html', {'category': category,'products':products, 'name': name})
