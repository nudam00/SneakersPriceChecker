# SneakersPriceChecker
Program which checks sneaker prices on StockX and writes out to an Excel file the best price in **PLN** after deducting the commission (the commision depends on the level of the account on Stockx). The price on StockX is detected based on the SKU and size in US. Price from StockX is compared to price on Alias (Excel file, just write price in USD) and it writes out final price. In stock.xlsx there are two columns named "dni_stockx" and "dni_alias" - write:
1. "NIE" if you would like to get price-1
2. "TAK" if you would like to get price
3. "MASAKRA" if you would like to write both sites in "Best_site", even if the second site has lower price (example: "MASAKRA" in "dni_alias" - a pair of sneakers sells on Alias very rarely so I would like to list it on StockX as well even if the price is lower, if higher then "Alias" won't be written in "Best_site").
<br /> 
StockX ends up blocked by PerimeterX quite often, so the program will be restarted automatically and PerimeterX needs to be resolved. You also have to choose region and log in manually again.<br /> 
Written in Python using Selenium.

## stockx.py
Checks the price on StockX. It takes the same price as displayed in the application for 100%.

## restocks.py
Outdated.

## size_converter.py
Converts sizes to fit the page. Restocks is executed based on restocks.json.

## prices.py
Returns prices after commission (modify self.stockx_fee if you have different account level).

## add.py
A few additional functions.

## main.py
It brings the whole program together. Calls classes based on data in stock.xlsx and writes prices to prices.xlsx.

## stock.xlsx
Write SKU, size in US.
Write in "dni_stockx" and "dni_alias":
1. "NIE" if you would like to get price-1.
2. "TAK" if you would like to get price.
3. "MASAKRA" if you would like to write both sites in "Best_site", even if the second site has lower price (example: "MASAKRA" in "dni_alias" - a pair of sneakers sells on Alias very rarely so I would like to list it on StockX as well even if the price is lower, if higher then "Alias" won't be written in "Best_site"). Price will be considered as price-1.
Write price in USD from Alias app.

## price.xslx
Look at:
1. StockX and Alias payouts in PLN (rounded down to tens).
2. StockX price in GBP (only if best site is StockX, created for my need).
3. Best site/s.
4. Best price rounded down to tens.
