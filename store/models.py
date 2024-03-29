from django.core.validators import MinValueValidator
from django.db import models
from uuid import uuid4

class Promotion(models.Model):
   description = models.CharField(max_length=255)
   discount = models.FloatField()

class Collection(models.Model):
   title = models.CharField(max_length=255)
   featured_product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='+')

   def __str__(self):
      return self.title
   
   class Meta:
      ordering = ['title']

class Product(models.Model):
   title = models.CharField(max_length=255)
   slug = models.SlugField()
   description = models.TextField(null=True, blank=True)
   price = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(1)])
   inventory = models.IntegerField(validators=[MinValueValidator(1)])
   last_update = models.DateTimeField(auto_now=True) #data e horário; add só uma vez
   collection = models.ForeignKey(Collection, on_delete=models.PROTECT, related_name='products')
   promotions = models.ManyToManyField(Promotion, blank=True)

   def __str__(self):
      return self.title
   
   class Meta:
      ordering = ['title']

class Customer(models.Model):
   MEMBERSHIP_BRONZE = 'B'
   MEMBERSHIP_SILVER = 'S'
   MEMBERSHIP_GOLD = 'G'

   MEMBERSHIP_CHOICES = [
      (MEMBERSHIP_BRONZE, 'Bronze'),
      (MEMBERSHIP_SILVER, 'Silver'),
      (MEMBERSHIP_GOLD, 'Gold'),
   ]

   first_name = models.CharField(max_length=255)
   last_name = models.CharField(max_length=255)
   email = models.EmailField(unique=True)
   phone = models.CharField(max_length=255)
   birth_date = models.DateField(null=True) #somente data
   membership = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)

   def __str__(self):
      return f'{self.first_name} {self.last_name}'

   class Meta:
      ordering = ['first_name', 'last_name']

class Order(models.Model):
   PENDING = 'P'
   COMPLETE = 'C'
   FAILED = 'F'

   PAYMENT_STATUS = [
      (PENDING, 'Pending'),
      (COMPLETE, 'Complete'),
      (FAILED, 'Failed'),
   ]

   placed_at = models.DateTimeField(auto_now_add=True)
   payment_status = models.CharField(max_length=1, choices=PAYMENT_STATUS, default=PENDING)
   customer = models.ForeignKey('Customer', on_delete=models.PROTECT)

class OrderItem(models.Model):
   order = models.ForeignKey(Order, on_delete=models.PROTECT)
   product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='orderitems')
   quantity = models.PositiveSmallIntegerField()
   unit_price = models.DecimalField(max_digits=6, decimal_places=2)

#Part 1 - Cap 3 - video 7
class Address(models.Model):
   zip = models.CharField(max_length=10)
   street = models.CharField(max_length=255)
   city = models.CharField(max_length=255)
   customer = models.OneToOneField(Customer, on_delete=models.CASCADE, primary_key=True)

class Cart(models.Model):
   id = models.UUIDField(primary_key=True, default=uuid4)
   created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
   cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
   product = models.ForeignKey(Product, on_delete=models.CASCADE)
   quantity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])

   class Meta:
      unique_together = [['cart', 'product']]

class Review(models.Model):
   product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
   name = models.CharField(max_length=255)
   description = models.TextField()
   date = models.DateField(auto_now_add=True)