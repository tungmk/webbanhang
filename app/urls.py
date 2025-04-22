from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('register/', views.register, name="register"),
    path('login/', views.login, name="login"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('contact/', views.contact, name="contact"),
    path('introduce/', views.introduce, name="introduce"),
    path('shopping_guide/', views.shopping_guide, name="shopping_guide"),
    path('update_item/', views.updateItem, name="update_item")
]
