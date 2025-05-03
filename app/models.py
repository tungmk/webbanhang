from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.utils import timezone

# Tài khoản khách hàng
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200)

    def __str__(self):
        return self.name or str(self.user)

# Danh mục sản phẩm
class Category(models.Model):
    sub_category = models.ForeignKey('self', on_delete=models.CASCADE, related_name='sub_categories', null=True, blank=True)
    is_sub = models.BooleanField(default=False)
    name = models.CharField(max_length=200, null=True)
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return self.name

# Đăng ký người dùng
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

# Sản phẩm
class Product(models.Model):
    category = models.ManyToManyField(Category, related_name='products')
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField()
    digital = models.BooleanField(default=False, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def ImageURL(self):
        try:
            return self.image.url
        except:
            return ''

# Đơn hàng
class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date_order = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=True)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return f"Order #{self.id}"

    @property
    def get_cart_items(self):
        return sum(item.quantity for item in self.orderitem_set.all())

    @property
    def get_cart_total(self):
        return sum(item.get_total for item in self.orderitem_set.all())

# Sản phẩm trong giỏ hàng
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        return self.product.price * self.quantity

# Địa chỉ giao hàng
class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=20, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address or "Shipping Address"

# Biến thể sản phẩm (màu, size, ...)
variation_category_choice = (
    ('color', 'Color'),
    ('size', 'Size'),
)

class VariationManager(models.Manager):
    def colors(self):
        return self.filter(variation_category='color', is_active=True)

    def sizes(self):
        return self.filter(variation_category='size', is_active=True)

class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variations')
    variation_category = models.CharField(max_length=100, choices=variation_category_choice)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)

    objects = VariationManager()

    def __str__(self):
        return f"{self.variation_category}: {self.variation_value}"

class Payment(models.Model):
    PAYMENT_METHODS = (
        ('cod', 'Thanh toán khi nhận hàng'),
        ('vnpay', 'VNPay'),
        ('momo', 'Momo'),
        ('banking', 'Chuyển khoản'),
    )

    STATUS_CHOICES = (
        ('pending', 'Đang xử lý'),
        ('completed', 'Thành công'),
        ('failed', 'Thất bại'),
    )

    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='cod')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    amount = models.FloatField()
    transaction_code = models.CharField(max_length=255, null=True, blank=True)
    paid_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_method_display()} - {self.get_status_display()} - Order #{self.order.id}"

class Payment_success(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    payment_method = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.payment_method} - {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"

class PaymentForm(forms.Form):

    order_id = forms.CharField(max_length=250)
    order_type = forms.CharField(max_length=20)
    amount = forms.IntegerField()
    order_desc = forms.CharField(max_length=200)
    bank_code = forms.CharField(max_length=20, required=False)
    language = forms.CharField(max_length=2)

class PaymentRecord(models.Model):
    order_id = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_desc = models.TextField()
    transaction_no = models.CharField(max_length=255)
    response_code = models.CharField(max_length=10)
    payment_date = models.DateTimeField(default=timezone.now, blank=True, null=True)
    bank_code = models.CharField(max_length=10)
    card_type = models.CharField(max_length=20)
    success = models.BooleanField(default=False)
    