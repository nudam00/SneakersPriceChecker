from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from add import captcha
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException


class Stockx:

    def __init__(self, driver, size, sku):
        self.driver = driver
        self.size = size
        self.sku = sku

    def product_link(self):
        # Finds product link
        while True:
            try:
                self.driver.get(
                    "https://stockx.com/search/sneakers?s={}".format(self.sku))
                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(
                    (By.XPATH, '//*[@data-testid="search-confirmation"]')))
                href = self.driver.find_element(
                    By.XPATH, '//*[@class="css-pnc6ci"]')
                return href.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
            except (TimeoutException, NoSuchElementException):
                self.driver.close()
                self.driver = captcha()

    def item_info(self):
        # Gets product name, sku and price
        url = self.product_link().replace('https://stockx.com/', '')
        self.driver.get('https://stockx.com/sell/'+url+'?size='+self.size)

        while True:
            try:
                # Lowest ask
                WebDriverWait(self.driver, 2).until(EC.presence_of_element_located(
                    (By.XPATH, '//span[2][@class="css-d5w67v"]')))
                low_high = self.driver.find_element(
                    By.XPATH, '//span[2][@class="css-d5w67v"]')
                price = float(low_high.text.replace('Lowest Ask: £', ''))

                # Item name
                item_name1 = self.driver.find_element(
                    By.XPATH, '//h2[1][@class="chakra-heading css-3lfcke"]').text
                item_name2 = self.driver.find_element(
                    By.XPATH, '//h2[2][@class="chakra-heading css-3lfcke"]').text

                return [item_name1+" "+item_name2, price, self.driver]
            except (TimeoutException, NoSuchElementException, StaleElementReferenceException):
                try:
                    # "Place new ask" button
                    WebDriverWait(self.driver, 2).until(EC.presence_of_element_located(
                        (By.XPATH, '//*[@class="chakra-button css-ajk9oe"]')))
                    self.driver.find_element(
                        By.XPATH, '//*[@class="chakra-button css-ajk9oe"]').click()
                except TimeoutException:
                    try:
                        # "I have this one" button
                        WebDriverWait(self.driver, 2).until(EC.presence_of_element_located(
                            (By.XPATH, '//div[1]/div/button[@class="chakra-button css-e33jku"]')))
                        self.driver.find_element(
                            By.XPATH, '//div[1]/div/button[@class="chakra-button css-e33jku"]').click()
                    except TimeoutException:
                        try:
                            # "I understand" button
                            WebDriverWait(self.driver, 2).until(EC.presence_of_element_located(
                                (By.XPATH, '//*[@class="chakra-button css-vzfjg0"]')))
                            self.driver.find_element(
                                By.XPATH, '//*[@class="chakra-button css-vzfjg0"]').click()
                        except TimeoutException:
                            self.driver.close()
                            self.driver = captcha()
                            return self.item_info()
