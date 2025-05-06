#serializer.py
from rest_framework import serializers
from .product_models import Product, Cart, CartItem, Checkout, Payment

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock']

class CartItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'added_at']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        write_only=True
    )
    quantity = serializers.IntegerField(write_only=True, min_value=1, default=1)

    class Meta:
        model = Cart
        fields = ['id', 'items', 'created_at', 'product', 'quantity']

    def create(self, validated_data):
        product = validated_data.pop('product')
        quantity = validated_data.pop('quantity')
        
        cart = Cart.objects.create()
        cart_item = CartItem.objects.create(
            product=product,
            quantity=quantity
        )
        cart.items.add(cart_item)
        return cart

class CheckoutSerializer(serializers.ModelSerializer):
    cart = serializers.PrimaryKeyRelatedField(queryset=Cart.objects.all())
    total_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True
    )

    class Meta:
        model = Checkout
        fields = ['id', 'cart', 'total_price', 'created_at']

    def create(self, validated_data):
        cart = validated_data.get('cart')
        if not cart or not cart.items.exists():
            raise serializers.ValidationError("Cart is empty or invalid")
        
        total_price = sum(
            item.product.price * item.quantity 
            for item in cart.items.all()
        )
        
        return Checkout.objects.create(
            cart=cart,
            total_price=total_price
        )

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'checkout', 'payment_method', 'payment_status', 'payment_date']

# Add this line at the end of the file
__all__ = ['ProductSerializer', 'CartSerializer', 'CartItemSerializer', 'CheckoutSerializer']