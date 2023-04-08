import json
from add import get_settings
import cloudscraper


class Sneakit:

    def __init__(self):
        self.url = 'https://sneakit.com/search/product'
        self.scraper = cloudscraper.create_scraper()
        self.eur = get_settings('eur_rate')
        print("Logged into Klekt account")
        self.headers = {'Accept': 'application/json',
                        'Accept-Encoding': 'gzip, deflate',
                        'Accept-Language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7,fa;q=0.6',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
                        }

    def __get_product(self, sku):
        # Gets product link
        try:
            r = self.scraper.get(headers=self.headers,
                                 url=self.url+'s/'+sku).text
            if str([x['sku'] for x in json.loads(r)['data']][0]) != sku:
                print('Sneakit: No product found')
                return None
            return str([x['id'] for x in json.loads(r)['data']][0])
        except:
            print('Sneakit: No product found')
            return None

    def get_price(self, sku, size):
        # Gets price
        id = self.__get_product(sku)
        if id == None:
            return 0

        try:
            r = self.scraper.get(headers=self.headers,
                                 url=self.url+'/'+id).text
            for x in json.loads(r)['sizesPrices']:
                if str(x['size']) == size:
                    return self.__get_price(float(x['price'])-1)
        except:
            return 0

    def __get_price(self, price):
        # Gets price in PLN after fees
        try:
            price_pln = (price/1.2)*self.eur
            return price_pln
        except (TypeError, ValueError):
            return 0
