from bs4 import BeautifulSoup
from lxml import etree
import json


class Sneakit:

    def __init__(self, sku, size, scraper):
        self.sku = sku
        self.size = size
        self.scraper = scraper
        self.headers = {'Accept': 'application/json',
                        'Accept-Encoding': 'gzip, deflate',
                        'Accept-Language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7,fa;q=0.6',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
                        }

    def __get_product(self):
        # Gets product link
        url = 'https://sneakit.com/search/products/{}'.format(self.sku)
        try:
            r = self.scraper.get(headers=self.headers, url=url).text
            return str([x['id'] for x in json.loads(r)['data']][0])
        except:
            return 0

    def get_price(self):
        # Gets price
        id = self.__get_product()

        try:
            url = 'https://sneakit.com/product/{}'.format(id)
            r = self.scraper.get(headers=self.headers, url=url).text

            soup = BeautifulSoup(r, features="lxml")
            sizes = json.loads(
                str(soup.find('purchase-size-dropdown')).split("'")[1])
            for size in sizes:
                if str(size['size']) == self.size:
                    return int(size['resellPrice'])
        except:
            return 0
