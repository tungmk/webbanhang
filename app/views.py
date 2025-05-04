
from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from .models import *
import json
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .models import Product
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import ShippingAddress
from django.shortcuts import render, redirect
from .models import Order, Payment
from django.utils import timezone
import random
from app.models import PaymentForm
from django.urls import reverse
from app.vnpay import vnpay
from django.conf import settings
from datetime import datetime
import random
import string


# Create your views here.

# def paypal_ipn(requests):
#     return redirect('home')

# def your_return_view(requests):
#     messages.success(requests,'Ok la hahaahaaha')
#     return redirect('home')

# def your_cancel_view(requests):
#     messages.success(requests, 'Ok la hahaahaaha')
#     return redirect('home')

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


    # What you want the button to do.
    paypal_dict = {
        "business": "sb-rzg8a28081989@personal.example.com",
        "amount": "1230.00",
        "item_name": "nHIHI",
        "invoice": "unique-invoice-id",
        # "notify_url": request.build_absolute_uri(reverse('paypal_ipn')),
        # "return": request.build_absolute_uri(reverse('your_return_view')),
        # "cancel_return": request.build_absolute_uri(reverse('your_cancel_view')),
        "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
    }

    # Create the instance.

    categories = Category.objects.filter(is_sub = False) # lay danh muc lon
    super_categories = Category.objects.filter(is_sub = True)
    order_id = generate_unique_id()
    context = {'categories':categories,'items':items, 'order':order, 'cartItems':cartItems, 'order_id': order_id}
    return render(request, 'checkout.html', context)

def generate_unique_id():
    now = datetime.now()
    timestamp = now.strftime('%Y%m%d%H%M%S') + f'{now.microsecond // 1000:03d}'
    suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))  # 5-character random suffix
    return timestamp + suffix

def updateItem(request):
    data = json.loads(request.body)
    productID = data['productID']
    action = data['action']
    quantity = int(data.get('quantity', 1))  # lấy số lượng từ client

    customer = request.user
    product = Product.objects.get(id=productID)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity += quantity  # ✅ tăng theo số lượng client gửi
    elif action == 'remove':
        orderItem.quantity -= quantity

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse({'message': 'Đã cập nhật', 'cart_total': order.get_cart_items()}, safe=False)
    
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

@login_required
def clear_cart(request):
    if request.method == 'POST':
        try:
            # Lấy giỏ hàng chưa thanh toán của user
            order = Order.objects.filter(customer=request.user, complete=False).first()
            
            if order:
                # Xóa tất cả OrderItem liên quan
                order.orderitem_set.all().delete()
                
                # Cập nhật lại thông tin giỏ hàng (nếu cần)
                order.transaction_id = None
                order.save()
                
                return JsonResponse({'success': True, 'message': 'Giỏ hàng đã được xóa!'})
            else:
                return JsonResponse({'success': False, 'message': 'Không tìm thấy giỏ hàng'})
        
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    
    return JsonResponse({'success': False, 'message': 'Yêu cầu không hợp lệ'})

def processOrder(request):
    data = json.loads(request.body)
    
    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    ShippingAddress.objects.create(
        order=order,
        name=data['name'],
        email=data['email'],
        address=data['address'],
        city=data['city'],
        state=data['state'],
        zipcode=data['zipcode'],
    )

    order.complete = True
    order.save()

    return JsonResponse('Đơn hàng đã được xử lý', safe=False)

def payment_view(request):
    if request.method == 'POST':
        # Lấy dữ liệu từ form checkout
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zipcode = request.POST.get('zipcode')

        # Bạn có thể lưu dữ liệu này vào session hoặc context để truyền sang payment.html
        context = {
            'name': name,
            'email': email,
            'address': address,
            'city': city,
            'state': state,
            'zipcode': zipcode,
        }

        return render(request, 'payment.html',context)
    
    # # Nếu ai đó truy cập trực tiếp mà không qua POST
    return redirect('checkout')  # hoặc trả về lỗi, tuỳ bạn

def payment_success_view(request):
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        
        # Lưu vào database nếu bạn có model
        Payment_success.objects.create(
            user=request.user,
            payment_method=payment_method
        )

        return render(request, 'payment_success.html', {
            'payment_method': payment_method
        })

    return redirect('payment_success.html')


#Add vnpay
#VN PAY

