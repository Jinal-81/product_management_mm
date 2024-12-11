from django.urls import path
from .views import (ProductListCreateAPIView, ProductDetailAPIView, DiscountListCreateAPIView, DiscountDetailAPIView,
                    OrderListCreateAPIView,OrderDetailAPIView)


urlpatterns = [
    path('products/', ProductListCreateAPIView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductDetailAPIView.as_view(), name='product-detail'),

    path('discounts/', DiscountListCreateAPIView.as_view(), name='discount-list-create'),
    path('discounts/<int:pk>/', DiscountDetailAPIView.as_view(), name='discount-detail'),

    path('orders/', OrderListCreateAPIView.as_view(), name='order-list-create'),
    path('orders/<int:pk>/', OrderDetailAPIView.as_view(), name='order-detail'),
]
