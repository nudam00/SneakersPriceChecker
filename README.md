# SneakersPriceChecker

Not updated for a while, but it should still work. <br/>
Program which scraps sneaker prices based on **sku** and **size** and writes out prices in PLN to the excel file. Scrapped sites:

1. StockX - prices must be in USD.
2. Alias - prices must be in USD.
3. Klekt - prices must be in EUR.
4. Wethenew - prices must be in EUR.
5. Hypeboost - prices must be in EUR.
6. Sneakit - prices must be in EUR.

   <br />
   StockX ends up blocked by PerimeterX quite often, so PerimeterX needs to be resolved sometimes.<br />
   StockX and Alias are basic sites, it will prints out Klekt/Wethenew/Hypeboost only if the price is equal or higher than price on StockX/Alias and if the margin is above margin given in settings.json.
   In stock.xlsx there are two columns called stockx and alias. You can write here "NIE" (means that it sells rarely) or "TAK" (means that it sell quite often). Example: If you write "NIE" in stockx column and "TAK" in alias column then even if the price on StockX is higher than on Alias it will take Alias price as the highest one. If you write "TAK" in stockx column and price is higher than on Alias then it will print out StockX only.<br />
   Written in Python using Playwright, requests and cloudsraper.

## Converters

size_converter.py - converts all sizes to fit the page.

## Input

### settings.json - create that by yourself

`{"email": "x", "alias_username": "x", "alias_password": "x", "stockx_password": "x", "wethenew_email_": "x", "wethenew_password": "x", "sneakit_password": "x", "stockx_fee": 0.x, "usd_rate": x, "eur_rate": x, "proxy": "http://username:passw@ip:port", "margin": x}`

### stock.xlsx

1. Write SKU.
2. Write size in US.
3. Write net price
4. Write "TAK" or "NIE"
5. Write "TAK" or "NIE"
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
