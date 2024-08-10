from django.db import models
from django.contrib.auth.models import User
class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    GENDER_CHOICES = [
        ('MEN','M'),
        ('WOMEN','W'),
        ('BOTH','B')
    ]
    gender = models.CharField(max_length=5, choices=GENDER_CHOICES, default='BOTH', blank=True, null=True)
    hot = models.BooleanField(default=False)
    image = models.ImageField(upload_to='posters', blank=True, null=True, verbose_name='Poster')
    def get_image(self):
        try:
            return self.image.url
        except:
            return 'https://cdn.iconscout.com/icon/premium/png-256-thumb/insert-image-9924441-8059276.png'


class Liked(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    @property
    def get_cart_total_price(self):
        cart_products = self.cartproduct_set.all()
        total_price = sum([product.get_total_price for product in cart_products])
        return total_price

    @property
    def get_cart_total_quantity(self):
        cart_products = self.cartproduct_set.all()
        total_quantity = sum([product.quantity for product in cart_products])
        return total_quantity

    @property
    def get_cart_quantity(self):
        cart_products = self.cartproduct_set.all()
        quantity = sum([1 for product in cart_products])
        return quantity


class CartProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)

    @property
    def get_total_price(self):
        total_price = self.product.price * self.quantity
        return total_price



class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    house = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=255)



class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'

    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'In expectation'),
        (PAYMENT_STATUS_COMPLETE, 'Completed'),
        (PAYMENT_STATUS_FAILED, 'Canceled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=PAYMENT_STATUS_CHOICES,
                              default=PAYMENT_STATUS_PENDING)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, blank=True, null=True)
    placed_at = models.DateTimeField(auto_now_add=True)



class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)


