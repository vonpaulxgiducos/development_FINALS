# api/product_models.py

#from django.db import models

#class Product(models.Model):
#    name = models.CharField(max_length=200)
#    description = models.TextField()
#    price = models.DecimalField(max_digits=10, decimal_places=2)
#    image_url = models.URLField()
#    added_on = models.DateTimeField(auto_now_add=True)
#
#    def __str__(self):
#        return self.name


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
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Checkout {self.id} - Total Price: {self.total_price}"

# Payment model (added)
class Payment(models.Model):
    checkout = models.OneToOneField(Checkout, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=100)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=50, default="Pending")

    def __str__(self):
        return f"Payment for Checkout {self.checkout.id} via {self.payment_method}"
