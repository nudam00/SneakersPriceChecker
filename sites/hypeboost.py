import cloudscraper
from bs4 import BeautifulSoup
from lxml import etree

from add import get_settings


class Hypeboost:
    def __init__(self):
        self.url = "https://hypeboost.com/search"
        self.headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7,fa;q=0.6",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
        }
        self.scraper = cloudscraper.create_scraper()
        self.eur = get_settings("eur_rate")
        print("Logged into Hypeboost account")

    def __get_product(self, sku):
        # Gets product link
        soup = BeautifulSoup(
            self.scraper.get(
                headers=self.headers, url=self.url + "/shop?keyword={}".format(sku)
            ).text,
            features="lxml",
        )
        try:
            if soup.find("span").text != sku:
                print("Hypeboost: No product found")
                return False
            return soup.find("a")["href"]
        except:
            return False

    def get_price(self, sku, size):
        # Gets sizes
        product = self.__get_product(sku)
        if product == False:
            return 0

        soup = BeautifulSoup(
            self.scraper.get(headers=self.headers, url=product).text, features="lxml"
        )
        dom = etree.HTML(str(soup))

        for i in range(1, 25):
            try:
                s = dom.xpath(
                    '//*[@id="page-product"]/div[1]/div[1]/div[2]/div/div[1]/div/div[2]/div/div[{}]/div[1]'.format(
                        i
                    )
                )[0].text
                if s == size:
                    return self.__get_price(
                        int(
                            dom.xpath(
                                '//*[@id="page-product"]/div[1]/div[1]/div[2]/div/div[1]/div/div[2]/div/div[{}]/div[2]/span'.format(
                                    i
                                )
                            )[0].text.replace(" €", "")
                        )
                        - 1
                    )
            except:
                pass
        return 0

    def __get_price(self, price):
        # Gets price in PLN after fees
        try:
            price_pln = (price * 0.915 - 15) / 1.21 * self.eur
            return price_pln
        except (TypeError, ValueError):
            return 0
