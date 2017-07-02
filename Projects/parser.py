import requests
import json
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 YaBrowser/17.6.0.1633 Yowser/2.5 Safari/537.36'}

def parse(url, type):
    desc = {}
    desc['Тип объявления'] = type

    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, "html.parser")

    authorName = soup.find("div", {"class": "offer-card__author-name ellipsis"})
    desc["Контактное лицо"] = ' '.join(authorName)

    if authorName is None:
        block = soup.find("p")
        desc["Error"] = ' '.join(block.get_text())
        print(block.get_text())
        exit()

    header = soup.find("h1", {"class": "offer-card__header-text"})
    desc['Название'] = ' '.join(header)

    authorNote = soup.find("div", {"class": "offer-card__author-note"})
    desc["Кем размещено объявление"] = ' '.join(authorNote)

    price = soup.find("h3", {"class": "offer-price offer-card__price offer-card__price"})
    desc['Цена'] = ' '.join(price.get_text())

    priceDetail = soup.find("span", {"class": "offer-card__price-detail"})
    desc['Цена за метр квадратный'] = ' '.join(priceDetail.get_text())

    address = soup.find("h2", {"class": "offer-card__address ellipsis"})
    desc["Адрес"] = ' '.join(address)

    descText = soup.find("div", {"class": "offer-card__desc-text"})
    desc["Описание от продавца"] = ' '.join(descText)

    dates = soup.find("div", {"class": "offer-card__dates"})
    desc['Дата публикации и обновления объявления'] = ' '.join(dates)
# -------------------------------------------------------------------------------------------------------
    #featuresGroup = soup.findAll("div", {"class": "offer-card__featuresGroup"})
# featureValue = soup.find("div", {"class": "offer-card__feature-value"})
# featureName = soup.find("div", {"class": "offer-card__feature-name"})
    name = soup.findAll("div", {"class": "offer-card__feature-name"})
    value = soup.findAll("div", {"class": "offer-card__feature-value"})
    for i in name:
        for e in value:
            print (e)
            featureName = i
            featureValue = e
            desc[' '.join(featureName)] = ' '.join(featureValue)
            del value[0]
            break


#----------------------------------
    #for i in items:
    #    featureValue = soup.find("div", {"class": "offer-card__feature-value"})
    #    featureName = soup.find("div", {"class": "offer-card__feature-name"})
    #    desc[' '.join(featureName)] = ' '.join(featureValue)
    #    print (i)
#-----------------------------------
        #featValue = soup.findNext("div", {"class": "offer-card__feature-value"})
        #featName = soup.findNext("div", {"class": "offer-card__feature-name"})
        #desc[' '.join(featName)] = ' '.join(featValue)

# -------------------------------------------------------------------------------------------------------
    return desc


if __name__ == '__main__':
    descArr = []
    #exampleURL = "https://realty.yandex.ru/offer/477931658444815873/?newFlat=NO&rgid=547386&type=SELL&category=APARTMENT&sort=RELEVANCE&maxCoordinates=500&showUniquePoints=NO&pageSize=20&minTrust=NORMAL&offerIds=477931658444815873&offerIds=6865655688004899584&offerIds=7192645531040857600&offerIds=5305696740553548033&offerIds=1435299278918978816&offerIds=6293751213535284993&offerIds=4964016505597977857&offerIds=5482878738409381632&offerIds=7940765583983276544&offerIds=1129099722904792576&offerIds=5957083327146185217&offerIds=1124568064721008897&offerIds=4649203119936722432&offerIds=7771959763604938496&offerIds=53382771855160832&offerIds=8745989294922496513&offerIds=8412153098044414208&offerIds=3699092668289653761&offerIds=5679441876551673344&offerIds=4388909&initialPage=0"
    #exampleURL = "https://realty.yandex.ru/volgograd/kupit/kvartira/?newFlat=NO&offerId=7771959763604938496"
    exampleURL = "https://aveeell.github.io/page/"
    type = "Продажа"
    descArr.append(parse(exampleURL, type))
    with open('data.json', 'w', encoding='utf-8') as file:
        json.dump(descArr, file, indent=2, ensure_ascii=False)
# print (soup.prettify()) #Вывод всего дерева
