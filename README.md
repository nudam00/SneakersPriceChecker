# SneakersPriceChecker

Program which scraps sneaker prices based on **sku** and **size** and writes out prices in PLN to the excel file. Scrapped sites:

1. StockX - prices must be in USD.
2. Alias - prices must be in USD.
3. Klekt - prices must be in EUR.
4. Wethenew - prices must be in EUR.
5. Hypeboost - prices must be in EUR.

   <br />
   StockX ends up blocked by PerimeterX quite often, so PerimeterX needs to be resolved sometimes.<br />
   StockX and Alias are basic sites, it will prints out Klekt/Wethenew/Hypeboost only if the price is equal or higher than price on StockX/Alias and if the margin is above margin given in settings.json.
   Written in Python using Playwright, requests and cloudsraper.

## Converters

size_converter.py - converts all sizes to fit the page.

## Input

### settings.json - create that by yourself

`{"email": "x", "alias_username": "x", "alias_password": "x", "stockx_password": "x", "wethenew_password": "x", "stockx_fee": 0.x, "usd_rate": x, "eur_rate": x, "proxy": "http://username:passw@ip:port", "margin": x}`

### stock.xlsx

1. Write SKU.
2. Write size in US.
3. Write net price
   <br />

## Output

### prices.xslx

Look at:

1. StockX and Alias payouts in PLN (rounded down to tens).
2. Best site/s.
3. Best price rounded down to tens.
4. Additional sites
   <br />

## Sites

Classes needed for checking prices.
<br />

## add.py

A few additional functions.

## main.py

It brings the whole program together. Calls classes based on data in stock.xlsx and writes prices to prices.xlsx.
