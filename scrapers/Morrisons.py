import re

import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
from decimal import Decimal


def getMorrisonsData():
    p = set()
    info = {}
    home_url = "https://groceries.morrisons.com"
    start_url = "https://groceries.morrisons.com/browse/beer-wines-spirits-103120/wine-champagne-176432"

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
            title = soup.find("h1").text.strip()
            price = Decimal(soup.find("h2", {"class": "bop-price__current"}).text.strip()[1:])
            desc = soup.find("div", {"class": "gn-accordionElement__wrapper"}).get_text(separator="\n")
            img_src = soup.find("img", {"class": "bop-gallery__image"}).get('src')
            info[title] = {"price": price, "desc": desc, "url": url, "retailer": "Morrisons", "img_src": home_url+img_src}

        for link in soup.find_all('a', href=re.compile("/products/")):
            l = link.get('href')
            if l not in p:
                p.add(l)
                new_l = home_url + l
                crawl(new_l, n + 1)

    crawl(start_url, 0)
    return info


getMorrisonsData()
