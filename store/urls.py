from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('clear-session/', views.clear_session, name='clear-session'),
    path('category/<slug:category_slug>/', views.products_by_category, name='category_products'),
    path('new-clothing/', views.new_clothing, name='new_clothing'),
    path('thrift-clothing/', views.thrift_clothing, name='thrift_clothing'),
    path('category/<slug:category_slug>/', views.products_by_category, name='products_by_category'),
    path('category/<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.add_to_cart_view, name='add_to_cart'),
    path('cart/remove/<int:cart_item_id>/', views.remove_from_cart_view, name='remove_from_cart'),
    path('cart/update/<int:cart_item_id>/', views.update_cart_item_view, name='update_cart_item'),
]