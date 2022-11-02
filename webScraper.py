from bs4 import BeautifulSoup
from urllib.request import urlopen

url = "https://www.lidl.co.uk/p/eggs/woodcote-6-organic-eggs/p6730"
page = urlopen(url)
html = page.read().decode("utf-8")
soup = BeautifulSoup(html, "html.parser")

headings = soup.find_all("h1", {"class": "attributebox__headline attributebox__headline--h1"})
price = soup.find("span", {"class": "pricebox__price"})
desc = soup.find("article", {"class": "textbody"})
data = desc.find_all("li")

print(headings[0].text.strip())
print(price.text.strip())
print()

for i in data:
    print(i.text)

