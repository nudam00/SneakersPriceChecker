import time
from add import get_settings


class Wethenew():

    def __init__(self, username, password, p):
        self.eur = get_settings('eur_rate')
        self.p = p
        while self.__log_in(username, password) == False:
            self.__log_in(username, password)

    def __log_in(self, username, password):
        # Logs into wethenew account
        self.p.goto('https://sell.wethenew.com/login', timeout=0)
        self.p.wait_for_load_state('load')
        time.sleep(3)
        try:
            self.p.locator(
                'xpath=//button[@id="didomi-notice-agree-button"]').first.click(force=True, click_count=2)
            time.sleep(2)
        except:
            pass
        try:
            self.p.locator(
                'xpath=//input[@type="email"]').type(username)
            time.sleep(1)
            self.p.locator(
                'xpath=//input[@type="password"]').type(password)
            time.sleep(1)
            self.p.locator('xpath=//button[@type="submit"]').click()
            time.sleep(2)
        except:
            pass
        print("Logged into Wethenew account")
        return True

    def __get_product(self, sku):
        # Gets product page

        try:
            self.p.goto('https://sell.wethenew.com/listing', timeout=0)
            self.p.wait_for_load_state('load')
            self.p.locator(
                'xpath=//input[@type="search"]').type(sku)
            self.p.wait_for_load_state('load')
            time.sleep(2)
            self.p.locator(
                'xpath=//*[@id="__next"]/div/div[1]/div/div/div[3]/div/div/div/div/div/div[2]/button').click()
            self.p.wait_for_load_state('load')
            time.sleep(2)
            return True
        except:
            print('Wethenew: No product found')
            return None

    def get_price(self, sku, size):
        # Gets price

        # Unfortunately sometimes there are more than one product page so then it won't work
        url = self.__get_product(sku)
        if url == None:
            return 0

        try:
            try:
                self.p.locator(
                    'xpath=//li[@role="button"]', has_text=size).click()
            except:
                self.p.locator(
                    'xpath=//li[@role="button"]', has_text="WTB\n{}".format(size)).click()
            time.sleep(1)
            print(self.p.locator(
                'xpath=//span[@style="font-weight: 500;"]').inner_text())
            price = self.__get_PLN(float(self.p.locator(
                'xpath=//span[@style="font-weight: 500;"]').inner_text().replace('€', ''))-1)
            print(price)
            return price
        except:
            return 0

    def __get_PLN(self, price):
        # Gets price in PLN after fees

        try:
            price_pln = (price/1.2)*self.eur
            return price_pln
        except (TypeError, ValueError):
            return 0
