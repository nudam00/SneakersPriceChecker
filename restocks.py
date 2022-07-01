import datetime
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


class Restocks:

    def __init__(self, driver, size, sku):
        self.size = size
        self.sku = sku
        self.driver = driver

    def region(self):
        # Chooses country
        self.driver.get("https://restocks.net/shop/?q={}".format(self.sku))

        while True:
            try:
                WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((
                    By.ID, 'save__first__localization__button')))
                select = Select(self.driver.find_element("id",
                                                         'change_first_country'))
                select.select_by_visible_text('The Netherlands')
                select.select_by_value('NL')
                self.driver.find_element("id",
                                         'save__first__localization__button').click()
                break
            except Exception:
                print('{}:Sth is wrong, check that, repair and write sth (or restart)'.format(
                    datetime.datetime.now()))
                input()

    def product_link(self):
        # Gets product link
        self.driver.get("https://restocks.net/shop/?q={}".format(self.sku))

        while True:
            try:
                WebDriverWait(self.driver, 15).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'product-item')))
                product_link = self.driver.find_element("class name",
                                                        'product-item').get_attribute('href')
                return product_link
            except Exception:
                print('{}:Nothing for sale'.format(datetime.datetime.now()))

    def item_info(self):
        # Gets item price
        product_link = self.product_link()

        time.sleep(1)
        self.driver.get(product_link)
        WebDriverWait(self.driver, 15).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@class="select__size__list"]')))
        sizes = self.driver.find_element("xpath",
                                         '//*[@class="select__size__list"]')

        for s in range(1, 25):
            try:
                # Chooses appropriate size
                if sizes.find_element("xpath", '//*[@class="select__size__list"]/li[{}]/span[1]'.format(s)).\
                        get_attribute("innerText") == self.size:
                    price = float(sizes.find_element("xpath", '//*[@class="select__size__list"]/li[{}]/span[3]/span[1]'.
                                                              format(s)).get_attribute("innerText").replace('€ ', ''))
                    return price
            except Exception:
                print('{}:Nothing for sale'.format(datetime.datetime.now()))
