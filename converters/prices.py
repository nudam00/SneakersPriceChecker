from sites.stockx import Stockx
from sites.alias import Alias
from sites.restocks import Restocks
from sites.klekt import Klekt
from sites.wethenew import Wethenew
from sites.hypeboost import Hypeboost


class Prices:
    # Gets prices from each site

    def __init__(self, driver, sizes_list, sku, eur, usd, alias_token, scraper, stockx_fee, page):
        self.driver = driver
        self.scraper = scraper
        self.size_stockx = sizes_list[0]
        self.size_alias = sizes_list[1]
        self.size_restocks_hypeboost = sizes_list[2]
        self.size_klekt = sizes_list[3]
        self.size_wethenew = sizes_list[4]
        self.sku = sku
        self.eur = eur
        self.usd = usd
        self.alias_token = alias_token
        self.stockx_fee = stockx_fee
        self.page = page

    def stockx(self):
        # Gets price from StockX to PLN
        stockx = Stockx(self.driver,  self.size_stockx, self.sku)
        try:
            item_name, price, driver = stockx.item_info()
            price_pln = (price-(price*0.03)-(price*self.stockx_fee))*self.usd
            # Rounding down to tens (better comparison)
            a = price_pln % 10
            price_pln = price_pln-a
            return [item_name, price_pln, driver]
        except (TypeError, ValueError):
            return ['None', 0, 'None']

    def alias(self):
        # Gets price from Alias to PLN
        alias = Alias(self.sku, self.size_alias,
                      self.alias_token, self.scraper)
        try:
            price = int(alias.get_price())
            price_pln = (price*0.905-12)*self.usd*0.971
            # Rounding down to tens
            a = price_pln % 10
            price_pln = price_pln-a
            return price_pln
        except (TypeError, ValueError):
            return 0

    def restocks(self):
        # Gets price from Restocks to PLN
        restocks = Restocks(self.size_restocks_hypeboost,
                            self.sku, self.scraper)
        try:
            price = int(restocks.get_price())
            price_pln = (price*0.9-20)/1.21*self.eur
            # Rounding down to tens
            a = price_pln % 10
            price_pln = price_pln-a
            return price_pln
        except (TypeError, ValueError):
            return 0

    def klekt(self):
        # Gets price from Klekt to PLN
        klekt = Klekt(self.sku, self.size_klekt, self.scraper)
        try:
            price = int(klekt.get_price())
            price_pln = (price/1.17-5)/1.21*self.eur
            # Rounding down to tens
            a = price_pln % 10
            price_pln = price_pln-a
            return price_pln
        except (TypeError, ValueError):
            return 0

    def wethenew(self):
        # Gets price from WETHENEW to PLN
        wethenew = Wethenew(self.sku, self.size_wethenew, self.page)
        try:
            price = int(wethenew.get_price())
            price_pln = (price/1.2)*self.eur
            # Rounding down to tens
            a = price_pln % 10
            price_pln = price_pln-a
            return price_pln
        except (TypeError, ValueError):
            return 0

    def hypeboost(self):
        # Gets price from Restocks to PLN
        hypeboost = Hypeboost(self.size_restocks_hypeboost,
                              self.sku, self.scraper)
        try:
            price = int(hypeboost.get_price())
            price_pln = (price*0.93-10)/1.21*self.eur
            # Rounding down to tens
            a = price_pln % 10
            price_pln = price_pln-a
            return price_pln
        except (TypeError, ValueError):
            return 0

    def bestPrice(self, p_stockx, p_alias, p_restocks, p_klekt, p_wethenew, p_hypeboost):
        # Returns best price and site
        additional_sites = ''
        best_price = 0
        if p_stockx > p_alias:
            sites = 'StockX'
            best_price = p_stockx
        elif p_stockx < p_alias:
            sites = 'Alias'
            best_price = p_alias
        else:
            sites = 'StockX/Alias'
            best_price = p_alias
        if p_restocks > best_price:
            additional_sites += 'Restocks/'
        if p_klekt > best_price:
            additional_sites += 'Klekt/'
        if p_wethenew > best_price:
            additional_sites += 'Wethenew/'
        if p_hypeboost > best_price:
            additional_sites += 'Hypeboost/'
        return [sites, additional_sites, best_price]
