from django.db import models
from django.core.validators import MinValueValidator
# Create your models here.


class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()


class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey(
        'Product', on_delete=models.SET_NULL, null=True, related_name='+')  # Use + sign to tell django not create the reverse relationship

    # TO change the string representation we override the __str__
    def __str__(self) -> str:
        return self.title

    # Define Meta class to specify the default ordering of collection objects
    class Meta:
        ordering = ['title']


class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    # blank tells the admin page that field is not required
    description = models.TextField(null=True, blank=True)
    unit_price = models.DecimalField(
        max_digits=7,
        decimal_places=3,
        validators=[MinValueValidator(1)])
    inventory = models.IntegerField(validators=[MinValueValidator(1)])
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(
        Collection, on_delete=models.PROTECT)
    promotions = models.ManyToManyField(Promotion, blank=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ['title']


class Customer(models.Model):

    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'
    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, 'BRONZE'),
        (MEMBERSHIP_SILVER, 'SILVER'),
        (MEMBERSHIP_GOLD, 'GOLD')
    ]

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)
    membership = models.CharField(
        max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'

    class Meta:
        ordering = ['first_name', 'last_name']


class Order(models.Model):

    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'

    PAYMENT_STATUS = [
        (PAYMENT_STATUS_PENDING, 'PENDING'),
        (PAYMENT_STATUS_COMPLETE, 'COMPLETE'),
        (PAYMENT_STATUS_FAILED, 'FAILED')
    ]

    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(
        max_length=1, choices=PAYMENT_STATUS, default=PAYMENT_STATUS_PENDING)

    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.SmallIntegerField()
    unit_price = models.DecimalField(max_digits=7, decimal_places=3)


# One to One relationship between address and Customer
# Each Customer only has one address and each address
# belongs to only one Customer
# Address class is child of Customer so it should exist
# after Customer is created
class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)

    # Specify parent
    # If we dont set primary key to true
    # Django will create another id key
    # for each address and then we will be able
    # to have multiple addresses for one customer
    # customer = models.OneToOneField(
    #    Customer, on_delete=models.CASCADE, primary_key=True)

    # If we want to allow each customer to have more than one
    # address then we need to define OneToManyRelationship
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)


class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)

    # Here we use cascade because if we delete a product
    # It means that this product has never been ordered
    # before because orderItem has product protected,
    # so we delete it from the cart too
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
