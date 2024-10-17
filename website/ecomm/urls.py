from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='homepage'),
    path('about/', views.about, name='about'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('search/', views.search, name='search'),
    path('product/<int:pk>', views.product_view, name='product'),
    path('category/<str:name>', views.Category_view, name='category'),

]