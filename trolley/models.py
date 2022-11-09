from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=128)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    desc = models.CharField(max_length=256, default="DESCRIPTION")
    url = models.URLField(name="See on official website", default="Default Val")

    def __str__(self):
        return self.name
