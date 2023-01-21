import json
from bs4 import BeautifulSoup


class Restocks:

    def __init__(self, size, sku, scraper):
        self.size = size
        self.sku = sku
        self.scraper = scraper
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'pl,en-US;q=0.7,en;q=0.3',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0',
            'Referer': 'https://restocks.net/en',
            'Origin': 'https://restocks.net',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'Connection': 'keep-alive',
            'Host': 'restocks.net',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

    def __get_product(self):
        # Gets product page
        url = 'https://restocks.net/en/shop/search?q={}&page=1&filters[0][range][price][gte]=1'.format(
            self.sku)
        r = self.scraper.get(url=url, headers=self.headers)
        try:
            return [x['slug'] for x in json.loads(r.text)['data']][0]
        except IndexError:
            print('Restocks: No product found')
            return False

    def get_price(self):
        # Gets price
        url = self.__get_product()
        if url == False:
            return 0

        r = self.scraper.get(url=url, headers=self.headers)
        soup = BeautifulSoup(r.text, features="lxml")
        sizes = soup.findAll('li', {'data-type': 'all'})
        for size in sizes:
            if size.find('span', {'class': 'text'}).get_text() == self.size:
                try:
                    return size.find('span', {'class': ''}).get_text().replace('€ ', '')
                except:
                    return 0
        return 0