def index(request):
    return render(request, "payment/index.html", {"title": "Danh sách demo"})


def hmacsha512(key, data):
    byteKey = key.encode('utf-8')
    byteData = data.encode('utf-8')
    return hmac.new(byteKey, byteData, hashlib.sha512).hexdigest()


def payment_request(request):
    # total_amount = form.cleaned_data['amount']
    # print("Tien đc day sang:")
    # print(total_amount)
    if request.method == 'POST':
        print("Tien đc day sang:")
        # Process input data and build url payment
        form = PaymentForm(request.POST)
        if form.is_valid():
            order_type = form.cleaned_data['order_type']
            order_id = form.cleaned_data['order_id']
            amount = form.cleaned_data['amount']
            order_desc = form.cleaned_data['order_desc']
            bank_code = form.cleaned_data['bank_code']
            language = form.cleaned_data['language']

            #Thông tin người nhận
            name = request.POST.get('name')
            email = request.POST.get('email')
            address = request.POST.get('address')
            city = request.POST.get('city')
            state = request.POST.get('state')
            zipcode = request.POST.get('zipcode')

            ipaddr = get_client_ip(request)
            print("Tien đc day sang:")
            print(amount)
            # Build URL Payment
            vnp = vnpay()
            vnp.requestData['vnp_Version'] = '2.1.0'
            vnp.requestData['vnp_Command'] = 'pay'
            vnp.requestData['vnp_TmnCode'] = settings.VNPAY_TMN_CODE
            vnp.requestData['vnp_Amount'] = amount * 100
            vnp.requestData['vnp_CurrCode'] = 'VND'
            vnp.requestData['vnp_TxnRef'] = order_id
            vnp.requestData['vnp_OrderInfo'] = order_desc
            vnp.requestData['vnp_OrderType'] = order_type

            #Build customer info
            customer_info = {
                'name': name,
                'email': email,
                'address': address,
                'city': city,
                'state': state,
                'zipcode': zipcode 
            }
            # Save to session
            request.session['customer_info'] = customer_info

            # Check language, default: vn
            if language and language != '':
                vnp.requestData['vnp_Locale'] = language
            else:
                vnp.requestData['vnp_Locale'] = 'vn'
                # Check bank_code, if bank_code is empty, customer will be selected bank on VNPAY
            if bank_code and bank_code != "":
                vnp.requestData['vnp_BankCode'] = bank_code

            vnp.requestData['vnp_CreateDate'] = datetime.now().strftime('%Y%m%d%H%M%S')  # 20150410063022
            vnp.requestData['vnp_IpAddr'] = ipaddr
            vnp.requestData['vnp_ReturnUrl'] = settings.VNPAY_RETURN_URL
            vnpay_payment_url = vnp.get_payment_url(settings.VNPAY_PAYMENT_URL, settings.VNPAY_HASH_SECRET_KEY)
            print('Link đường dẫn qua sanbox: ')
            print(vnpay_payment_url)
            return redirect(vnpay_payment_url)
        else:
            print("Bị lỗi gì đó")
            print(form.errors)
            # Return form with errors
            return render(request, "payment/payment_request.html", {
                "form": form,
                "title": "Thanh toán",
            })
    else:
        return render(request, "payment/payment_request.html", {"title": "Thanh toán"})


def payment_ipn(request):
    inputData = request.GET
    if inputData:
        vnp = vnpay()
        vnp.responseData = inputData.dict()
        order_id = inputData['vnp_TxnRef']
        amount = inputData['vnp_Amount']
        order_desc = inputData['vnp_OrderInfo']
        vnp_TransactionNo = inputData['vnp_TransactionNo']
        vnp_ResponseCode = inputData['vnp_ResponseCode']
        vnp_TmnCode = inputData['vnp_TmnCode']
        vnp_PayDate = inputData['vnp_PayDate']
        vnp_BankCode = inputData['vnp_BankCode']
        vnp_CardType = inputData['vnp_CardType']

        if vnp.validate_response(settings.VNPAY_HASH_SECRET_KEY):
            # Check & Update Order Status in your Database
            # Your code here
            firstTimeUpdate = True
            totalamount = True
            if totalamount:
                if firstTimeUpdate:
                    if vnp_ResponseCode == '00':
                        print('Payment Success. Your code implement here')
                    else:
                        print('Payment Error. Your code implement here')

                    # Return VNPAY: Merchant update success
                    result = JsonResponse({'RspCode': '00', 'Message': 'Confirm Success'})
                else:
                    # Already Update
                    result = JsonResponse({'RspCode': '02', 'Message': 'Order Already Update'})
            else:
                # invalid amount
                result = JsonResponse({'RspCode': '04', 'Message': 'invalid amount'})
        else:
            # Invalid Signature
            result = JsonResponse({'RspCode': '97', 'Message': 'Invalid Signature'})
    else:
        result = JsonResponse({'RspCode': '99', 'Message': 'Invalid request'})

    return result


