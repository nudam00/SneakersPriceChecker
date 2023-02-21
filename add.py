from forex_python.converter import CurrencyRates
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
