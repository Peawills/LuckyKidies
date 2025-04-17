from django.contrib import admin
from .models import Category, Product, Cart, CartItem, Color, Size

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active')
    prepopulated_fields = {'slug': ('name',)}

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'stock', 'category', 'condition', 'is_available', 'created_date')
    list_filter = ('category', 'condition', 'is_available')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')
    list_editable = ('stock', 'is_available')
    filter_horizontal = ('colors', 'sizes')

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0

class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'session_id', 'created_date')  # Removed 'total_price'
    inlines = [CartItemInline]
    search_fields = ('user__username', 'session_id')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem)
admin.site.register(Color)
admin.site.register(Size)
