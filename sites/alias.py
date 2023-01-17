import time
import json


class Alias:

    def __init__(self, sku, size, access, scraper):
        self.url = 'https://sell-api.goat.com/api/v1/analytics/variants/availability'
        self.headers = {
            'Accept': 'application/json',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'pl-PL,pl;q=0.9',
            'User-Agent': 'alias/1.20.1 (iPhone; iOS 16.2; Scale/3.00) Locale/en',
            'x-emb-id': '2389040D96C04834A761C65276AC5564',
            'x-emb-st': str(int(time.time() * 1000)),
            'X-PX-AUTHORIZATION': '3',
            'X-PX-ORIGINAL-TOKEN': '3:87ec12c5b4c34832b42e88735f4da9949538cc013cb7ac2c48d8504371518d81:tT/X5LIfW0h1Ymfegj0v4hZx9Oj13sLWXGbw2+PCtg96IiaUfvn0SG5e/GH+QJPIphQY4u6NziXV+nQypGVLhQ==:1000:f9OqYPvRS2ATdeQYm+cskkymJJlSpyDHB++F566kPebKaJwCf2Y4nxse8wunIYMPytrJCPEOm6dZ8rD19SE/JpJH5cWswIgF7i2DQvMEyP+hVIDae1eUTuZViSvGiPlf2hjvkc8kAUbVDx4I72mqHCx6jzH1+F/2qsnWjdxL5lu7s/b+sdA035/eOeXBihKOcOTT08GYQ1EAkgqiFTMQPg==',
            'Connection': 'keep-alive',
            'Host': 'sell-api.goat.com',
            'Authorization': 'Bearer {}'.format(access)
        }
        self.scraper = scraper
        self.sku = sku
        self.size = size

    def __get_product(self):
        # Gets product id
        url = "https://2fwotdvm2o-dsn.algolia.net/1/indexes/product_variants_v2?analyticsTags=%5B%22platform%3Aios%22%2C%22channel%3Aalias%22%5D&distinct=1&facetingAfterDistinct=1&facets=%5B%22product_category%22%5D&filters=%28product_category%3Aclothing%20OR%20product_category%3Ashoes%20OR%20product_category%3Aaccessories%20OR%20product_category%3Abags%29&page=0&query={}".format(
            self.sku)
        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'br;q=1.0, gzip;q=0.9, deflate;q=0.8',
            'Accept-Language': 'pl-PL;q=1.0, en-PL;q=0.9',
            'User-Agent': 'alias/1.20.1 (com.goat.OneSell.ios; build:763; iOS 16.2.0) Alamofire/5.6.2',
            'x-emb-id': '2389040D96C04834A761C65276AC5564',
            'x-emb-st': str(int(time.time() * 1000)),
            'X-Algolia-API-Key': '838ecd564b6aedc176ff73b67087ff43',
            'X-Algolia-Application-Id': '2FWOTDVM2O',
            'Connection': 'keep-alive',
            'Host': '2fwotdvm2o-dsn.algolia.net'
        }
        r = self.scraper.get(headers=headers, url=url)
        try:
            return str([x['slug'] for x in json.loads(r.text)['hits']][0])
        except Exception as e:
            print(e)
            return False

    def get_price(self):
        # Gets price
        product = self.__get_product()
        if product == False:
            return 0
        data = {"variant": {"id": product, "size": self.size, "productCondition": '1',
                            "packagingCondition": '1', "consigned": 'false', "regionId": "2"}}
        r = self.scraper.post(data=json.dumps(data), headers=self.headers,
                              url=self.url)
        try:
            return json.loads(r.text)['lowest_price_cents'][:-2]
        except:
            return json.loads(r.text)['high_demand_price_cents'][:-2]
