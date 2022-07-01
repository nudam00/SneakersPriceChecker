from restocks import Restocks
from stockx import Stockx
# Gets prices from each site


class Prices:

    def __init__(self, driver, sizes_list, sku, email, password, t, rate_gbp, rate_eur):
        self.driver = driver
        self.sizes_list = sizes_list
        self.sku = sku
        self.email = email
        self.password = password
        self.t = t
        self.rate_gbp = rate_gbp
        self.rate_eur = rate_eur

    def stockx(self):
        st = Stockx(
            self.driver, self.sizes_list[0], self.sku, self.email, self.password)
        if self.t == 0:
            st.region()
        try:
            list_stockx = st.item_info()
            price_stockx = (
                list_stockx[1] - (list_stockx[1] * 0.03) - (list_stockx[1] * 0.075)) * self.rate_gbp
            return [list_stockx[0], list_stockx[1], price_stockx]
        except Exception:
            return ['None', 0, 0]

    def restocks(self):
        rest = Restocks(self.driver, self.sizes_list[2], self.sku)
        if self.t == 0:
            rest.region()
        try:
            price = rest.item_info()
            price_restocks = (price * 0.9 - 10) * self.rate_eur
            return [price, price_restocks]
        except Exception:
            return [0, 0]
