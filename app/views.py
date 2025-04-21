from django.shortcuts import render
from django.http import HttpResponse
from .models import *
# Create your views here.

def home(request):
    products = Product.objects.all()
    context= {'products': products} 
    return render(request, 'home.html', context)

def cart(request):
    return render(request, 'cart.html', context)

def checkout(request):
    context= {}
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
