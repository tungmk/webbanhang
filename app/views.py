from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):
    return render(request, 'home.html')

def cart(request):
    context= {}
    return render(request, 'cart.html')

def checkout(request):
    context= {}
    return render(request, 'checkout.html')

def contact(request):
    context= {}
    return render(request, 'contact.html')

def introduce(request):
    context= {}
    return render(request, 'introduce.html')