def payment_return(request):
    inputData = request.GET
    print("---" + str(request.user))
    customer = request.user
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    if inputData:
        vnp = vnpay()
        vnp.responseData = inputData.dict()
        order_id = inputData['vnp_TxnRef']
        amount = int(inputData['vnp_Amount']) / 100
        order_desc = inputData['vnp_OrderInfo']
        vnp_TransactionNo = inputData['vnp_TransactionNo']
        vnp_ResponseCode = inputData['vnp_ResponseCode']
        vnp_TmnCode = inputData['vnp_TmnCode']
        vnp_PayDate = inputData['vnp_PayDate']
        vnp_BankCode = inputData['vnp_BankCode']
        vnp_CardType = inputData['vnp_CardType']

        #Thông tin người nhận
        customer_info = request.session.get('customer_info')

        name = customer_info.get('name')
        email = customer_info.get('email')
        address = customer_info.get('address')
        city = customer_info.get('city')
        state = customer_info.get('state')
        zipcode = customer_info.get('zipcode')


        payment_record = PaymentRecord.objects.create(
            order_id=order_id,
            amount=amount,
            order_desc=order_desc,
            transaction_no=vnp_TransactionNo,
            response_code=vnp_ResponseCode,
           
            bank_code=vnp_BankCode,
            card_type=vnp_CardType,
            success=(vnp_ResponseCode == "00")
        )

        if vnp.validate_response(settings.VNPAY_HASH_SECRET_KEY):
            if vnp_ResponseCode == "00":

                ShippingAddress.objects.create(
                    order=order,
                    name=name,
                    email=email,
                    address=address,
                    city=city,
                    state=state,
                    zipcode=zipcode
                )

                order.complete = True
                order.save()

                return render(request, "payment/payment_return.html",
                              {
                                   "title": "Kết quả thanh toán",
                                   "result": "Thành công", "order_id": order_id,
                                   "amount": amount,
                                   "order_desc": order_desc,
                                   "vnp_TransactionNo": vnp_TransactionNo,
                                   "vnp_ResponseCode": vnp_ResponseCode,
                                   "name": name, 
                                   "email":email, 
                                   "address": address,
                                   "city": city,
                                   "state": state,
                                   "zipcode": zipcode
                               })
            else:
                return render(request, "payment/payment_return.html",
                              {
                                  "title": "Kết quả thanh toán",
                                  "result": "Lỗi", "order_id": order_id,
                                  "amount": amount,
                                  "order_desc": order_desc,
                                  "vnp_TransactionNo": vnp_TransactionNo,
                                  "vnp_ResponseCode": vnp_ResponseCode,
                                   "name": name, 
                                   "email":email, 
                                   "address": address,
                                   "city": city,
                                   "state": state,
                                   "zipcode": zipcode
                              })
        else:
            return render(request, "payment/payment_return.html",
                          {
                              "title": "Kết quả thanh toán",
                              "result": "Lỗi", "order_id": order_id, "amount": amount,
                              "order_desc": order_desc, "vnp_TransactionNo": vnp_TransactionNo,
                              "vnp_ResponseCode": vnp_ResponseCode, "msg": "Sai checksum",
                                   "name": name, 
                                   "email":email, 
                                   "address": address,
                                   "city": city,
                                   "state": state,
                                   "zipcode": zipcode
                          })
    else:
        return render(request, "payment/payment_return.html", {"title": "Kết quả thanh toán", "result": ""})


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

n = random.randint(10**11, 10**12 - 1)
n_str = str(n)
while len(n_str) < 12:
    n_str = '0' + n_str


