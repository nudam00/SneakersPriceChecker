# SneakersPriceChecker

Program which scraps sneaker prices based on **sku** and **size** and writes out prices in PLN to the excel file. Scrapped sites:

1. StockX - prices must be in USD.
2. Alias - prices must be in USD.
   <br />
   StockX ends up blocked by PerimeterX quite often, so PerimeterX needs to be resolved sometimes.<br />
   Written in Python using Playwright, requests and cloudsraper.

## Converters

size_converter.py - converts all sizes to fit the page.

## Input

### settings.json - write your credentials on Alias and StockX fee

`{"email": "x", "alias_username": "x", "alias_password": "x", "stockx_password": "x", "stockx_fee": 0.x, "usd_rate": x, "proxy": "http://username:passw@ip:port"}`

### stock.xlsx

1. Write SKU.
2. Write size in US.
   <br />

## Output

### prices.xslx

Look at:

1. StockX and Alias payouts in PLN (rounded down to tens).
2. Best site/s.
3. Best price rounded down to tens.
   <br />

## Sites

1. alias.py - checks the price on Alias.
2. stockx.py - checks the price on StockX.
   <br />

## add.py

A few additional functions.

## main.py

It brings the whole program together. Calls classes based on data in stock.xlsx and writes prices to prices.xlsx.
