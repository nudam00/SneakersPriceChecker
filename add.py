import json


def get_settings(setting):
    # Gets setting from settings.json
    settings_file = open("input/settings.json")
    settings = json.load(settings_file)
    return settings[setting]


def best_site(stockx, alias, stockx_days, alias_days):
    # Returns best price and site
    better_site = ""
    better_price = 0
    if stockx > alias:
        if stockx_days == "NIE":
            sites = "StockX/Alias"
            best_price = min(alias, stockx)
            better_site = "StockX/"
            better_price = stockx
        else:
            sites = "StockX"
            best_price = stockx
    if stockx < alias:
        if alias_days == "NIE":
            sites = "StockX/Alias"
            best_price = min(alias, stockx)
            better_site = "Alias/"
            better_price = alias
        else:
            sites = "Alias"
            best_price = alias
    if stockx == alias:
        sites = "StockX/Alias"
        best_price = alias
        better_site = ""
        better_price = 0
    return [sites, better_site, best_price, better_price]


def add_site(
    best_price,
    klekt,
    wethenew,
    hypeboost,
    sneakit,
    net_price,
    margin,
    better_site,
    better_price,
):
    # Checks additional sites
    add_sites = ""
    if klekt >= best_price and (klekt - net_price) / net_price >= margin:
        add_sites = add_sites + "Klekt/"
    if wethenew >= best_price and (wethenew - net_price) / net_price >= margin:
        add_sites = add_sites + "Wethenew/"
    if hypeboost >= best_price and (hypeboost - net_price) / net_price >= margin:
        add_sites = add_sites + "Hypeboost/"
    if sneakit >= best_price and (sneakit - net_price) / net_price >= margin:
        add_sites = add_sites + "Sneakit/"
    if better_price >= best_price and (better_price - net_price) / net_price >= margin:
        add_sites = add_sites + better_site
    return add_sites
