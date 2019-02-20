import requests
import json
from selenium import webdriver
from decimal import Decimal
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from bs4 import BeautifulSoup

url = 'https://jk-grinada.ru/catalog/flats/'

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)


def price():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    #chrome_options=options
    browser = webdriver.Chrome(chrome_options=options)
    browser.get(url)
    sleep(5)
    x = browser.find_element_by_class_name("results-list__body")
    start = True
    while start:
        try:
            button = x.find_element_by_class_name('btn-medium')
            button.click()
            sleep(1)
        except NoSuchElementException:
            start = False
    html = browser.page_source
    browser.quit()
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('a', class_='item')
    for item in items:
        object = item.find_all('div', class_='param__value')
        complex = "Гринада"
        type_building = 'flat'
        building = object[0].string
        section = object[1].string
        floor = int(object[2].string)
        number = int(object[3].string)
        rooms = int(object[4].string)
        area = Decimal(object[5].string)
        price = Decimal(object[7].string.replace(' ',''))
        item = dict(
            complex=complex,
            phase=None,
            building=building,
            section=section,
            floor=floor,
            number=number,
            number_on_site=None,
            price=price,
            rooms=rooms,
            area=area,
            in_sale=1,
            type=type_building,
            finished=0)
        r = [item]
        print(json.dumps(r, cls=DecimalEncoder, indent=1, sort_keys=False))


if __name__ == '__main__':
    price()
