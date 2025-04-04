from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

CATEGORY_TYPE_CHOICES = [
    ('new', 'New'),
    ('thrift', 'Thrift'),
]

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    category_type = models.CharField(max_length=6, choices=CATEGORY_TYPE_CHOICES, default='new')  # Set default to 'new'

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_url(self):
        return reverse('products_by_category', args=[self.slug])

    def __str__(self):
        return self.name



class Product(models.Model):
    CONDITION_CHOICES = [
        ('new', 'New'),
        ('thrift', 'Thrift'),
    ]

    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(max_length=500, blank=True)
    image = models.ImageField(upload_to='photos/products')
    stock = models.IntegerField()
    condition = models.CharField(max_length=6, choices=CONDITION_CHOICES, default='new')
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.CharField(max_length=100, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart {self.id}"

    @property
    def total_price(self):
        """Since there's no price field in Product, this should return 0"""
        return 0  # or implement alternative logic

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    @property
    def subtotal(self):
        """Since there's no price field, return 0 or implement alternative logic"""
        return 0  # or another logic if needed
