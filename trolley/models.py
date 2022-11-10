from django.db import models
from django.template.defaultfilters import slugify


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    desc = models.CharField(max_length=256, default="DESCRIPTION")
    url = models.URLField(name="See on official website", default="Default Val")
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
