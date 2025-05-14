# Modified serializers.py
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
        
        # Check if an existing cart with this product exists
        existing_item = CartItem.objects.filter(product=product).first()
        
        if existing_item:
            # Update existing item quantity instead of creating a new one
            existing_item.quantity = quantity
            existing_item.save()
            return existing_item.cart_set.first() or Cart.objects.create()
        else:
            # Create new cart and item
            cart = Cart.objects.create()
            cart_item = CartItem.objects.create(
                product=product,
                quantity=quantity
            )
            cart.items.add(cart_item)
            return cart

class CheckoutSerializer(serializers.ModelSerializer):
    cart = serializers.PrimaryKeyRelatedField(queryset=Cart.objects.all())
    customer_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    phone = serializers.CharField(required=True)
    shipping_address = serializers.CharField(required=True)

    class Meta:
        model = Checkout
        fields = ['id', 'cart', 'total_price', 'customer_name', 'email', 
                 'phone', 'shipping_address', 'notes', 'status', 'created_at']

    def create(self, validated_data):
        cart = validated_data.get('cart')
        if not cart or not cart.items.exists():
            raise serializers.ValidationError("Cart is empty or invalid")
        
        total_price = sum(
            item.product.price * item.quantity 
            for item in cart.items.all()
        )
        
        checkout = Checkout.objects.create(
            cart=cart,
            total_price=total_price,
            customer_name=validated_data.get('customer_name'),
            email=validated_data.get('email'),
            phone=validated_data.get('phone'),
            shipping_address=validated_data.get('shipping_address'),
            notes=validated_data.get('notes', ''),
            status='pending'
        )
        
        return checkout

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'checkout', 'payment_method', 'payment_status', 'payment_date']
        
        fields = '__all__'

# Add this line at the end of the file
__all__ = ['ProductSerializer', 'CartSerializer', 'CartItemSerializer', 'CheckoutSerializer']


        