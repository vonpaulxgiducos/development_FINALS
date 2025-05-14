# api/product_models.py
from django.db import models

# Product model
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
 

    def __str__(self):
        return self.name

# CartItem model
class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

# Cart model
class Cart(models.Model):
    items = models.ManyToManyField(CartItem)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart {self.id}"

# Checkout model
class Checkout(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    customer_name = models.CharField(max_length=100, null=True, blank=True, default='Guest')
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    shipping_address = models.TextField(null=True, blank=True)
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, default='pending')
    cart_items = models.JSONField(default=list)

    def __str__(self):
        return f"Checkout {self.id} for {self.customer_name or 'Guest'}"

# Payment model (added)
#class Payment(models.Model):
#    checkout = models.ForeignKey(Checkout, on_delete=models.CASCADE)
#    payment_method = models.CharField(max_length=50)
#    card_name = models.CharField(max_length=255, null=True, blank=True)
#    card_number = models.CharField(max_length=20, null=True, blank=True)
#    expiry_date = models.CharField(max_length=10, null=True, blank=True)
#    amount = models.DecimalField(max_digits=10, decimal_places=2)
#    status = models.CharField(max_length=20, default='pending')
#    created_at = models.DateTimeField(auto_now_add=True)

class Payment(models.Model):
    checkout = models.ForeignKey(Checkout, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=50)
    card_name = models.CharField(max_length=255, null=True, blank=True)
    card_number = models.CharField(max_length=20, null=True, blank=True)
    expiry_date = models.CharField(max_length=10, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'api_payment'

    def __str__(self):
        return f"Payment for Checkout {self.checkout.id} via {self.payment_method}"

#    checkout = models.OneToOneField(Checkout, on_delete=models.CASCADE)
#    payment_method = models.CharField(max_length=100)
#    payment_date = models.DateTimeField(auto_now_add=True)
#    payment_status = models.CharField(max_length=50, default="Pending")
    
#    checkout = models.ForeignKey(Checkout, on_delete=models.CASCADE)
#    payment_method = models.CharField(max_length=50)
#    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
#    payment_date = models.DateTimeField(auto_now_add=True)

#    checkout = models.ForeignKey('Checkout', on_delete=models.CASCADE)
#    payment_method = models.CharField(max_length=50, default='creditCard')  
#    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
#    card_name = models.CharField(max_length=255, null=True, blank=True)
#    card_number = models.CharField(max_length=20, null=True, blank=True)
#    expiry_date = models.CharField(max_length=10, null=True, blank=True)
#    status = models.CharField(max_length=20, default='pending')
#    created_at = models.DateTimeField(auto_now_add=True)

    

#    class Meta:
#        db_table = 'api_payment'
#
#    def __str__(self):
#        return f"Payment for Checkout {self.checkout.id} via {self.payment_method}"


        















