# api/product_views.py

#from django.shortcuts import render
#from .models import Product

#def product_list(request):
    # Fetch all products from the database
#    products = Product.objects.all()
#    return render(request, 'products.html', {'products': products})

#product_views.py
from rest_framework import viewsets
from .product_models import Product, Cart, Checkout
from .serializers import ProductSerializer, CartSerializer, CheckoutSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

class CheckoutViewSet(viewsets.ModelViewSet):
    queryset = Checkout.objects.all()
    serializer_class = CheckoutSerializer

