from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from add import captcha
from selenium.common.exceptions import StaleElementReferenceException
import time


class Stockx:

    def __init__(self, driver, size, sku):
        self.driver = driver
        self.size = size
        self.sku = sku

    def product_link(self):
        # Gets listing creation link
        while True:
            try:
                self.driver.get("https://pro.stockx.com/listings/create")
                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(
                    (By.XPATH, '//input[@data-testid="search-box"]')))
                time.sleep(1)
                self.driver.find_element(
                    By.XPATH, '//input[@data-testid="search-box"]').send_keys(self.sku)
                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="product-search-results"]/div[1]/div/button')))
                self.driver.find_element(
                    By.XPATH, '//*[@id="product-search-results"]/div[1]/div/button').click()
                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="main-container"]/div[1]/div[2]/div[3]/div/button[1]')))
                break
            except:
                # When PerimeterX is detected
                self.driver.close()
                self.driver = captcha()

    def choose_size(self):
        # Clicks size
        self.product_link()
        while True:
            try:
                for i in range(1, 42):
                    size = self.driver.find_element(
                        By.XPATH, '//*[@id="main-container"]/div[1]/div[2]/div[3]/div/button[{}]/div'.format(i)).text
                    if size == self.size:
                        self.driver.find_element(
                            By.XPATH, '//*[@id="main-container"]/div[1]/div[2]/div[3]/div/button[{}]'.format(i)).click()
                        break
                break
            except StaleElementReferenceException:
                print("Click pop ups...")
                input()

    def item_info(self):
        # Gets product name, sku and price
        self.choose_size()

        # Lowest ask
        WebDriverWait(self.driver, 2).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="main-container"]/div[1]/div[2]/div[5]/div[2]/div[3]/div/span/div/div/input')))
        p = self.driver.find_element(
            By.XPATH, '//*[@id="main-container"]/div[1]/div[2]/div[5]/div[2]/div[3]/div/span/div/div/input').get_attribute("value")
        price = float(p)+1

        # Item name
        item_name1 = self.driver.find_element(
            By.XPATH, '//*[@id="main-container"]/div[1]/div[2]/div[1]/div/div/div[1]').text
        item_name2 = self.driver.find_element(
            By.XPATH, '//*[@id="main-container"]/div[1]/div[2]/div[1]/div/div/div[2]').text

        return [item_name1+" "+item_name2, price, self.driver]
