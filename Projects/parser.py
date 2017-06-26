import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 YaBrowser/17.6.0.1633 Yowser/2.5 Safari/537.36'}
URL = "https://realty.yandex.ru/offer/477931658444815873/?newFlat=NO&rgid=547386&type=SELL&category=APARTMENT&sort=RELEVANCE&maxCoordinates=500&showUniquePoints=NO&pageSize=20&minTrust=NORMAL&offerIds=477931658444815873&offerIds=6865655688004899584&offerIds=7192645531040857600&offerIds=5305696740553548033&offerIds=1435299278918978816&offerIds=6293751213535284993&offerIds=4964016505597977857&offerIds=5482878738409381632&offerIds=7940765583983276544&offerIds=1129099722904792576&offerIds=5957083327146185217&offerIds=1124568064721008897&offerIds=4649203119936722432&offerIds=7771959763604938496&offerIds=53382771855160832&offerIds=8745989294922496513&offerIds=8412153098044414208&offerIds=3699092668289653761&offerIds=5679441876551673344&offerIds=4388909&initialPage=0"
page = requests.get(URL, headers=headers)
pageContent = page.content
soup = BeautifulSoup(pageContent, "html.parser")
author = soup.find_all("div", {"class": "content"})


print(author)
#print (soup.prettify()) #Вывод всего дерева