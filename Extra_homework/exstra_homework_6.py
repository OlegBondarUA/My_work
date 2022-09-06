import json
import csv
import pandas as pd
import sqlite3

from requests import Session
from bs4 import BeautifulSoup


def main():
    url = 'https://rozetka.com.ua/ua/notebooks/c80004/'

    with Session() as session:
        response = session.get(url, timeout=10)
        assert response.status_code == 200, 'bad response'
        print(response.status_code)

    soup = BeautifulSoup(response.content, 'html.parser')

    items_list = soup.find_all('li', class_="catalog-grid__cell catalog-grid__"
                                            "cell_type_slim ng-star-inserted")

    data = []

    for item in items_list:
        img = item.find('img').get('src')
        title = item.find('a',
                          class_="goods-tile__heading ng-star-inserted").text.strip()
        price = item.find('div', class_="goods-tile__prices").find('p',
                                                                   class_="ng-star-inserted").text.strip().replace('\xa0', '')
        status = item.find('div',
                           class_="goods-tile__availability").text.strip()
        link = item.find('a',
                         class_="goods-tile__heading ng-star-inserted").get(
            'href').strip()

        data.append(
            {
                'img': img,
                'title': title,
                'price': price,
                'status': status,
                'link': link
            }
        )

    with open('laptops.json', 'w') as file:
        json.dump(data, file, indent=4,
                  ensure_ascii=False,
                  separators=(',', ': '))

    with open('laptops.csv', 'w', ) as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['img', 'title', 'price', 'status', 'link'])

        for item in data:
            writer.writerow([item['img'], item['title'],
                             item['price'], item['status'], item['link']])


with open('laptops.json') as f:
    laptop = json.load(f)

df = pd.DataFrame(laptop)
df.head()

conn = sqlite3.connect('laptops.db')
cursor = conn.cursor()
df.to_sql('laptops', conn)

if __name__ == '__main__':
    main()
