import decimal
import re

import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
from decimal import Decimal


def getMorrisonsData():
    p = set()
    info = {}
    home_url = "https://groceries.morrisons.com"
    start_urls = ["https://groceries.morrisons.com/browse/beer-wines-spirits-103120/wine-champagne-176432",
                  "https://groceries.morrisons.com/browse/fish-seafood-184367",
                  "https://groceries.morrisons.com/browse/bakery-cakes-102210/bread-165657",
                  "https://groceries.morrisons.com/browse/drinks-103644/coffee-161007",
                  "https://groceries.morrisons.com/browse/fruit-veg-176738/vegetables-176756"
                  "https://groceries.morrisons.com/browse/frozen-180331",
                  "https://groceries.morrisons.com/browse/fresh-176739"]

    def crawl(url, n):
        if n > 15:
            return
        try:
            page = requests.get(url)
        except:
            print("invalid url")
            return
        soup = BeautifulSoup(page.content, "html.parser")

        if n != 0:
            try:
                title = soup.find("h1").text.strip()
                price = soup.find("h2", {"class": "bop-price__current"}).text.strip()[1:]
                desc = soup.find("div", {"class": "gn-accordionElement__wrapper"}).get_text(separator="\n")
                img_src = soup.find("img", {"class": "bop-gallery__image"}).get('src')
                info[title] = {"price": price, "desc": desc, "url": url, "retailer": "Morrisons", "img_src": home_url+img_src}
            except AttributeError as ae:
                print("attribute error with url:", url)
            except decimal.InvalidOperation as io:
                print("invalid conversion with url:", url)

        for link in soup.find_all('a', href=re.compile("/products/")):
            l = link.get('href')
            if l not in p:
                p.add(l)
                new_l = home_url + l
                crawl(new_l, n + 1)

    for i in range(len(start_urls)):
        print("Now working on url", i+1, "of", len(start_urls))
        crawl(start_urls[i], 0)
    return info


#getMorrisonsData()
