from django.shortcuts import render
from django.http import HttpResponse
from .models import *
# Create your views here.

def home(request):
    products = Product.objects.all()
    context= {'products': products} 
    return render(request, 'home.html', context)

def cart(request):
    if request.user.is_authenticated: 
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
    else: 
        items = []
        order = {'get_cart_items':0,'get_cart_total':0} 
    context = {'items':items, 'order':order}
    return render(request, 'cart.html', context)

def checkout(request):
    if request.user.is_authenticated: 
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
    else: 
        items = []
        order = {'get_cart_items':0,'get_cart_total':0} 
    context = {'items':items, 'order':order}
    return render(request, 'checkout.html', context)

def contact(request):
    context= {}
    return render(request, 'contact.html')

def introduce(request):
    context= {}
    return render(request, 'introduce.html')

def shopping_guide(request):
    context={}
    return render(request, 'shopping_guide.html')
