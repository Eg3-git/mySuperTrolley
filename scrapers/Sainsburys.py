import re

from bs4 import BeautifulSoup
from urllib.request import urlopen
from decimal import Decimal


def getSainsburysData():
    p = set()
    info = {}
    url = "https://www.sainsburys.co.uk/shop/gb/groceries/drinks/all-wine-?fromMegaNav=1#langId=44&storeId=10151&catalogId=10241&categoryId=258772&parent_category_rn=12192&top_category=12192&pageSize=60&orderBy=FAVOURITES_ONLY%7CSEQUENCING%7CTOP_SELLERS&searchTerm=&beginIndex=0&hideFilters=true&facet=&facet=&facet="

    def crawl(url, n):
        if n > 15:
            return
        try:
            page = urlopen(url)
        except:
            return
        html = page.read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")

        if n != 0:
            try:
                title = soup.find("h1", {"class": "pd__header"}).text.strip()
            except:
                print(url)
                return
            print(title)
            price = Decimal(soup.find("span", {"data-test-id": "price-with-nectar"}).text.strip()[1:])
            desc = soup.find("div", {"class": "itemTypeGroupContainer productText"})
            data = "/n".join([d.text for d in desc.find_all("p")])
            # new_url = "https://www.lidl.co.uk" + l
            info[title] = [price, data, url]
        else:
            pass
            # new_url = "https://www.lidl.co.uk" + l

        for link in soup.find_all('a', href=re.compile("/product/")):
            l = link.get('href')
            if l not in p:
                p.add(l)
                crawl(l, n + 1)

    crawl(url, 0)
    return info
getSainsburysData()