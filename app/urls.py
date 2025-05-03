from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name="home"),
    path('register/', views.register, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutPage, name="logout"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('contact/', views.contact, name="contact"),
    path('introduce/', views.introduce, name="introduce"),
    path('shopping_guide/', views.shopping_guide, name="shopping_guide"),
    path('update_item/', views.updateItem, name="update_item"),
    path('search/', views.search, name="search"),
    path('category/', views.category, name="category"),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('product/<int:pk>/reviews/', views.product_reviews, name='product_reviews'),
    path('product/<int:pk>/comments/', views.product_comments, name='product_comments'),
    path('add-to-cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('clear_cart/', views.clear_cart, name='clear_cart'),
    path('payment/', views.payment_view, name='payment'),
    path('payment-success/', views.payment_success_view, name='payment_success'),

    #VNPAY
    path('pay/', views.index, name='index'),
    path('payment_request/',views.payment_request, name='payment_request'),
    path('payment_ipn/', views.payment_ipn, name='payment_ipn'),
    path('payment_return/', views.payment_return, name='payment_return'),
    path('query/', views.query, name='query'),
    path('refund/', views.refund, name='refund')

]
