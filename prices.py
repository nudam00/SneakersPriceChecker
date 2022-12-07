from stockx import Stockx
# Gets prices from each site


class Prices:

    def __init__(self, driver, sizes_list, sku, gbp, eur, usd, dni_stockx, dni_alias, price_alias):
        self.driver = driver
        self.size_stockx = sizes_list[0]
        self.size_restocks = sizes_list[1]
        self.sku = sku
        self.gbp = gbp
        self.eur = eur
        self.usd = usd
        self.dni_stockx = dni_stockx
        self.dni_alias = dni_alias
        self.price_alias = price_alias

    def stockx(self):
        stockx = Stockx(self.driver,  self.size_stockx, self.sku)
        try:
            item_name, price, driver = stockx.item_info()
            if self.dni_stockx == 'NIE' or self.dni_stockx == 'MASAKRA':
                price = price-1
            price_pln = (price-(price*0.03)-(price*0.085))*self.gbp
            a = price_pln % 10
            price_pln = price_pln-a
            return [item_name, price, price_pln, driver]
        except TypeError as e:
            print(e)
            return ['None', 'None', 'None']

    def alias(self):
        if self.dni_alias == 'NIE' or self.dni_alias == 'MASAKRA':
            self.price_alias = self.price_alias-1
        price_pln = (self.price_alias -
                     (self.price_alias*0.095)-12)*self.usd*0.971
        a = price_pln % 10
        price_pln = price_pln-a
        return price_pln

    def bestPrice(self, p_stockx, p_alias):
        if self.dni_stockx == 'MASAKRA' and self.dni_alias == 'MASAKRA':
            return ['Stockx/Alias', min(p_stockx, p_alias)]
        elif p_stockx > p_alias:
            if self.dni_stockx == 'MASAKRA':
                return ['Stockx/Alias', p_alias]
            else:
                return ['Stockx', p_stockx]
        elif p_alias > p_stockx:
            if self.dni_alias == 'MASAKRA':
                return ['Stockx/Alias', p_stockx]
            else:
                return ['Alias', p_alias]
        elif p_alias == p_stockx:
            return ['Stockx/Alias', p_alias]
