import time


class Wethenew():

    def __init__(self, sku, size, page):
        self.sku = sku
        self.size = size
        self.page = page

    def __get_product(self):
        # Gets product page

        try:
            self.page.goto('https://sell.wethenew.com/listing', timeout=0)
            self.page.wait_for_load_state('load')
            self.page.locator(
                'xpath=//input[@type="search"]').type(self.sku)
            self.page.wait_for_load_state('load')
            time.sleep(2)
            self.page.locator(
                'xpath=//*[@id="__next"]/div/div[1]/div/div/div[3]/div/div/div/div/div/div[2]/button').click()
            self.page.wait_for_load_state('load')
            time.sleep(1)
            return True
        except Exception as e:
            print(e)
            return False

    def get_price(self):
        # Gets price
        bool = False
        while bool == False:
            bool = self.__get_product()

        locator = self.page.locator('xpath=//li[@role="button"]').all()
        for loc in locator:
            if loc.inner_text() == self.size:
                loc.click()
        try:
            price = self.page.locator(
                'xpath=//span[@style="font-weight: 500;"]').inner_text()
            return price.replace('€', '')
        except:
            return 0
