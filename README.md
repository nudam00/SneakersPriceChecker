# SneakersPriceChecker
Program which checks sneaker prices on StockX and writes out to an Excel file the best price after deducting the commission (the commision depends on the level of the account on Stockx). The price is selected based on the SKU, size in US. Price from StockX is compared to price on Alias (Excel file) and it writes out final price. <br /> 
Each first time the program is turned on at intervals, it ends up blocked by PerimeterX, in which case the program must be restarted and PerimeterX resolved. You also have to choose region and log in manually (PerimeterX is blocking horribly).<br /> 
Written in Python using Selenium.

## stockx.py
A file that checks the price on StockX. It performs automatic logging, chooses region based on IP and selects the size, which is placed in data.txt.

## restocks.py
A file that checks the price on Restocks. It selects the region of the Netherlands (so that the currency is EUR) and chooses the size, which is placed in data.txt.

## size_converter.py
Converts sizes to fit the page (Klekt and Goat out of date). Restocks is executed based on restocks.json.

## prices.py
Returns prices after commission (modify StockX if you have different account level).

## main.py
It brings the whole program together. Calls classes based on data in shoes.xlsx and writes prices to stock.xlsx.

## data.txt
Create file data.txt with:
1. Put Stockx email
2. Put Stockx password
3. Put GBP exchange rate with "." format
4. Put EUR exchange rate with "." format

## shoes.xlsx
Write SKU, size in US, price in ZL (with "." format) and "Faktura" if you want add VAT (23%) to margin.

## stock.xslx
Look at best prices and site. It writes two sites if the difference is ~10zl.
