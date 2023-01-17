import os
from openpyxl import Workbook
from converters.prices import Prices
import pandas as pd
from converters.size_converter import Size
from add import get_driver, get_exchange, get_scraper
import json


def get_settings(setting):
    # Gets settings from settings.json
    settings_file = open("input/settings.json")
    settings = json.load(settings_file)
    return settings[setting]


def shoes(eur, usd, name, driv, token, scraper, stockx_fee):
    # Gets all needed data from sites
    df = pd.DataFrame(columns=['Product_name', 'SKU', 'Size', 'StockX_payout',
                      'Alias_payout', 'Best_site', 'Best_price', 'Additional_sites'])
    excel = pd.read_excel('input/stock.xlsx', sheet_name=name)

    new_row = {'Product_name': '', 'SKU': '', 'Size': '', 'StockX_payout': '',
               'Alias_payout': '', 'Best_site': '', 'Best_price': '', 'Additional_sites': ''}

    # Based on each row in excel sheet (stock.xlsx)
    for index, row in excel.iterrows():
        if '.0' in str(row['size']):
            size = str(row['size']).replace('.0', '')
        else:
            size = str(row['size'])
        sku = row['sku']

        # If same shoe as before then get saved data from earlier iteration
        if size == new_row['Size'] and sku == new_row['SKU']:
            pass
        else:
            converter = Size(size, sku)
            sizes_list = converter.sizes()
            prices = Prices(driver=driv, sizes_list=sizes_list, sku=sku, eur=eur,
                            usd=usd, alias_token=token, scraper=scraper, stockx_fee=stockx_fee)

            # Gets Stockx price
            item_name, price_stockx_pln, driver = prices.stockx()
            driv = driver
            # Gets Alias price
            price_alias_pln = prices.alias()
            # Gets Restocks pirce
            price_restocks_pln = prices.restocks()
            # Gets Klekt pirce
            price_klekt_pln = prices.klekt()

            # Best price and site
            site, additional_sites, best_price = prices.bestPrice(
                price_stockx_pln, price_alias_pln, price_restocks_pln, price_klekt_pln)

            new_row = {'Product_name': item_name, 'SKU': sku, 'Size': str(row['size']), 'StockX_payout': str(price_stockx_pln).replace('.', ','), 'Alias_payout': str(
                price_alias_pln).replace('.', ','), 'Best_site': site, 'Best_price': str(best_price).replace('.0', ',0'), 'Additional_sites': additional_sites}

        # Adds row
        df = df.append(new_row, ignore_index=True)
        print('\n'+item_name)
        print(sku)
        print(row['size'])
        print({'StockX: ': price_stockx_pln, 'Alias': price_alias_pln, 'Restocks': price_restocks_pln,
              'Klekt': price_klekt_pln, 'Best_site': site, 'Additional_sites': additional_sites})

    return [df, driver]


if __name__ == "__main__":
    print('stock.xlsx:\n'
          '1. Write sku\n'
          "2. Write sizes into that format:\n"
          "Men - e.g. 9/9.5\n"
          "Women - e.g. 9W/9.5W\n"
          "Gs - e.g. 6Y/6.5Y\n"
          'Td - e.g. 2C\n'
          '\n'
          'Write anything when you would like to start\n')
    input()

    # Preparing
    alias_token, scraper = get_scraper(get_settings(
        'alias_username'), get_settings('alias_password'))
    eur, usd = get_exchange()
    driver = get_driver()
    stockx_fee = get_settings('stockx_fee')
    try:
        os.remove("output/prices.xlsx")
    except FileNotFoundError:
        pass
    wb = Workbook()
    wb.save(filename='output/prices.xlsx')
    sheets = pd.ExcelFile('input/stock.xlsx').sheet_names

    # Based on each sheet in excel file
    for i in range(len(pd.ExcelFile('input/stock.xlsx').sheet_names)):
        stock, driver = shoes(eur, usd, i, driver,
                              alias_token, scraper, stockx_fee)
        with pd.ExcelWriter('output/prices.xlsx', engine='openpyxl', mode='a') as writer:
            stock.to_excel(writer, sheet_name=sheets[i])
