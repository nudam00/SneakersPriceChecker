from sites.alias import Alias
from sites.stockx import StockX
from sites.klekt import Klekt
from sites.wethenew import Wethenew
from sites.hypeboost import Hypeboost
from sites.sneakit import Sneakit
from add import get_settings, best_site, add_site
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
import os
from openpyxl import Workbook
import pandas as pd
from converters.size_converter import Size


if __name__ == "__main__":
    print('stock.xlsx:\n'
          '1. Write sku\n'
          "2. Write sizes into format:\n"
          "Men - e.g. 9/9.5\n"
          "Women - e.g. 9W/9.5W\n"
          "Gs - e.g. 6Y/6.5Y\n"
          'Td - e.g. 2C\n'
          '\n'
          'Write anything when you would like to start\n')
    input()

    # Preparing files
    try:
        os.remove("output/prices.xlsx")
    except FileNotFoundError:
        pass
    wb = Workbook()
    wb.save(filename='output/prices.xlsx')
    sheets = pd.ExcelFile('input/stock.xlsx').sheet_names

    with sync_playwright() as p:
        browser = p.firefox.launch(headless=False, slow_mo=300)
        page = browser.new_page()
        stealth_sync(page)

        # Preparing
        alias = Alias(get_settings('alias_username'),
                      get_settings('alias_password'))
        stockx = StockX(get_settings('email'), get_settings(
            'stockx_password'), page, get_settings('stockx_fee'))
        klekt = Klekt()
        wethenew = Wethenew(get_settings('email'), get_settings(
            'wethenew_password'), page)
        hypeboost = Hypeboost()
        sneakit = Sneakit()

        for i in range(len(pd.ExcelFile('input/stock.xlsx').sheet_names)):
            # Creating dataframe
            df = pd.DataFrame(columns=['Product_name', 'SKU', 'Size', 'StockX_payout',
                                       'Alias_payout', 'Best_site', 'Best_price', 'Additional_sites'])
            excel = pd.read_excel('input/stock.xlsx', sheet_name=i)
            new_row = {'Product_name': '', 'SKU': '', 'Size': '', 'StockX_payout': '',
                       'Alias_payout': '', 'Best_site': '', 'Best_price': '', 'Additional_sites': ''}

            for index, row in excel.iterrows():
                # Getting inputs
                if '.0' in str(row['size']):
                    size = str(row['size']).replace('.0', '')
                else:
                    size = str(row['size'])
                sku = row['sku']
                net_price = float(str(row['price_net']).replace(',', '.'))
                stockx_days = row['stockx']
                alias_days = row['alias']

                # If same shoe as before then get data from latest iteration
                if size == new_row['Size'] and sku == new_row['SKU']:
                    pass
                else:
                    sizes_converter = Size(size, sku)
                    alias_price = alias.get_price(sku, sizes_converter.alias())
                    stockx_data = stockx.get_price(
                        sku, sizes_converter.stockx())
                    product_name = stockx_data[0]
                    stockx_price = stockx_data[1]
                    klekt_price = klekt.get_price(sku, sizes_converter.klekt())
                    wethenew_price = wethenew.get_price(
                        sku, sizes_converter.wethenew(product_name.lower()))
                    hypeboost_price = hypeboost.get_price(
                        sku, sizes_converter.hypeboost(product_name.lower()))
                    sneakit_price = sneakit.get_price(
                        sku, sizes_converter.sneakit(product_name.lower()))

                    # Best price
                    site, better_site, best_price, better_price = best_site(
                        stockx_price, alias_price, stockx_days, alias_days)
                    add_sites = add_site(
                        best_price, klekt_price, wethenew_price, hypeboost_price, sneakit_price, net_price, get_settings('margin'), better_site, better_price)

                    try:
                        best_price = str(best_price).replace('.', ',')
                    except:
                        continue

                    new_row = {'Product_name': product_name, 'SKU': sku, 'Size': str(row['size']), 'StockX_payout': str(stockx_price).replace(
                        '.', ','), 'Alias_payout': str(alias_price).replace('.', ','), 'Best_site': site, 'Best_price': str(best_price).replace('.0', ',0'),
                        'Additional_sites': add_sites}

                df = df.append(new_row, ignore_index=True)
                print('\n'+product_name)
                print(sku)
                print(size)
                print({'StockX: ': stockx_price,
                      'Alias': alias_price, 'Best_site': site, 'Additional_sites': add_sites})

            with pd.ExcelWriter('output/prices.xlsx', engine='openpyxl', mode='a') as writer:
                df.to_excel(writer, sheet_name=sheets[i])
