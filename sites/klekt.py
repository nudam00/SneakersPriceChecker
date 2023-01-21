from bs4 import BeautifulSoup
from lxml import etree


class Klekt:

    def __init__(self, sku, size, scraper):
        self.scraper = scraper
        self.sku = sku
        self.size = size

    def __get_product(self):
        # Gets product page
        soup = BeautifulSoup(self.scraper.get(
            'https://www.klekt.com/brands?search={}'.format(self.sku)).text, features="lxml")
        try:
            return soup.find('a', {'class': 'pod-link'})['href']
        except:
            return False

    def get_price(self):
        # Gets price
        try:
            soup = BeautifulSoup(self.scraper.get(
                'https://www.klekt.com/'+self.__get_product()).text, features="lxml")
        except:
            return 0
        dom = etree.HTML(str(soup))
        for i in range(1, 25):
            try:
                size = dom.xpath(
                    '//*[@id="__next"]/div/div/div[3]/div/div[3]/div/div[4]/div[2]/div/div[{}]/span[1]/span'.format(i))[0].text
                if size == self.size:
                    price = dom.xpath(
                        '//*[@id="__next"]/div/div/div[3]/div/div[3]/div/div[4]/div[2]/div/div[{}]/span[2]/span'.format(i))[1].text
                    return price
            except IndexError:
                return 0
