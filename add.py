import requests
from bs4 import BeautifulSoup
from lxml import etree
from selenium import webdriver
from selenium_stealth import stealth
from datetime import datetime
import json
import cloudscraper
import time


def get_driver():
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
    driver.get("https://pro.stockx.com/login")
    print("Log in manually, then type anything...")
    input()
    return driver


def get_exchange():
    # Get exchange rates (EUR/PLN, USD/PLN) from NBP site
    page = requests.get('https://www.nbp.pl/home.aspx?f=/kursy/kursya.html')
    soup = BeautifulSoup(page.content, features="lxml")
    dom = etree.HTML(str(soup))
    eur = float(
        dom.xpath('//tr[8]/td[3][@class="right"]')[0].text.replace(',', '.'))
    usd = float(
        dom.xpath('//tr[2]/td[3][@class="right"]')[0].text.replace(',', '.'))
    return [eur, usd]


def captcha():
    # Runs if PerimeterX is detected
    print("{}: Solve captcha".format(datetime.now()))
    return get_driver()


def get_scraper(username, password):
    # Gets scraper, alias token, region on restocks
    data = {"grantType": "password",
            "username": username, "password": password}
    url = 'https://sell-api.goat.com/api/v1/unstable/users/login'
    headers = {'Accept': 'application/json',
               'Accept-Encoding': 'gzip, deflate, br',
               'Accept-Language': 'pl-PL,pl;q=0.9',
               'User-Agent': 'alias/1.20.1 (iPhone; iOS 16.2; Scale/3.00) Locale/en',
               'x-emb-id': '2389040D96C04834A761C65276AC5564',
               'x-emb-st': str(int(time.time() * 1000)),
               'X-PX-AUTHORIZATION': '3',
               'X-PX-ORIGINAL-TOKEN': '3:87ec12c5b4c34832b42e88735f4da9949538cc013cb7ac2c48d8504371518d81:tT/X5LIfW0h1Ymfegj0v4hZx9Oj13sLWXGbw2+PCtg96IiaUfvn0SG5e/GH+QJPIphQY4u6NziXV+nQypGVLhQ==:1000:f9OqYPvRS2ATdeQYm+cskkymJJlSpyDHB++F566kPebKaJwCf2Y4nxse8wunIYMPytrJCPEOm6dZ8rD19SE/JpJH5cWswIgF7i2DQvMEyP+hVIDae1eUTuZViSvGiPlf2hjvkc8kAUbVDx4I72mqHCx6jzH1+F/2qsnWjdxL5lu7s/b+sdA035/eOeXBihKOcOTT08GYQ1EAkgqiFTMQPg==',
               'Connection': 'keep-alive',
               'Host': 'sell-api.goat.com',
               }
    scraper = cloudscraper.create_scraper()
    while True:
        try:
            restocks_region(scraper)
            r = scraper.post(data=json.dumps(
                data), headers=headers, url=url)
            return [json.loads(r.text)["auth_token"]['access_token'], scraper]
        except:
            continue


def restocks_region(scraper):
    soup = BeautifulSoup(scraper.get(
        'https://restocks.net/en').text, features="lxml")
    token = soup.find('meta', {'name': 'csrf-token'})['content']
    data = {'_token': token, 'country': 'PL',
            'language': 'en', 'valuta': 'EUR'}
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'pl,en-US;q=0.7,en;q=0.3',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0',
        'Referer': 'https://restocks.net/en',
        'Origin': 'https://restocks.net',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'Connection': 'keep-alive',
        'Host': 'restocks.net',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    url = 'https://restocks.net/localization'
    scraper.post(data=data, headers=headers,
                 url=url)
    return True
