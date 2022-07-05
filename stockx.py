import datetime
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def captcha():
    print("{}: Solve captcha".format(datetime.datetime.now()))
    time.sleep(5)


class Stockx:

    def __init__(self, driver, size, sku, email, password):
        self.driver = driver
        self.size = size
        self.sku = sku
        self.email = email
        self.password = password

    def region(self):
        # Chooses region
        self.driver.get("https://stockx.com/")
        print("Choose region and log in manually (PerimeterX is blocking horribly) and type anything...")
        input()
        # time.sleep(5)

        # while True:
        #     try:
        #         WebDriverWait(self.driver, 10).until(
        #             EC.presence_of_element_located((By.XPATH, '//*[@role="dialog"]/footer/button')))
        #         self.driver.find_element(
        #             "xpath", '/html/body/div[6]/div[4]/div/section/footer/button').click()
        #         break
        #     except Exception as e:
        #         try:
        #             WebDriverWait(self.driver, 10).until(
        #                 EC.presence_of_element_located((By.XPATH, '//*[@role="dialog"]/footer/button')))
        #             self.driver.find_element(
        #                 "xpath", '/html/body/div[5]/div[4]/div/section/footer/button').click()
        #             break
        #         except Exception:
        #             captcha()
        #         captcha()
        # time.sleep(4)

        # # Accept cookies
        # self.driver.find_element(
        #     'xpath', '/html/body/div[5]/div[2]/div/div[1]/div/div[2]/div/button[3]').click()
        # self.logging_in()

    # def logging_in(self):
    #     # Logs in

    #     while True:
    #         try:
    #             self.driver.find_element("xpath",
    #                                      '//*[@id="nav-login"]').click()
    #             break
    #         except Exception:
    #             captcha()
    #     self.driver.refresh()

    #     while True:
    #         try:
    #             WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((
    #                 By.XPATH, '//*[@id="email-login"]')))
    #             self.driver.find_element("xpath",
    #                                      '//*[@id="email-login"]').send_keys(self.email)
    #             time.sleep(0.5)
    #             self.driver.find_element("xpath",
    #                                      '//*[@id="password-login"]').send_keys(self.password)
    #             time.sleep(2)
    #             break
    #         except Exception:
    #             captcha()

    def product_link(self):
        # Finds product link
        while True:
            try:
                self.driver.get(
                    "https://stockx.com/search/sneakers?s={}".format(self.sku))
                break
            except Exception:
                continue

        while True:
            try:
                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@data-testid'
                                                                                              '="search-confirmation"]')
                                                                                   ))
                href = self.driver.find_element("xpath",
                                                '//*[@class="css-1dh562i"]')
                return href.find_element("css selector", 'a').get_attribute('href')
            except Exception:
                captcha()

    def item_info(self):
        # Gets product name, sku and price

        self.driver.get(self.product_link())

        while True:
            try:
                self.driver.find_element("xpath", '/html/body/div[1]/div/main/div/section[1]/div[3]/div['
                                                  '2]/div[2]/div[1]/div/button').click()
                break
            except Exception:
                try:
                    self.driver.find_element("xpath",
                                             '/html/body/div[1]/div/main/div/section[1]/div[3]/div[2]/div[2]/div[1]/div/button').click()
                    break
                except Exception:
                    try:
                        self.driver.find_element("xpath", '/html/body/div[1]/div/main/div/section[1]/div['
                                                          '3]/div[2]/div[1]/div[1]/div/button').click()
                        break
                    except Exception:
                        captcha()
        time.sleep(0.5)

        # Scraps price
        for s in range(1, 27):
            try:
                # Chooses appropriate size
                sizes = self.driver.find_element("xpath",
                                                 '//div[@class="css-1o6kz7w"]/button[{}]'.format(s))
                a = sizes.get_attribute('innerHTML').split(
                    'chakra-stat__label css-nszg6y">', 1)[1]
                size = a.split(
                    '</dt><dd class="chakra-stat__number css-1pulpde', 1)[0]

                if size == "US M {}".format(self.size) or size == "US {}".format(self.size):

                    # Clicks size
                    self.driver.find_element("xpath",
                                             '//div[@class="css-1o6kz7w"]/button[{}]'.format(s)).click()

                    # Lowest ask
                    try:
                        price = int(
                            self.driver.find_element("xpath", '//div[2]/div/a[2]/p[@class="chakra-text css-qhbnuv"]'
                                                     ).get_attribute("innerText").replace('Buy for £', ''))
                    except Exception:
                        price = int(self.driver.find_element("xpath", '//div[2]/div[1]/div[2]/div[1]/div/dl/dd['
                                                                      '@class="chakra-stat__number '
                                                                      'css-1brf3jx"]').get_attribute(
                            "innerText").replace('£', ''))

                    # Scraps item names
                    item_name = self.driver.find_element("xpath", '//*[@class="chakra-heading css-1voth73"]'). \
                        get_attribute("innerText")

                    return [item_name, price]
            except Exception as e:
                print(e)
                print('{}:Nothing for sale'.format(datetime.datetime.now()))
