import json


def get_settings(setting):
    # Gets setting from settings.json
    settings_file = open("input/settings.json")
    settings = json.load(settings_file)
    return settings[setting]


def best_site(stockx, alias):
    # Returns best price and site
    if stockx > alias:
        sites = 'StockX'
        best_price = stockx
    if stockx < alias:
        sites = 'Alias'
        best_price = alias
    if stockx == alias:
        sites = 'StockX/Alias'
        best_price = alias
    return [sites, best_price]


def add_site(best_price, klekt, wethenew, hypeboost, net_price, margin):
    # Checks additional sites
    add_sites = ''
    if klekt >= best_price and (klekt-net_price)/net_price >= margin:
        add_sites = add_sites + "Klekt/"
    if wethenew >= best_price and (wethenew-net_price)/net_price >= margin:
        add_sites = add_sites + "Wethenew/"
    if hypeboost >= best_price and (hypeboost-net_price)/net_price >= margin:
        add_sites = add_sites + "Hypeboost/"
    return add_sites
