import decimal
import re

import requests
from bs4 import BeautifulSoup
from decimal import Decimal


def getLidlData():
    p = set()
    info = {}
    home_url = "https://www.lidl.co.uk"
    start_urls = ["https://www.lidl.co.uk/food-offers",
                  "https://www.lidl.co.uk/our-products/wines-beers-spirits/wines/all-wine",
                  "https://www.lidl.co.uk/our-products/big-on-scottish/view-our-scottish-range"
                  "https://www.lidl.co.uk/our-products/chilled",
                  "https://www.lidl.co.uk/our-products/eggs"]

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
                title = soup.find("h1", {"class": "attributebox__headline attributebox__headline--h1"}).text.strip()
                price = Decimal(soup.find("span", {"class": "pricebox__price"}).text.strip().split(" ")[1])
                desc = soup.find("article", {"class": "textbody"}).get_text(separator="\n")
                img_src = soup.find("img", {"class": "lazyload"}).get('src')
                info[title] = {"price": price, "desc": desc, "url": url, "retailer": "Lidl", "img_src": img_src}
            except AttributeError as ae:
                print("attribute error with url:", url)
            except decimal.InvalidOperation as io:
                print("invalid conversion with url:", url)

        for link in soup.find_all('a', href=re.compile("/p/")):
            l = link.get('href')
            if l not in p:
                p.add(l)
                new_l = home_url + l
                crawl(new_l, n + 1)

    for i in range(len(start_urls)):
        print("Now working on url", i+1, "of", len(start_urls))
        crawl(start_urls[i], 0)
    return info


#getLidlData()
