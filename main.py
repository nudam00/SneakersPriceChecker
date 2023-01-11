import os
from openpyxl import Workbook
from prices import Prices
import pandas as pd
from size_converter import Size
from add import getDriver, getExchange


def shoes(gbp, eur, usd, name, driv):
    # Gets all needed data from sites
    df = pd.DataFrame(columns=['Product_name', 'SKU', 'Size', 'StockX_payout',
                               'Alias_payout', 'StockX_price', 'Best_site', 'Best_price'])
    excel = pd.read_excel('stock.xlsx', sheet_name=name)

    new_row = {'Product_name': '', 'SKU': '', 'Size': '', 'StockX_payout': '',
               'Alias_payout': '', 'StockX_price': '', 'Best_site': '', 'Best_price': ''}

    # Based on each row in excel sheet (stock.xlsx)
    for index, row in excel.iterrows():
        if '.0' in str(row['size']):
            size = str(row['size']).replace('.0', '')
        else:
            size = str(row['size'])
        sku = row['sku']
        dni_stockx = row['dni_stockx']
        dni_alias = row['dni_alias']
        price_alias = row['price_alias']

        # If same shoe as before then get saved data from earlier iteration
        if size == new_row['Size'] and sku == new_row['SKU']:
            pass
        else:
            converter = Size(size, sku)
            sizes_list = converter.sizes()
            prices = Prices(driv, sizes_list, sku, gbp, eur,
                            usd, dni_stockx, dni_alias, price_alias)

            # Gets Stockx price
            item_name, price_stockx, price_stockx_pln, driver = prices.stockx()
            driv = driver

            # Best price and site
            price_alias_pln = prices.alias()
            site, best_price = prices.bestPrice(
                price_stockx_pln, price_alias_pln)
            # It could be deleted, created just for my need
            if site == 'Alias':
                price_stockx = ''

            new_row = {'Product_name': item_name, 'SKU': sku, 'Size': str(row['size']), 'StockX_payout': str(
                price_stockx_pln).replace('.', ','), 'Alias_payout': str(price_alias_pln).replace('.', ','),
                'StockX_price': str(price_stockx).replace('.0', ''), 'Best_site': site, 'Best_price': str(best_price).replace('.0', ',0')}

        # Adds row
        df = df.append(new_row, ignore_index=True)
        print('\n'+item_name)
        print(sku)
        print(row['size'])
        print({'StockX: ': price_stockx_pln,
              'Alias': price_alias_pln, 'Best_site': site})

    return [df, driver]


if __name__ == "__main__":
    print('stock.xlsx:\n'
          '1. Write sku\n'
          "2. Write sizes into that format:\n"
          "Men - e.g. 9/9.5\n"
          "Women - e.g. 9W/9.5W\n"
          "Gs - e.g. 6Y/6.5Y\n"
          "3. Write 'NIE' if you want to get price-1 on StockX\n"
          "4. Write 'NIE' if you want to get price-1 on Alias\n"
          "5. Write price on Alias in USD\n"
          '\n'
          'Write anything when you would like to start\n')
    input()

    eur, gbp, usd = getExchange()
    driver = getDriver()
    try:
        os.remove("prices.xlsx")
    except FileNotFoundError:
        pass
    wb = Workbook()
    wb.save(filename='prices.xlsx')
    sheets = pd.ExcelFile('stock.xlsx').sheet_names

    # Based on each sheet in excel file
    for i in range(len(pd.ExcelFile('stock.xlsx').sheet_names)):
        stock, driver2 = shoes(gbp, eur, usd, i, driver)
        driver = driver2
        with pd.ExcelWriter('prices.xlsx', engine='openpyxl', mode='a') as writer:
            stock.to_excel(writer, sheet_name=sheets[i])