def query(request):
    if request.method == 'GET':
        return render(request, "payment/query.html", {"title": "Kiểm tra kết quả giao dịch"})

    url = settings.VNPAY_API_URL
    secret_key = settings.VNPAY_HASH_SECRET_KEY
    vnp_TmnCode = settings.VNPAY_TMN_CODE
    vnp_Version = '2.1.0'

    vnp_RequestId = n_str
    vnp_Command = 'querydr'
    vnp_TxnRef = request.POST['order_id']
    vnp_OrderInfo = 'kiem tra gd'
    vnp_TransactionDate = request.POST['trans_date']
    vnp_CreateDate = datetime.now().strftime('%Y%m%d%H%M%S')
    vnp_IpAddr = get_client_ip(request)

    hash_data = "|".join([
        vnp_RequestId, vnp_Version, vnp_Command, vnp_TmnCode,
        vnp_TxnRef, vnp_TransactionDate, vnp_CreateDate,
        vnp_IpAddr, vnp_OrderInfo
    ])

    secure_hash = hmac.new(secret_key.encode(), hash_data.encode(), hashlib.sha512).hexdigest()

    data = {
        "vnp_RequestId": vnp_RequestId,
        "vnp_TmnCode": vnp_TmnCode,
        "vnp_Command": vnp_Command,
        "vnp_TxnRef": vnp_TxnRef,
        "vnp_OrderInfo": vnp_OrderInfo,
        "vnp_TransactionDate": vnp_TransactionDate,
        "vnp_CreateDate": vnp_CreateDate,
        "vnp_IpAddr": vnp_IpAddr,
        "vnp_Version": vnp_Version,
        "vnp_SecureHash": secure_hash
    }

    headers = {"Content-Type": "application/json"}

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        response_json = json.loads(response.text)
    else:
        response_json = {"error": f"Request failed with status code: {response.status_code}"}

    return render(request, "payment/query.html", {"title": "Kiểm tra kết quả giao dịch", "response_json": response_json})

def refund(request):
    if request.method == 'GET':
        return render(request, "payment/refund.html", {"title": "Hoàn tiền giao dịch"})

    url = settings.VNPAY_API_URL
    secret_key = settings.VNPAY_HASH_SECRET_KEY
    vnp_TmnCode = settings.VNPAY_TMN_CODE
    vnp_RequestId = n_str
    vnp_Version = '2.1.0'
    vnp_Command = 'refund'
    vnp_TransactionType = request.POST['TransactionType']
    vnp_TxnRef = request.POST['order_id']
    vnp_Amount = request.POST['amount']
    vnp_OrderInfo = request.POST['order_desc']
    vnp_TransactionNo = '0'
    vnp_TransactionDate = request.POST['trans_date']
    vnp_CreateDate = datetime.now().strftime('%Y%m%d%H%M%S')
    vnp_CreateBy = 'user01'
    vnp_IpAddr = get_client_ip(request)

    hash_data = "|".join([
        vnp_RequestId, vnp_Version, vnp_Command, vnp_TmnCode, vnp_TransactionType, vnp_TxnRef,
        vnp_Amount, vnp_TransactionNo, vnp_TransactionDate, vnp_CreateBy, vnp_CreateDate,
        vnp_IpAddr, vnp_OrderInfo
    ])

    secure_hash = hmac.new(secret_key.encode(), hash_data.encode(), hashlib.sha512).hexdigest()

    data = {
        "vnp_RequestId": vnp_RequestId,
        "vnp_TmnCode": vnp_TmnCode,
        "vnp_Command": vnp_Command,
        "vnp_TxnRef": vnp_TxnRef,
        "vnp_Amount": vnp_Amount,
        "vnp_OrderInfo": vnp_OrderInfo,
        "vnp_TransactionDate": vnp_TransactionDate,
        "vnp_CreateDate": vnp_CreateDate,
        "vnp_IpAddr": vnp_IpAddr,
        "vnp_TransactionType": vnp_TransactionType,
        "vnp_TransactionNo": vnp_TransactionNo,
        "vnp_CreateBy": vnp_CreateBy,
        "vnp_Version": vnp_Version,
        "vnp_SecureHash": secure_hash
    }

    headers = {"Content-Type": "application/json"}

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        response_json = json.loads(response.text)
    else:
        response_json = {"error": f"Request failed with status code: {response.status_code}"}

    return render(request, "payment/refund.html", {"title": "Kết quả hoàn tiền giao dịch", "response_json": response_json})