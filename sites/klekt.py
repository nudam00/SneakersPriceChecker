import json

import cloudscraper

from add import get_settings


class Klekt:
    def __init__(self):
        self.url = "https://www.klekt.com/"
        self.scraper = cloudscraper.create_scraper()
        self.eur = get_settings("eur_rate")
        print("Logged into Klekt account")

    def __get_product(self, sku):
        # Gets product link
        res = str(self.scraper.get(self.url + "brands?search={}".format(sku)).content)
        try:
            return res.split('"slug":"')[1].split('"')[0]
        except:
            print("Klekt: No product found")
            return 0

    def get_price(self, sku, size):
        # Gets price

        try:
            soup = str(
                self.scraper.get(
                    self.url + "product/{}".format(self.__get_product(sku))
                ).content
            )
            variants = soup.split('"variants":[')[1].split(',"variantsNDD":')[0]
            for variant in json.loads('{"variants":[' + variants + "}")["variants"]:
                if variant["facetValues"][0]["name"] == size:
                    return self.__get_price(variant["priceWithTax"] / 100 - 1)
            return 0
        except Exception as e:
            print(e)
            return 0

    def __get_price(self, price):
        # Gets price in PLN after fees
        try:
            price_pln = (price / 1.17 - 5) / 1.21 * self.eur
            return price_pln
        except (TypeError, ValueError):
            return 0
