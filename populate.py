import os
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mySuperTrolley.settings')

django.setup()

from trolley.models import Product
from scrapers.Lidl import getLidlData


def populate():
    info = getLidlData()

    for title, data in info.items():
        p = add_product(title, data)

    for p in Product.objects.all():
        print(p)


def add_product(title, data):
    p = Product.objects.get_or_create(name=title)[0]
    p.price = data[0]
    p.desc = data[1]
    p.url = data[2]
    p.save()
    return p


if __name__ == '__main__':
    print("Beginning population...")
    populate()
