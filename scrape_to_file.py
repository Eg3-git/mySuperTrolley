import json
import shutil
import requests

from scrapers.Lidl import getLidlData
from scrapers.Morrisons import getMorrisonsData


def populate():
    count = 0
    count = process_data(getLidlData(), "Lidl", count)
    count = process_data(getMorrisonsData(), "Morrisons", count)


def process_data(info, retailer, count):
    print("Adding products to file")
    save_loc = 'scraped_data/'+retailer+'_data.json'
    new_count = add_images(info, count)
    with open(save_loc, 'w') as f:
        f.write(json.dumps(info))

    return new_count


def add_images(info, count):
    for title, data in info.items():
        count+=1
        img_data = requests.get(data['img_src']).content
        with open("temp_img.jpg", "wb") as handler:
            handler.write(img_data)

        shutil.copy("temp_img.jpg", "scraped_data/imgs/"+str(count)+".jpg")
        data['img_no'] = count
    return count


if __name__ == '__main__':
    print("Beginning population...")
    populate()
