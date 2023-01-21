from bs4 import BeautifulSoup
from lxml import etree


class Hypeboost:

    def __init__(self, size, sku, scraper):
        self.size = size
        self.sku = sku
        self.scraper = scraper
        self.url = 'https://hypeboost.com/search/shop?keyword={}'.format(
            self.sku)
        self.headers = {'Accept': '*/*',
                        'Accept-Encoding': 'gzip, deflate',
                        'Accept-Language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7,fa;q=0.6',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
                        }

    def __get_product(self):
        soup = BeautifulSoup(self.scraper.get(
            headers=self.headers, url=self.url).text, features="lxml")
        try:
            return soup.find('a')['href']
        except:
            return False

    def get_price(self):
        url = self.__get_product()
        try:
            soup = BeautifulSoup(self.scraper.get(
                headers=self.headers, url=url).text, features="lxml")
            dom = etree.HTML(str(soup))
            for i in range(1, 25):
                size = dom.xpath(
                    '//*[@id="page-product"]/div[1]/div[1]/div[2]/div/div[1]/div/div[2]/div/div[{}]/div[1]'.format(i))[0].text
                if size == self.size:
                    price = dom.xpath(
                        '//*[@id="page-product"]/div[1]/div[1]/div[2]/div/div[1]/div/div[2]/div/div[{}]/div[2]/span'.format(i))[0].text.replace(' €', '')
                    return price
        except:
            return 0
