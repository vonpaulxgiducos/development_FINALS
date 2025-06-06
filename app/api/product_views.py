# Modified product_views.py
from rest_framework import viewsets, status, serializers as drf_serializers
from rest_framework.response import Response
from rest_framework.decorators import action
from .product_models import Product, Cart, CartItem, Checkout, Payment
from . import serializers


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = serializers.CartSerializer
    
    def create(self, request, *args, **kwargs):
        try:
            data = request.data.copy()
            
            # Debug the incoming request data
            print(f"Request data: {data}")
            
            # If product_id is sent instead of product, map it properly
            if 'product_id' in data and 'product' not in data:
                data['product'] = data['product_id']
                del data['product_id']
            
            print(f"Modified data: {data}")
            
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            cart = self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data, 
                status=status.HTTP_201_CREATED, 
                headers=headers
            )
        except drf_serializers.ValidationError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def perform_create(self, serializer):
        return serializer.save()





    
    @action(detail=False, methods=['delete'])
    def clear(self, request):
        """
        Clear all items from all carts
        """
        try:
            # Delete all cart items
            CartItem.objects.all().delete()
            # Optionally, delete all carts too
            Cart.objects.all().delete()
            
            return Response(
                {"message": "All carts cleared successfully"},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['post'], url_path='clear')
    def clear_item(self, request):
        """
        Remove a specific product from all carts
        """
        try:
            product_id = request.data.get('product_id')
            
            if not product_id:
                return Response(
                    {"error": "Product ID is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Find the product
            try:
                product = Product.objects.get(pk=product_id)
            except Product.DoesNotExist:
                return Response(
                    {"error": f"Product with ID {product_id} not found"},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Find and delete all cart items with this product
            items_deleted = CartItem.objects.filter(product=product).delete()
            
            return Response(
                {"message": f"Removed product {product_id} from cart", "items_deleted": items_deleted},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class CheckoutViewSet(viewsets.ModelViewSet):
    queryset = Checkout.objects.all()
    serializer_class = serializers.CheckoutSerializer

    @action(detail=False, methods=['post'])
    def process_checkout(self, request):
        try:
            # Get active cart
            cart = Cart.objects.filter(status='active').first()
            if not cart:
                return Response(
                    {"error": "No active cart found"}, 
                    status=status.HTTP_404_NOT_FOUND
                )

            # Calculate totals
            cart_items = cart.items.all()
            subtotal = sum(item.product.price * item.quantity for item in cart_items)
            shipping = 5.00  # Fixed shipping cost
            tax = subtotal * 0.12  # 12% tax
            total = subtotal + shipping + tax

            # Create checkout record
            checkout = Checkout.objects.create(
                cart=cart,
                total_price=total,
                customer_name=f"{request.data.get('firstName')} {request.data.get('lastName')}",
                email=request.data.get('email'),
                phone=request.data.get('phone'),
                shipping_address=f"{request.data.get('address')}, {request.data.get('city')}, {request.data.get('postalCode')}, {request.data.get('country')}",
                notes=request.data.get('notes', '')
            )

            # Update cart status
            cart.status = 'pending'
            cart.save()

            return Response({
                'checkout_id': checkout.id,
                'total': total,
                'message': 'Checkout created successfully'
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = serializers.PaymentSerializer

    @action(detail=False, methods=['post'], url_path='process-payment')
    def process_payment(self, request):
        """
        Process a payment and link it to a checkout.
        """
        try:
            # Extract data from the request
            checkout_id = request.data.get('checkout_id')
            payment_method = request.data.get('payment_method')
            card_name = request.data.get('card_name', None)
            card_number = request.data.get('card_number', None)
            expiry_date = request.data.get('expiry_date', None)
            amount = request.data.get('amount')

            # Validate required fields
            if not checkout_id or not payment_method or not amount:
                return Response(
                    {"error": "Missing required fields: checkout_id, payment_method, or amount"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Fetch the corresponding checkout
            try:
                checkout = Checkout.objects.get(id=checkout_id)
            except Checkout.DoesNotExist:
                return Response(
                    {"error": f"Checkout with ID {checkout_id} not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Create a payment record
            payment = Payment.objects.create(
                checkout=checkout,
                payment_method=payment_method,
                card_name=card_name,
                card_number=card_number,
                expiry_date=expiry_date,
                amount=amount,
                status='completed'
            )

            # Update the checkout status to 'paid'
            checkout.status = 'paid'
            checkout.save()

            return Response(
                {
                    "message": "Payment processed successfully",
                    "payment_id": payment.id,
                    "checkout_id": checkout.id,
                    "amount": amount,
                },
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )



