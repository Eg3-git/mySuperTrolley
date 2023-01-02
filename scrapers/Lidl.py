import re

import requests
from bs4 import BeautifulSoup
from decimal import Decimal


def getLidlData():
    p = set()
    info = {}
    home_url = "https://www.lidl.co.uk"
    start_url = "https://www.lidl.co.uk/food-offers"

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
            title = soup.find("h1", {"class": "attributebox__headline attributebox__headline--h1"}).text.strip()
            price = Decimal(soup.find("span", {"class": "pricebox__price"}).text.strip().split(" ")[1])
            data = soup.find("article", {"class": "textbody"})
            desc = "/n".join([d.text for d in data.find_all("li")])
            img_src = soup.find("img", {"class": "lazyload"}).get('src')
            info[title] = {"price": price, "desc": desc, "url": url, "retailer": "Lidl", "img_src": img_src}

        for link in soup.find_all('a', href=re.compile("/p/")):
            l = link.get('href')
            if l not in p:
                p.add(l)
                new_l = home_url + l
                crawl(new_l, n + 1)

    crawl(start_url, 0)
    return info


getLidlData()
