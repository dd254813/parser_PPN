import requests
import json
import urllib3
from decimal import Decimal
from bs4 import BeautifulSoup


url = 'https://you-me.ru/buy/params/'

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)


def price():
    http = urllib3.PoolManager()
    html = http.request('GET', url)
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='line_wrapper')
    for item in items:
        complex = "Ты и Я"
        type_building = 'flat'
        section = item.find('div', class_='sort_section').string
        floor = item.find('div', class_='sort_floor').string
        rooms = item.find('div', class_='sort_rooms').string
        try:
            div = item.find('div', class_='decoration_on')
            area = Decimal(div.find('span', class_='data_f_item').get_text().replace('М2','').replace(',','.'))
            finished = 1
        except:
            div = item.find('div', class_='decoration_off')
            area = Decimal(div.find('span', class_='data_f_item').get_text().replace('М2','').replace(',','.'))
            finished = 0
            pass
        number = item.find('div', class_='flatinfo_item').get_text().replace('Квартира№','').replace(' ','')
        price = Decimal(item.find('div', class_='flat_cost').get_text().replace(' ',''))
        item = dict(
            complex=complex,
            phase=None,
            building=None,
            section=section,
            floor=int(floor),
            number=int(number),
            number_on_site=None,
            price=price,
            rooms=int(rooms),
            area=area,
            in_sale=1,
            type=type_building,
            finished=finished)
        r = [item]
        print(json.dumps(r, cls=DecimalEncoder, indent=1, sort_keys=False))



if __name__ == '__main__':
    price()
