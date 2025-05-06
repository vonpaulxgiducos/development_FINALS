# api/product_urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .product_views import ProductViewSet, CartViewSet, CheckoutViewSet, PaymentViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'cart', CartViewSet)
router.register(r'checkout', CheckoutViewSet)
router.register(r'payments', PaymentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]