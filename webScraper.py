from bs4 import BeautifulSoup
from urllib.request import urlopen
from decimal import Decimal


def getInfo():
    p = set()
    info = {}
    url = "https://www.lidl.co.uk/food-offers"

    def crawl(url, n):
        if n > 15:
            return
        try:
            page = urlopen(url)
        except:
            return
        html = page.read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")

        for link in soup.find_all('a'):
            l = link.get('href')
            if "/p/" in l:
                if l not in p:
                    if n != 0:
                        title = soup.find("h1",
                                          {"class": "attributebox__headline attributebox__headline--h1"}).text.strip()
                        price = Decimal(soup.find("span", {"class": "pricebox__price"}).text.strip().split(" ")[1])
                        desc = soup.find("article", {"class": "textbody"})
                        data = "/n".join([d.text for d in desc.find_all("li")])
                        new_url = "https://www.lidl.co.uk" + l
                        info[title] = [price, data, new_url]
                    else:
                        new_url = "https://www.lidl.co.uk" + l

                    p.add(l)
                    crawl(new_url, n + 1)

    crawl(url, 0)
    return info
