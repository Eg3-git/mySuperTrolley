import decimal
import json
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mySuperTrolley.settings')
django.setup()

from django.core.files import File
from trolley.models import Product
from decimal import Decimal

def populate():
    directory = os.fsencode('scraped_data')

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".json"):
            with open('scraped_data/'+filename) as f:
                info = json.load(f)

            process_data(info)

def process_data(info):
    count = 0
    print("Adding products to database")
    for title, data in info.items():
        p = add_product(title, data)
        count += 1
    print("Added", count, "to database")


def add_product(title, data):
    try:
        price_as_decimal = Decimal(data['price'])
    except decimal.InvalidOperation as io:
        return None

    p = Product.objects.get_or_create(name=title)[0]
    p.price = price_as_decimal
    p.desc = data['desc']
    p.site_url = data['url']
    p.retailer = data['retailer']
    p.save()

    p.picture.save(p.retailer + "/" + str(p.id) + ".jpg", File(open("scraped_data/imgs/"+str(data['img_no'])+".jpg", "rb")))
    return p


if __name__ == '__main__':
    print("Beginning population...")
    populate()
