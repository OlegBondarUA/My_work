import asyncio
import uvloop
import csv
from time import perf_counter

import httpx
from bs4 import BeautifulSoup

counter = 0
tasks = []

notebooks_list = []

fieldnames = (
    'id', 'name', 'price', 'availability', 'image',
)

GOOGLE_BOT = {
    'user-agent': 'APIs-Google (+https://developers.google.com/webmasters/'
                  'APIs-Google.html)'
}


def get_notebooks_urls(response_text: str):
    soup = BeautifulSoup(response_text, 'html.parser')
    notebooks = soup.select('.goods-tile__picture')
    return [notebook.get('href') for notebook in notebooks]


def process_detail_notebook(response_text: str):
    global counter
    soup = BeautifulSoup(response_text, 'html.parser')

    name = soup.select('.product__title')
    price = soup.select('.product-prices__big')
    availability = soup.select('.product-statuses__item')
    image = soup.select('.main-slider__item img')

    counter += 1

    notebook = {
        'id': counter,
        'name': name[0].text.strip(),
        'price': price[0].text.replace('\xa0', '').strip() if price else None,
        'availability': availability[0].text.strip() if availability else None,
        'image': [img.get('src') for img in image]
    }
    notebooks_list.append(notebook)


async def detail_worker(queue, worker_number):
    while True:
        if queue.qsize() == 0:
            break
        url = await queue.get()
        print(f'[Request in {worker_number}], queue_size '
              f'{queue.qsize()}, {url}')
        try:
            async with httpx.AsyncClient() as session:
                response = await session.get(url, timeout=10,
                                             headers=GOOGLE_BOT)
                assert response.status_code == 200,\
                    f'Bad status{response.status_code}'

            process_detail_notebook(response.text)

        except Exception as error:
            print(error)
            await queue.put(url)


async def links_worker(queue: asyncio.Queue, worker_number: int):
    while True:
        if queue.qsize() == 0:
            break

        url = await queue.get()
        if url == 'https://rozetka.com.ua/ua/notebooks/c80004/page=1/':
            url = 'https://rozetka.com.ua/ua/notebooks/c80004/'

        print(f'[Request in {worker_number}], '
              f'queue_size {queue.qsize()}, {url}')

        try:
            async with httpx.AsyncClient() as session:
                response = await session.get(url, timeout=10,
                                             headers=GOOGLE_BOT)
                assert response.status_code == 200, \
                    f'Bad status{response.status_code}'

            notebooks_urls = get_notebooks_urls(response.text)
            print('Urls appended')
            print(len(notebooks_urls))
            url_list_queue = asyncio.Queue()

            for url in notebooks_urls:
                url_list_queue.put_nowait(url)

            for worker in range(len(notebooks_urls)):
                task = await detail_worker(url_list_queue, worker)
                tasks.append(task)

        except Exception as error:
            print(error)
            await queue.put(url)


async def main():
    with open('rozetka.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

    queue = asyncio.Queue()
    domain = 'https://rozetka.com.ua/ua/notebooks/c80004/page={page}/'
    last_page = 20
    workers = 20

    for page in range(1, last_page + 1):
        queue.put_nowait(domain.format(page=page))

    for worker_number in range(workers):
        task = links_worker(queue, worker_number)
        tasks.append(task)

    await asyncio.gather(*tasks)

    print('WRITING DATA TO FILE!!!')
    with open('rozetka.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        for row in notebooks_list:
            writer.writerow(row)


if __name__ == '__main__':
    uvloop.install()
    start_time = perf_counter()

    asyncio.run(main())

    end_time = perf_counter()
    print(f'SCRAPPING DONE in {end_time - start_time:.2f} seconds')
