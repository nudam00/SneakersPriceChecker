from bs4 import BeautifulSoup
from lxml import etree
from add import get_settings
import cloudscraper


class Klekt:

    def __init__(self):
        self.url = 'https://www.klekt.com/'
        self.scraper = cloudscraper.create_scraper()
        self.eur = get_settings('eur_rate')
        print("Logged into Klekt account")

    def __get_product(self, sku):
        # Gets product link
        soup = BeautifulSoup(self.scraper.get(
            self.url+'brands?search={}'.format(sku)).text, features="lxml")
        try:
            return soup.find('a', {'class': 'pod-link'})['href']
        except:
            print('Klekt: No product found')
            return 0

    def get_price(self, sku, size):
        # Gets price
        try:
            soup = BeautifulSoup(self.scraper.get(
                self.url+self.__get_product(sku)).text, features="lxml")
        except:
            return 0
        dom = etree.HTML(str(soup))
        for i in range(1, 25):
            try:
                s = dom.xpath(
                    '//*[@id="__next"]/div/div/div[3]/div/div[3]/div/div[4]/div[2]/div/div[{}]/span[1]/span'.format(i))[0].text
                if s == size:
                    return self.__get_price(int(dom.xpath(
                        '//*[@id="__next"]/div/div/div[3]/div/div[3]/div/div[4]/div[2]/div/div[{}]/span[2]/span'.format(i))[1].text)-1)
            except IndexError:
                return 0

    def __get_price(self, price):
        # Gets price in PLN after fees
        try:
            price_pln = (price/1.17-5)/1.21*self.eur
            return price_pln
        except (TypeError, ValueError):
            return 0
