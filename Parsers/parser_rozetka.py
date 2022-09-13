from concurrent.futures import ThreadPoolExecutor
from threading import Lock
from queue import Queue

from requests import Session
from bs4 import BeautifulSoup

from table_pars import Image, Price, Product


class RozetkaScraper:
    LOCK = Lock()
    TIME = 10

    def __init__(self, domain_url: str, last_page: int):
        self._domain_url = domain_url
        self._last_page = last_page

    def scrape(self):
        qu = self._fill_queue()
        print('Started scrapping!!!')
        with ThreadPoolExecutor(max_workers=20) as executor:
            for i in range(self._last_page):
                executor.submit(self._scrape, qu)

    def _fill_queue(self):
        qu = Queue()
        for page in range(1, self._last_page + 1):
            qu.put(self._domain_url.format(page=page))

        return qu

    def _scrape(self, qu: Queue):
        while True:
            url = qu.get()
            print(qu.qsize(), url)
            try:
                response_string = self._get_response(url)
                self._process(response_string)
            except Exception as error:
                print('Error', error)
                qu.put(url)

            if qu.empty():
                break

    def _get_response(self, url: str) -> str:
        try:
            with Session() as session:
                response = session.get(url, timeout=self.TIME)
                print(response.status_code)
                assert response.status_code == 200, 'Bad response'
            return response.text

        except Exception as error:
            print(error)

    @staticmethod
    def parse(html_string: str):
        soup = BeautifulSoup(html_string, 'html.parser')
        notebooks = soup.select('.goods-tile__inner')
        return notebooks

    def _process(self, html_string):
        notebooks = self.parse(html_string)
        with self.LOCK:
            for notebook in notebooks:
                sel_note = self.selection(notebook)
                price = self.insert_price(sel_note)
                product = self.insert_product(sel_note, price)
                self.insert_image(sel_note, product)
            print('PAGE SCRAPPED!!!')

    @staticmethod
    def selection(notebook):
        sel_note = {
            'name': notebook.select('.goods-tile__title'),
            'price': notebook.select('.goods-tile__price-value'),
            'old_price': notebook.select('.goods-tile__price--old'),
            'img_urls': notebook.select('.goods-tile__picture img'),
            'reviews': notebook.select('.goods-tile__reviews-link'),
            'promo': notebook.select('.goods-tile__label'),
            'availability': notebook.select('.goods-tile__availability'),
            'rating': notebook.select('.goods-tile__stars svg'),
        }
        sel_note['old_price'] = ''.join([
            num for num in sel_note['old_price'][0].text.replace('\xa0',
                                                                 '').strip()
            if num and num.isdigit()]) if sel_note['old_price'] else None
        return sel_note

    @staticmethod
    def insert_price(sel_note):
        price, _ = Price.get_or_create(
            price=int(sel_note['price'][0].text.replace('\xa0', '').strip()),
            old_price=int(sel_note['old_price']) if sel_note[
                'old_price'] else None
        )
        return price

    @staticmethod
    def insert_product(sel_note, price):
        notebook = {
            'name': sel_note['name'][0].text.strip(),
            'reviews': sel_note['reviews'][0].text.strip()
            if sel_note['reviews'] else None,
            'promo': sel_note['promo'][0].text.strip()
            if sel_note['promo'] else None,
            'price': price,
            'rating': sel_note['rating'][0].get('aria-label'),
            'availability': sel_note['availability'][0].text.strip()
            if sel_note['availability'] else None
        }
        product, _ = Product.get_or_create(**notebook)
        return product

    @staticmethod
    def insert_image(sel_note, product):
        images = [img.get('src') for img in sel_note['img_urls']]
        if images:
            for img in images:
                if img:
                    Image.create(product=product, url=img)


def main():
    domain = 'https://rozetka.com.ua/ua/notebooks/c80004/page={page}/'
    last_page = 67

    scraper = RozetkaScraper(domain, last_page)
    scraper.scrape()


if __name__ == '__main__':
    main()