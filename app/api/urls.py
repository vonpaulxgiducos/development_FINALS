from django.urls import path, include
from .views import HelloWorld, ContactListView, ContactUpdateDetailView
from rest_framework.routers import DefaultRouter
from .product_views import ProductViewSet, CartViewSet, CheckoutViewSet

# Create a router for viewsets
router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'cart', CartViewSet)
router.register(r'checkout', CheckoutViewSet)

urlpatterns = [
    path('hello/', HelloWorld.as_view(), name='hello_world'),
    path('contact/', ContactListView.as_view(), name='contact_new'),
    path('contact/<int:contact_id>/', ContactListView.as_view(), name='contact_detail'),
    path('contacts/', ContactListView.as_view(), name='contact_list'),
    path('contacts/<int:contact_id>/', ContactUpdateDetailView.as_view(), name='contact_update_detail'),
    path('', include(router.urls)),  # Include router URLs
    # REMOVE THIS LINE: path('api/', include('api.urls')),  
]