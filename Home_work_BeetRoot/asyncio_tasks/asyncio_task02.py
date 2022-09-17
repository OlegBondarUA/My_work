import asyncio
import json
import aiohttp
import ssl
import certifi
import requests

from time import time


async def create_list_comment(url, session):
    async with session.get(url, allow_redirects=True):
        response = requests.get(url).json()
        data = []
        for i in response['data']:
            comments = {
                'author': i['author'],
                'comment': i['body'],
                'subreddit': i['subreddit'],
                'created_utc': i['created_utc']
            }
            data.append(comments)

        with open('comments.json', 'a') as file:
            json.dump(data, file, indent=4)


async def main():
    url = 'https://api.pushshift.io/reddit/comment/search/'

    tasks = []

    ssl_context = ssl.create_default_context(cafile=certifi.where())
    conn = aiohttp.TCPConnector(ssl=ssl_context)

    async with aiohttp.ClientSession(connector=conn) as session:
        task = asyncio.create_task(create_list_comment(url, session))
        tasks.append(task)
        await asyncio.gather(*tasks)

if __name__ == '__main__':
    start = time()

    asyncio.run(main())

    end_time = time()
    print(f'Getting comments finished in {end_time - start:.2f} seconds')
