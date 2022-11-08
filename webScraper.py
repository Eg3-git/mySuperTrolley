from bs4 import BeautifulSoup
from urllib.request import urlopen

#url = "https://www.lidl.co.uk/p/eggs/woodcote-6-organic-eggs/p6730"
url = "https://www.lidl.co.uk/food-offers"

p = set()
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
                    print(n, soup.find("h1", {"class": "attributebox__headline attributebox__headline--h1"}).text.strip())
                    #print(l)
                new_url = "https://www.lidl.co.uk" + l

                p.add(l)
                crawl(new_url, n+1)


crawl(url, 0)






#headings = soup.find_all("h1", {"class": "attributebox__headline attributebox__headline--h1"})
#price = soup.find("span", {"class": "pricebox__price"})
#desc = soup.find("article", {"class": "textbody"})
#data = desc.find_all("li")

#print(headings[0].text.strip())
#print(price.text.strip())
#print()

#for i in data:
    #print(i.text)

