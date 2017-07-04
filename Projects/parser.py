import requests
import json
#import time
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 YaBrowser/17.6.0.1633 Yowser/2.5 Safari/537.36'}

def proxy(url):
    proxyURL = "https://www.ip-adress.com/proxy-list"
    pageProxy = requests.get(proxyURL)
    soupProxy = BeautifulSoup(pageProxy.text, "html.parser")

    a = soupProxy.findAll("td")
    s = requests.get(url)
    soupProv = BeautifulSoup(s.text, "html.parser")
    prov = soupProv("div", {"class": "offer-card__author-name ellipsis"})
    j=0
    while (j!=200):
        if (j%4==0):
            proxies = a[j].text
            try:
                r = requests.get(url, proxies={'https': proxies})
                if (prov in None):
                    print(proxies)
                    return proxies
            except (requests.exceptions.ConnectionError):
                continue
        j+=1

# ------------------------------------------------------------------
def parse(url, type):
    desc = {}
    desc['Тип объявления'] = type

    page = requests.get(url, headers=headers)#, proxies=proxies)
    soup = BeautifulSoup(page.text, "html.parser")
    authorName = soup.find("div", {"class": "offer-card__author-name ellipsis"})
    if authorName is None:
        block = soup.find("p")
        print("Яндекс заблокировал запросы")
        exit()
    else:
        authorName1 = soup.find("div", {"class": "offer-card__author-name ellipsis"})
        desc["Контактное лицо"] = ' '.join(authorName1)

        header = soup.find("h1", {"class": "offer-card__header-text"})
        print(header)
        desc['Название'] = ' '.join(header)

        authorNote = soup.find("div", {"class": "offer-card__author-note"})
        desc["Кем размещено объявление"] = ' '.join(authorNote)

        price = soup.find("h3", {"class": "offer-price offer-card__price offer-card__price"})
        desc['Цена'] = ' '.join(price.get_text())

        priceDetail = soup.find("span", {"class": "offer-card__price-detail"})
        if (priceDetail is not None):
            desc['Цена за метр квадратный'] = ' '.join(priceDetail.get_text())

        address = soup.find("h2", {"class": "offer-card__address ellipsis"})
        desc["Адрес"] = ' '.join(address)

        descText = soup.find("div", {"class": "offer-card__desc-text"})
        desc["Описание от продавца"] = ' '.join(descText)

        dates = soup.find("div", {"class": "offer-card__dates"})
        desc['Дата публикации и обновления объявления'] = ' '.join(dates)

        name = soup.findAll("div", {"class": "offer-card__feature-name"})
        value = soup.findAll("div", {"class": "offer-card__feature-value"})

        for i in name:
            for e in value:
                featureName = i
                featureValue = e
                desc[' '.join(featureName)] = ' '.join(featureValue)
                del value[0]
                break
            return desc
            # print("parse() завершил работу. Данные в data.json, ПО-ИДЕЕ ДОЛЖНЫ БЫТЬ ")

# ------------------------------------------------------------------
def scanPage(url, type):
    # type = "Продажа"
    # bURL = "https://realty.yandex.ru/"
    pageCont = requests.get(url, headers=headers)
    soup1 = BeautifulSoup(pageCont.text, "html.parser")
    # arrOfLinks =[]
    offerURLs = soup1.findAll("a", {"class": "link link_theme_normal serp-item-action stat__click i-bem"})
    for item in offerURLs:
        href = item.attrs["href"]
        #proxy(href)
        print("Начинаю парсить " + str(href))
        descArr.append(parse(href, type))
        # time.sleep(5)
        # arrOfLinks.append(href)
        # print(arrOfLinks)

        #  if (j == 21):
        #      pageStr = "?newFlat=NO&page="
        #     nextPage = bURL + str(pageStr) + str(i)
        #     print(nextPage)
        #    i += 1

# ------------------------------------------------------------------
if __name__ == '__main__':
    # baseURL = "https://realty.yandex.ru/volgograd/kupit/kvartira/?newFlat=NO"
    baseURL = "https://aveeell.github.io/hrefs/hrefs.html"
    # pageLink = "volgograd/kupit/kvartira/?newFlat=NO"
    descArr = []
    # exampleURL = "https://realty.yandex.ru/offer/477931658444815873/?newFlat=NO&rgid=547386&type=SELL&category=APARTMENT&sort=RELEVANCE&maxCoordinates=500&showUniquePoints=NO&pageSize=20&minTrust=NORMAL&offerIds=477931658444815873&offerIds=6865655688004899584&offerIds=7192645531040857600&offerIds=5305696740553548033&offerIds=1435299278918978816&offerIds=6293751213535284993&offerIds=4964016505597977857&offerIds=5482878738409381632&offerIds=7940765583983276544&offerIds=1129099722904792576&offerIds=5957083327146185217&offerIds=1124568064721008897&offerIds=4649203119936722432&offerIds=7771959763604938496&offerIds=53382771855160832&offerIds=8745989294922496513&offerIds=8412153098044414208&offerIds=3699092668289653761&offerIds=5679441876551673344&offerIds=4388909&initialPage=0"
    # exampleURL = "https://realty.yandex.ru/volgograd/kupit/kvartira/?newFlat=NO&offerId=7771959763604938496"
    # exampleURL = "https://aveeell.github.io/page/"
    type = "Продажа"
    # descArr.append(scanPage(baseURL))
    scanPage(baseURL, type)
    # descArr.append(parse(exampleURL, type))
    with open('data.json', 'w', encoding='utf-8') as file:
        json.dump(descArr, file, indent=2, ensure_ascii=False)
