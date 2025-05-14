class ProductModelTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Test Product",
            description="Test Description",
            price=Decimal('10.99'),
            stock=100
        )

    def test_product_creation(self):
        self.assertEqual(self.product.name, "Test Product")
        self.assertEqual(self.product.description, "Test Description")
        self.assertEqual(self.product.price, Decimal('10.99'))
        self.assertEqual(self.product.stock, 100)

    def test_product_str(self):
        self.assertEqual(str(self.product), "Test Product")

class CartItemModelTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Test Product",
            description="Test Description",
            price=Decimal('10.99'),
            stock=100
        )
        self.cart_item = CartItem.objects.create(
            product=self.product,
            quantity=2
        )

    def test_cart_item_creation(self):
        self.assertEqual(self.cart_item.product, self.product)
        self.assertEqual(self.cart_item.quantity, 2)

    def test_cart_item_str(self):
        self.assertEqual(str(self.cart_item), "Test Product x 2")

    def test_default_quantity(self):
        new_cart_item = CartItem.objects.create(product=self.product)
        self.assertEqual(new_cart_item.quantity, 1)

class CartModelTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Test Product",
            description="Test Description",
            price=Decimal('10.99'),
            stock=100
        )
        self.cart_item = CartItem.objects.create(
            product=self.product,
            quantity=2
        )
        self.cart = Cart.objects.create()
        self.cart.items.add(self.cart_item)

    def test_cart_creation(self):
        self.assertEqual(self.cart.items.count(), 1)
        self.assertIn(self.cart_item, self.cart.items.all())

    def test_cart_str(self):
        self.assertEqual(str(self.cart), f"Cart {self.cart.id}")

class CheckoutModelTest(TestCase):
    def setUp(self):
        self.cart = Cart.objects.create()
        self.checkout = Checkout.objects.create(
            cart=self.cart,
            total_price=Decimal('20.99'),
            customer_name="John Doe",
            email="john@example.com",
            phone="1234567890",
            shipping_address="123 Test St",
            notes="Test notes"
        )

    def test_checkout_creation(self):
        self.assertEqual(self.checkout.cart, self.cart)
        self.assertEqual(self.checkout.total_price, Decimal('20.99'))
        self.assertEqual(self.checkout.customer_name, "John Doe")
        self.assertEqual(self.checkout.status, "pending")

    def test_checkout_str(self):
        self.assertEqual(str(self.checkout), "Checkout 1 for John Doe")

    def test_checkout_default_values(self):
        minimal_checkout = Checkout.objects.create(
            cart=self.cart,
            total_price=Decimal('10.00')
        )
        self.assertEqual(minimal_checkout.customer_name, "Guest")
        self.assertEqual(minimal_checkout.status, "pending")

class PaymentModelTest(TestCase):
    def setUp(self):
        self.cart = Cart.objects.create()
        self.checkout = Checkout.objects.create(
            cart=self.cart,
            total_price=Decimal('20.99')
        )
        self.payment = Payment.objects.create(
            checkout=self.checkout,
            payment_method="Credit Card"
        )

    def test_payment_creation(self):