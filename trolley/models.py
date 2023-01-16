from datetime import datetime
from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    retailer = models.CharField(max_length=30, default="default/")
    desc = models.CharField(max_length=500, default="DESCRIPTION")
    picture = models.ImageField(blank=True)
    site_url = models.URLField(default="Default Val")
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Basket(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.now)

class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    data_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)
    shipping = True

    def __str__(self):
        return str(self.id)

    @property
    def calculate_basket_total(self):
        basket_items = self.orderitem_set.all()
        return sum([item.calculate_total for item in basket_items])

    @property
    def get_basket_quantities(self):
        basket_items = self.orderitem_set.all()
        return sum([item.quantity for item in basket_items])

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    data_added = models.DateTimeField(auto_now_add=True)

    @property
    def calculate_total(self):
        return self.product.price * self.quantity
