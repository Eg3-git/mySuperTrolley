import os
import django
import requests

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mySuperTrolley.settings')

django.setup()

from django.core.files import File
from trolley.models import Product
from scrapers.Lidl import getLidlData
from scrapers.Morrisons import getMorrisonsData


def populate():
    info = getLidlData()

    for title, data in info.items():
        p = add_product(title, data)

    for p in Product.objects.all():
        print(p)


def add_product(title, data):
    p = Product.objects.get_or_create(name=title)[0]
    p.price = data['price']
    p.desc = data['desc']
    p.url = data['url']
    p.retailer = data['retailer']
    p.save()

    img_data = requests.get(data['img_src']).content
    with open("temp_img.jpg", "wb") as handler:
        handler.write(img_data)

    p.picture.save(p.retailer+"/"+str(p.id)+".jpg", File(open("temp_img.jpg", "rb")))
    return p


if __name__ == '__main__':
    print("Beginning population...")
    populate()
