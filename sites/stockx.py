import time

from add import get_settings


class StockX:
    def __init__(self, username, password, p, stockx_fee):
        self.usd = get_settings("usd_rate")
        self.eur = get_settings("eur_rate")
        self.p = p
        self.stockx_fee = stockx_fee
        while self.__log_in(username, password) == False:
            self.__log_in(username, password)

    def __log_in(self, username, password):
        # Logs into StockX account

        self.p.goto("https://pro.stockx.com/", timeout=0)
        self.p.wait_for_load_state("load")
        time.sleep(3)
        try:
            # Login button
            self.p.locator(
                'xpath=//*[@id="main-container"]/div[1]/section[1]/div[1]/button'
            ).click()
            self.p.wait_for_load_state("load")
            time.sleep(5)

            # Switch from sign up to sign in
            self.p.locator('xpath=//button[@class="toggle-option"]').click()
            time.sleep(5)

            # Log in
            self.p.locator('xpath=//input[@id="email-login"]').type(username)
            time.sleep(1)
            self.p.locator('xpath=//input[@id="password-login"]').type(password)
            time.sleep(3)
            self.p.locator('xpath=//button[@id="btn-login"]').click()
            self.p.wait_for_load_state("load")
            time.sleep(6)
            print("Logged into StockX account")
            return True
        except:
            print(
                "Something had happened, check if Perimeterx popped up and type anything"
            )
            input()
            return False

    def __product_link(self, sku):
        # Gets listing creation link
        while True:
            try:
                self.p.goto("https://pro.stockx.com/listings/create")
                time.sleep(2)
                self.p.locator('xpath=//input[@data-testid="search-box"]').type(sku)
                time.sleep(1)
                self.p.locator(
                    'xpath=//*[@id="product-search-results"]/div[1]/div'
                ).click()

                self.p.wait_for_load_state("load")
                time.sleep(3)
                break
            except:
                print(
                    "Something had happened, check if Perimeterx popped up and type anything"
                )
                input()

    def __choose_size(self, sku, size):
        # Clicks size
        self.__product_link(sku)

        sizes = self.p.locator(
            'xpath=//*[@id="main-container"]/div[1]/div[2]/div[3]/div/button'
        ).all()

        for i in range(1, len(sizes) + 1):
            while True:
                try:
                    s = self.p.locator(
                        'xpath=//*[@id="main-container"]/div[1]/div[2]/div[3]/div/button[{}]/div'.format(
                            i
                        )
                    ).inner_text()
                    if size == s:
                        self.p.locator(
                            'xpath=//*[@id="main-container"]/div[1]/div[2]/div[3]/div/button[{}]'.format(
                                i
                            )
                        ).click()
                        return True
                    break
                except:
                    pass

        return False

    def get_price(self, sku, size):
        # Gets product name, sku and price
        item_name1 = ""
        item_name2 = ""
        while True:
            if self.__choose_size(sku, size) != False:
                try:
                    item_name1 = self.p.locator(
                        'xpath=//*[@id="main-container"]/div[1]/div[2]/div[1]/div/div[1]/div[1]'
                    ).inner_text()
                    item_name2 = self.p.locator(
                        'xpath=//*[@id="main-container"]/div[1]/div[2]/div[1]/div/div[1]/div[2]'
                    ).inner_text()
                    price = self.__get_PLN(
                        float(
                            self.p.locator(
                                'xpath=//*[@id="main-container"]/div[1]/div[2]/div[5]/div[2]/div[4]/div/span[1]'
                            )
                            .inner_text()
                            .replace("$", "")
                        )
                    )
                    print(price)
                except:
                    try:
                        price = self.__get_PLN(
                            float(
                                self.p.locator(
                                    'xpath=//*[@id="main-container"]/div[1]/div[2]/div[5]/div[2]/div[5]/div/span'
                                )
                                .inner_text()
                                .replace("$", "")
                            )
                        )
                        print(price)
                    except:
                        try:
                            price = self.__get_PLN(
                                float(
                                    self.p.locator(
                                        'xpath=//*[@id="main-container"]/div[1]/div[2]/div[5]/div[2]/div[3]/div/span/div/div/input'
                                    ).get_attribute("value")
                                )
                            )
                            print(price)
                        except:
                            return [None, None]

                return [item_name1 + " " + item_name2, price]
            else:
                continue

    def __get_PLN(self, price):
        # Gets price in PLN after fees

        try:
            if (price * self.stockx_fee * self.usd) > (5 * self.eur):
                price_pln = (
                    price - (price * 0.03) - (price * self.stockx_fee)
                ) * self.usd
            else:
                price_pln = ((price - (price * 0.03)) * self.usd) - (5 * self.eur)
            price_pln = price_pln - (2.73 * self.usd)
            return price_pln
        except (TypeError, ValueError):
            return False
