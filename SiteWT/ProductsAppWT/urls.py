
from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
   
    path('', views.index),
    path('products/', views.products),
    path('details/<int:id>/', views.product_detail, name='product_detail'),
    path('add/', views.product_add, name='product_add'),
    path('update/<int:id>/', views.product_update, name='product_update'),
    path('delete/<int:id>/', views.product_delete, name='product_delete'),
    path('coinbase/', views.coinbase_data, name='coinbase'),
    path('historical/', views.historical_data, name='historical_view')
    
]
