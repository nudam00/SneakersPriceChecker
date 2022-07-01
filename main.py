import os
from openpyxl import Workbook
from selenium import webdriver
from prices import Prices
import pandas as pd
from size_converter import Size
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium_stealth import stealth


def data():
    # Loads data from txt
    with open('data.txt', 'r') as file:
        txt = file.readlines()
    a = txt[0]
    b = txt[1]
    c = float(txt[2].replace("\n", ''))
    d = float(txt[3].replace("\n", ''))
    return [a, b, c, d]


def shoes(emai, passw, gbp, eur, name, driv, t):
    # Gets all needed data from sites
    df = pd.DataFrame(columns=['Product_name', 'SKU', 'Size', 'Stockx_payout', 'Restocks_payout', 'Stockx_price',
                               'Restocks_price', 'Site', 'Max_ZL', 'Max_Curr'])
    excel = pd.read_excel('shoes.xlsx', sheet_name=name)

    # Based on each row in excel sheet
    for index, row in excel.iterrows():
        if '.0' in str(row['size']):
            size = str(row['size']).replace('.0', '')
        else:
            size = str(row['size'])
        sku = row['sku']
        value = row['price']
        typ = row['type']
        converter = Size(size, row['sku'])
        sizes_list = converter.sizes()

        prices = Prices(driv, sizes_list, sku, emai, passw, t, gbp, eur)

        # Gets stockx price
        stockx = prices.stockx()
        item_name = stockx[0]
        price1 = stockx[1]
        price_stockx = stockx[2]

        # Gets restocks price
        restocks = prices.restocks()
        price2 = restocks[0]
        price_restocks = restocks[1]

        t += 1
        sites = {price_stockx: 'Stockx', price_restocks: 'Restocks'}

        # Calculates best site and linked price
        if typ == 'Faktura':
            income_stockx = price_stockx - (value / 1.23)
            income_restocks = price_restocks - value + (value - (value / 1.23) - price_restocks + (price_restocks / 1.21
                                                                                                   ))
            prices = {income_stockx: price_stockx,
                      income_restocks: price_restocks}
            incomes = [income_stockx, income_restocks]
            max_income = max(incomes)
            site = str(sites[prices[max_income]])
            if site == 'Stockx':
                max_price = price1
                max_price_zl = price_stockx
            else:
                max_price = ""
                max_price_zl = price_restocks
        else:
            income_stockx = price_stockx - value
            income_restocks = price_restocks - value - \
                (price_restocks - (price_restocks / 1.21))
            prices = {income_stockx: price_stockx,
                      income_restocks: price_restocks}
            incomes = [income_stockx, income_restocks]
            max_income = max(incomes)
            site = str(sites[prices[max_income]])
            if site == 'Stockx':
                max_price = price1
                max_price_zl = price_stockx
            else:
                max_price = ""
                max_price_zl = price_restocks

        new_row = {'Product_name': item_name, 'SKU': sku, 'Size': str(row['size']), 'Stockx_payout': str(price_stockx),
                   'Restocks_payout': str(price_restocks), 'Stockx_price': str(price1), 'Restocks_price': str(price2),
                   'Site': site, 'Max_ZL': str(max_price_zl), 'Max_Curr': str(max_price)}
        df = df.append(new_row, ignore_index=True)
        print('\n'+item_name)
        print(sku)
        print(row['size'])
        print({'Stockx: ': price_stockx, 'Restocks: ': price_restocks, })

    return df


print('data.txt:\n'
      '1. Put stockx email\n'
      '2. Put stockx password\n'
      '3. Put GBP exchange rate with "." format\n'
      '4. Put EUR exchange rate with "." format\n'
      '\n'
      'shoes.xlsx:\n'
      '1. Put sku\n'
      "2. Put sizes into that format:\n"
      "Men - e.g. 9/9.5\n"
      "Women - e.g. 9W/9.5W\n"
      "Gs - e.g. 6Y/6.5Y\n"
      '3. Put price with "." format\n'
      '4. Put "Faktura" if you add VAT to margin\n'
      '\n'
      'Write anything if you want to start\n')
input()

try:
    os.remove("stock.xlsx")
except FileNotFoundError:
    pass
wb = Workbook()
wb.save(filename='stock.xlsx')
data = data()
email = data[0]
password = data[1]
kurs_gbp = data[2]
kurs_eur = data[3]
sheets = pd.ExcelFile('shoes.xlsx').sheet_names

options = Options()
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
s = Service('C:\\BrowserDrivers\\chromedriver.exe')
driver = webdriver.Chrome(options=options,
                          executable_path="C:/Users/dratw/Documents/PythonProjects/priceChecker/chromedriver.exe")
stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )

# Based on each sheet in excel file
for i in range(len(pd.ExcelFile('shoes.xlsx').sheet_names)):
    if i == 0:
        stock = shoes(email, password, kurs_gbp, kurs_eur, i, driver, i)
    else:
        stock = shoes(email, password, kurs_gbp, kurs_eur, i, driver, 1)
    with pd.ExcelWriter('stock.xlsx', engine='openpyxl', mode='a') as writer:
        stock.to_excel(writer, sheet_name=sheets[i])

writer.save()
writer.close()
