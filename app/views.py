from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from .models import *
import json
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .models import Product

# Create your views here.
def category(request):
    categories = Category.objects.filter(is_sub = False) # lay danh muc lon
    active_category = request.GET.get('category','')# danh muc dang duoc chon
    if active_category:
        products = Product.objects.filter(category__slug = active_category)
    context = {'categories':categories, 'products':products, 'active_category':active_category}
    return render(request, 'category.html',context)
def search(request):
    if request.method == "POST":
        searched = request.POST["searched"]
        keys = Product.objects.filter(name__contains = searched)
    if request.user.is_authenticated: 
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else: 
        items = []
        order = {'get_cart_items':0,'get_cart_total':0} 
        cartItems = order['get_cart_items']
    products = Product.objects.all()
    return render(request,'search.html',{"searched":searched,"keys":keys,'products': products, 'cartItems':cartItems} )
def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('login')
    context = {'form':form}
    return render(request, 'register.html',context)
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')  # Chuyển hướng đến trang Home sau khi đăng nhập thành công
        else:
            # Nếu thông tin đăng nhập không chính xác
            messages.info(request,'user or password not correct!')
            return redirect('login')
    
    return render(request, 'login.html')
def logoutPage(request):
    logout(request)
    return redirect('login')
def home(request):
    if request.user.is_authenticated: 
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else: 
        items = []
        order = {'get_cart_items':0,'get_cart_total':0} 
        cartItems = order['get_cart_items']
    categories = Category.objects.filter(is_sub = False) # lay danh muc lon
    super_categories = Category.objects.filter(is_sub = True)
    active_category = request.GET.get('category','')# danh muc dang duoc chon
    products = Product.objects.all()
    context= {'categories':categories,'products': products, 'cartItems':cartItems} 
    return render(request, 'home.html', context)

def cart(request):
    if request.user.is_authenticated: 
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else: 
        items = []
        order = {'get_cart_items':0,'get_cart_total':0} 
        cartItems = order['get_cart_items']
    categories = Category.objects.filter(is_sub = False) # lay danh muc lon
    super_categories = Category.objects.filter(is_sub = True)
    context = {'categories':categories,'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'cart.html', context)

def checkout(request):
    if request.user.is_authenticated: 
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else: 
        items = []
        order = {'get_cart_items':0,'get_cart_total':0} 
        cartItems = order['get_cart_items']
    categories = Category.objects.filter(is_sub = False) # lay danh muc lon
    super_categories = Category.objects.filter(is_sub = True)
    context = {'categories':categories,'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'checkout.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productID = data['productID']
    action = data['action']
    customer = request.user
    product = Product.objects.get(id = productID)
    order, created = Order.objects.get_or_create(customer = customer, complete = False)
    orderItem, created = OrderItem.objects.get_or_create(order = order, product = product)
    if action == 'add':
        orderItem.quantity += 1
    elif action == 'remove':    
        orderItem.quantity -=1
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('Added', safe=False)
    
def contact(request):
    categories = Category.objects.filter(is_sub = False) # lay danh muc lon
    super_categories = Category.objects.filter(is_sub = True)
    context= {'categories':categories}
    return render(request, 'contact.html',context)

def introduce(request):
    categories = Category.objects.filter(is_sub = False) # lay danh muc lon
    super_categories = Category.objects.filter(is_sub = True)
    context= {'categories':categories}
    return render(request, 'introduce.html',context)

def shopping_guide(request):
    categories = Category.objects.filter(is_sub = False) # lay danh muc lon
    super_categories = Category.objects.filter(is_sub = True)
    context={'categories':categories}
    return render(request, 'shopping_guide.html',context)
def product_reviews(request, pk):
    product = get_object_or_404(Product, id=pk)
    return render(request, 'reviews.html', {'product': product})

def product_comments(request, pk):
    product = get_object_or_404(Product, id=pk)
    return render(request, 'comments.html', {'product': product})

def add_to_cart(request, pk):
    # Tùy logic thêm sản phẩm vào giỏ hàng của bạn
    quantity = int(request.POST.get('quantity', 1))
    product = get_object_or_404(Product, id=pk)
    # Xử lý thêm sản phẩm vào giỏ ở đây...
    return redirect('cart')  # Chuyển về giỏ hàng


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_detail.html', {'product': product})

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

@login_required
def dashboard(request):
    if request.user.is_superuser:
        return HttpResponse("Xin chào Admin!")
    else:
        return HttpResponse("Bạn không phải admin.")
