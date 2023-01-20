# SneakersPriceChecker
Program which checks sneaker prices based on **sku** and **size** and writes out in PLN to the excel file. Sites which are scrapped:
1. StockX - prices must be in USD. 
2. Alias - prices must be in USD.
3. Restocks - prices must be in EUR.
4. Klekt - prices must be in EUR.
5. WETHENEW - prices must be in EUR.
<br /> 
StockX ends up blocked by PerimeterX quite often, so the program will be restarted automatically and PerimeterX needs to be resolved. You also have to choose region and log in manually again.<br /> 
Written in Python using Selenium, requests and Playwright.

## Converters
1. prices.py - returns prices in PLN after commission.
2. restocks.json - size converter to restocks size.
3. size_converter.py - converts all sizes to fit the page.
4. wethenew.json - size converter to wethenew size.
<br />

## Input
1. settings.json - write your credentials on Alias and StockX fee
```{"alias_username": "x", "alias_password": "x", "stockx_fee": 0.x, "wethenew_password": "x"}```

## Output
### prices.xslx
Look at:
1. StockX and Alias payouts in PLN (rounded down to tens).
3. Best site/s.
4. Best price rounded down to tens.
5. Best additional sites (which are not that popular like StockX or Alias).
<br />

### stock.xlsx
1. Write SKU.
2. Write size in US.
<br />

## Sites
1. alias.py - checks the price on Alias.
2. restocks.py - check the price on Restocks.
3. stockx.py - checks the price on StockX.
4. klekt.py - check the price on Klekt.
5. wethenew.py - check the price on WETHENEW.
<br />

## add.py
A few additional functions.

## main.py
It brings the whole program together. Calls classes based on data in stock.xlsx and writes prices to prices.xlsx.

## INCOMING
1. Hypeboost
2. Sneakit
3. Best sizes based on price (will compare to StockX and Alias)
4. StockX rewrite
5. Whole program rewrite