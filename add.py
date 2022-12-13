import requests
from bs4 import BeautifulSoup
from lxml import etree
from selenium import webdriver
from selenium_stealth import stealth
from datetime import datetime


def getDriver():
    # Opening driver with needed options
    # Choose region, save cookies and log in manually (due to PerimeterX)
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(
        chrome_options=options, executable_path='C:/Users/dratw/Documents/codes/priceChecker/chromedriver.exe')
    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )
    driver.get("https://stockx.com/")
    print("Choose region and log in manually, type anything...")
    input()
    return driver


def getExchange():
    # Get exchange rates (eur/pln, gbp/pln, usd/pln) from NBP site
    page = requests.get('https://www.nbp.pl/home.aspx?f=/kursy/kursya.html')
    soup = BeautifulSoup(page.content, "html.parser")
    dom = etree.HTML(str(soup))
    eur = float(
        dom.xpath('//tr[8]/td[3][@class="right"]')[0].text.replace(',', '.'))
    gbp = float(
        dom.xpath('//tr[11]/td[3][@class="right"]')[0].text.replace(',', '.'))
    usd = float(
        dom.xpath('//tr[2]/td[3][@class="right"]')[0].text.replace(',', '.'))
    return [eur, gbp, usd]


def captcha():
    # Runs if PerimeterX is detected
    print("{}: Solve captcha".format(datetime.now()))
    return getDriver()
